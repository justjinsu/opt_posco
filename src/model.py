"""Pyomo optimization model for POSCO steel decarbonization.

Fixed ETS cost logic with proper CCUS handling and detailed OPEX.
"""

import logging
import pyomo.environ as pyo
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)
OBJ_SCALE = 1e-9

def build_model(
    params: Dict[str, Any], 
    discount_rate: float = 0.05,
    utilization: float = 0.90, 
    ccus_capture_rate: float = 0.80
) -> pyo.ConcreteModel:
    """Build POSCO optimization model with corrected ETS logic.
    
    Args:
        params: Parameter dictionary from io.load_parameters()
        discount_rate: Annual discount rate (e.g., 0.05 = 5%)
        utilization: Max capacity utilization (e.g., 0.90 = 90%)
        ccus_capture_rate: CCUS CO2 capture rate (e.g., 0.80 = 80%)
    
    Returns:
        Pyomo model with corrected ETS cost logic
    """
    
    logger.info("Building optimization model with corrected ETS logic")
    logger.info(f"Discount rate: {discount_rate:.1%}, Utilization: {utilization:.1%}")
    logger.info(f"CCUS capture rate: {ccus_capture_rate:.1%}")
    
    model = pyo.ConcreteModel(name="POSCO_Decarbonization")
    
    # ========== SETS ==========
    
    model.routes = pyo.Set(initialize=params['routes'], doc="Production routes")
    model.years = pyo.Set(initialize=params['years'], doc="Years", ordered=True)
    
    # Identify CCUS routes
    ccus_routes = [r for r in params['routes'] if 'CCUS' in r]
    model.ccus_routes = pyo.Set(initialize=ccus_routes, doc="Routes with CCUS")
    
    logger.info(f"Routes: {len(model.routes)} total, {len(ccus_routes)} with CCUS")
    logger.info(f"CCUS routes: {ccus_routes}")
    
    # ========== PARAMETERS ==========
    
    # Time parameters
    t0 = params['t0']
    model.t0 = pyo.Param(initialize=t0, doc="Base year")
    
    # Technology parameters
    model.unit_capacity = pyo.Param(model.routes, initialize=params['tech']['unit_capacity'], doc="Unit capacity (Mt/y)")
    model.capex = pyo.Param(model.routes, initialize=params['tech']['capex'], doc="CAPEX (USD/tpy)")
    model.fixed_opex = pyo.Param(model.routes, initialize=params['tech']['fixed_opex'], doc="Fixed O&M (USD/tpy/y)")
    
    # Emission factors (pre-CCUS capture)
    model.ef_scope1_gross = pyo.Param(model.routes, initialize=params['ef_scope1'], doc="Gross emission factor (tCO2/t)")
    
    # Compute net emission factors with CCUS applied
    ef_net = {}
    for route in params['routes']:
        ef_gross = params['ef_scope1'][route]
        if route in ccus_routes:
            ef_net[route] = ef_gross * (1.0 - ccus_capture_rate)  # Apply capture
            logger.info(f"Route {route}: EF {ef_gross:.3f} -> {ef_net[route]:.3f} tCO2/t (CCUS {ccus_capture_rate:.1%})")
        else:
            ef_net[route] = ef_gross
    
    model.ef_net = pyo.Param(model.routes, initialize=ef_net, doc="Net emission factor (tCO2/t, post-CCUS)")
    
    # Process intensities
    intensities = params['intensity']
    model.iron_ore_int = pyo.Param(model.routes, initialize=intensities.get('iron_ore_t', {}), doc="Iron ore intensity (t/t)")
    model.coking_coal_int = pyo.Param(model.routes, initialize=intensities.get('coking_coal_t', {}), doc="Coking coal intensity (t/t)")
    scrap_intensity = intensities.get('scrap_t', {})
    # ensure routes without entries default to zero
    scrap_init = {route: scrap_intensity.get(route, 0.0) for route in params['routes']}
    model.scrap_int = pyo.Param(model.routes, initialize=scrap_init, doc="Scrap intensity (t/t)")
    model.ng_int = pyo.Param(model.routes, initialize=intensities.get('ng_GJ', {}), doc="Natural gas intensity (GJ/t)")
    model.elec_int = pyo.Param(model.routes, initialize=intensities.get('electricity_MWh', {}), doc="Electricity intensity (MWh/t)")
    model.h2_int = pyo.Param(model.routes, initialize=intensities.get('h2_kg', {}), doc="Hydrogen intensity (kg/t)")
    model.flux_int = pyo.Param(model.routes, initialize=intensities.get('fluxes_t', {}), doc="Flux intensity (t/t)")
    model.alloys_usd = pyo.Param(model.routes, initialize=intensities.get('alloys_USD', {}), doc="Alloys cost (USD/t)")
    
    # Market parameters
    model.demand = pyo.Param(model.years, initialize=params['demand'], doc="Steel demand (Mt/y)")
    model.carbon_price = pyo.Param(model.years, initialize=params['carbon_price'], doc="Carbon price (USD/tCO2)")
    model.free_alloc = pyo.Param(model.years, initialize=params['free_alloc'], doc="Free allocation (MtCO2/y)")
    model.scrap_supply = pyo.Param(model.years, initialize=params['scrap_supply'], doc="Available scrap (Mt/y)")
    
    # Discount factors
    discount_factors = {y: 1.0 / ((1 + discount_rate) ** (y - t0)) for y in params['years']}
    model.discount_factor = pyo.Param(model.years, initialize=discount_factors, doc="Discount factors")
    
    # Log ETS parameters for first/last 3 years
    years_sorted = sorted(params['years'])
    trace_years = years_sorted[:3] + years_sorted[-3:]
    logger.info("ETS parameters (first/last 3 years):")
    for year in trace_years:
        logger.info(f"  {year}: carbon_price=${params['carbon_price'][year]:.0f}/tCO2, free_alloc={params['free_alloc'][year]:.1f}MtCO2")
    
    # ========== DECISION VARIABLES ==========
    
    model.Q = pyo.Var(model.routes, model.years, domain=pyo.NonNegativeReals, doc="Production (Mt/y)")
    model.K = pyo.Var(model.routes, model.years, domain=pyo.NonNegativeReals, doc="Capacity (Mt/y)")
    model.Build = pyo.Var(model.routes, model.years, domain=pyo.NonNegativeIntegers, doc="Builds (units)")
    
    # ETS positive variable: max(0, scope1 - free_alloc)
    model.ETSpos = pyo.Var(model.years, domain=pyo.NonNegativeReals, doc="ETS positive part (MtCO2)")
    
    logger.info(f"Variables: {len(model.routes)*len(model.years)*3 + len(model.years)} total")
    
    # ========== CONSTRAINTS ==========
    
    # 1. Demand satisfaction
    def demand_rule(model, year):
        return sum(model.Q[route, year] for route in model.routes) == model.demand[year]
    model.demand_constraint = pyo.Constraint(model.years, rule=demand_rule, doc="Demand satisfaction")
    
    # 2. Capacity balance
    def capacity_rule(model, route, year):
        if year == min(model.years):
            # Initial capacity: give BF-BOF enough to meet demand, others start at zero
            if 'BF-BOF' in route and 'CCUS' not in route:
                initial_cap = model.demand[year] * 1.1  # 110% buffer
                return model.K[route, year] == initial_cap + model.unit_capacity[route] * model.Build[route, year]
            else:
                return model.K[route, year] == model.unit_capacity[route] * model.Build[route, year]
        else:
            prev_year = model.years.prev(year)
            return model.K[route, year] == model.K[route, prev_year] + model.unit_capacity[route] * model.Build[route, year]
    model.capacity_balance = pyo.Constraint(model.routes, model.years, rule=capacity_rule, doc="Capacity balance")
    
    # 3. Utilization constraint
    def utilization_rule(model, route, year):
        return model.Q[route, year] <= utilization * model.K[route, year]
    model.utilization_constraint = pyo.Constraint(model.routes, model.years, rule=utilization_rule, doc="Utilization limit")

    # 4. Scrap availability constraint
    def scrap_limit_rule(model, year):
        total_scrap = sum(model.scrap_int[route] * model.Q[route, year] for route in model.routes)
        return total_scrap <= model.scrap_supply[year]
    model.scrap_limit = pyo.Constraint(model.years, rule=scrap_limit_rule, doc="Scrap availability limit")
    
    # 5. ETS linearization: ETSpos[t] >= sum(ef_net[r] * Q[r,t]) - free_alloc[t]
    def ets_balance_rule(model, year):
        # Scope 1 emissions in MtCO2: Mt production * tCO2/t = MtCO2
        scope1_mt = sum(model.ef_net[route] * model.Q[route, year] for route in model.routes)
        free_mt = model.free_alloc[year]  # Already in MtCO2
        return model.ETSpos[year] >= scope1_mt - free_mt
    model.ets_balance = pyo.Constraint(model.years, rule=ets_balance_rule, doc="ETS positive part constraint")
    
    # 6. Technology timing constraints
    h2_routes = [r for r in model.routes if 'H2' in r or 'HyREX' in r]
    if h2_routes:
        def h2_timing_rule(model, route, year):
            if route in h2_routes and year < 2030:
                return model.Build[route, year] == 0
            else:
                return pyo.Constraint.Skip
        model.h2_timing = pyo.Constraint(model.routes, model.years, rule=h2_timing_rule, doc="H2 timing constraints")
        logger.info(f"Applied timing constraints to H2 routes: {h2_routes}")
    
    # ========== OBJECTIVE ==========
    
    def objective_rule(model):
        """Minimize NPV of total system cost with detailed OPEX."""
        total_cost = 0
        price_fn = params['price_fn']
        hydrogen_case = params['options']['hydrogen_case']
        
        for year in model.years:
            disc = model.discount_factor[year]
            
            # CAPEX costs
            capex_t = sum(
                model.Build[route, year] * model.unit_capacity[route] * 1e6 * model.capex[route]
                for route in model.routes
            )
            
            # Fixed O&M costs
            fixom_t = sum(
                model.K[route, year] * 1e6 * model.fixed_opex[route]
                for route in model.routes
            )
            
            # Variable OPEX (detailed by commodity)
            var_t = 0
            for route in model.routes:
                # Cost per ton of steel produced (USD/t)
                usd_per_t = (
                    model.iron_ore_int[route] * price_fn("iron_ore_USD_per_t", year) +
                    model.coking_coal_int[route] * price_fn("coking_coal_USD_per_t", year) +
                    model.scrap_int[route] * price_fn("scrap_USD_per_t", year) +
                    model.ng_int[route] * price_fn("ng_USD_per_GJ", year) +
                    model.elec_int[route] * price_fn("electricity_USD_per_MWh", year) +
                    model.h2_int[route] * price_fn(f"hydrogen_USD_per_kg_{hydrogen_case}", year) +
                    model.flux_int[route] * price_fn("fluxes_USD_per_t", year) +
                    model.alloys_usd[route]  # Already in USD/t
                )
                # Total variable cost: Mt production * USD/t * 1e6 t/Mt = USD
                var_t += model.Q[route, year] * usd_per_t * 1e6
            
            # ETS costs: MtCO2 * 1e6 tCO2/MtCO2 * USD/tCO2 = USD
            ets_t = model.carbon_price[year] * model.ETSpos[year] * 1e6
            
            # Add discounted costs to total
            total_cost += disc * (capex_t + fixom_t + var_t + ets_t)
        
        # Scale to billions for better numerics
        return total_cost * OBJ_SCALE
    
    model.objective = pyo.Objective(rule=objective_rule, sense=pyo.minimize, doc="Minimize NPV total system cost")
    
    logger.info("Model built successfully with corrected ETS logic")
    num_constraints = len(list(model.component_objects(pyo.Constraint)))
    num_variables = len(list(model.component_objects(pyo.Var)))
    logger.info(f"Constraints: {num_constraints}")
    logger.info(f"Variables: {num_variables}")
    
    return model

def solve_model(model: pyo.ConcreteModel, solver: str = 'glpk') -> Tuple[str, float]:
    """Solve model and return status, objective."""
    opt = pyo.SolverFactory(solver)
    results = opt.solve(model, tee=True)
    status = str(results.solver.termination_condition)
    obj_val = pyo.value(model.objective) / OBJ_SCALE if results.solver.termination_condition == pyo.TerminationCondition.optimal else float('inf')
    return status, obj_val

def extract_solution(model: pyo.ConcreteModel, params: Dict[str, Any]) -> Dict[str, Any]:
    """Extract solution data."""
    solution = {
        'production': {r: {y: pyo.value(model.Q[r, y]) for y in model.years} for r in model.routes},
        'capacity': {r: {y: pyo.value(model.K[r, y]) for y in model.years} for r in model.routes},
        'builds': {r: {y: int(pyo.value(model.Build[r, y])) for y in model.years} for r in model.routes},
        'emissions': {y: sum(pyo.value(model.Q[r, y]) * pyo.value(model.ef_net[r]) 
                            for r in model.routes) for y in model.years},
        'ets_cost': {y: pyo.value(model.ETSpos[y]) * 1e6 * pyo.value(model.carbon_price[y]) 
                    for y in model.years}
    }
    return solution
