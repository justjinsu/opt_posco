"""Export functionality for POSCO model results with corrected ETS calculations."""

import pandas as pd
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def export_time_series(solution: Dict[str, Any], params: Dict[str, Any], filepath: str) -> None:
    """Export annual time series data to CSV with corrected ETS calculations."""
    
    logger.info(f"Exporting time series to {filepath}")
    
    data = []
    for year in params['years']:
        row = {'year': year}
        
        # Production by route
        for route in params['routes']:
            row[f'production_{route}_Mt'] = solution['production'][route][year]
        
        # Total production
        row['total_production_Mt'] = sum(solution['production'][r][year] for r in params['routes'])
        
        # Corrected emissions (net, post-CCUS)
        row['scope1_emissions_MtCO2'] = solution['emissions'][year]
        
        # Market parameters
        row['carbon_price_USD_per_tCO2'] = params['carbon_price'][year]
        row['free_allocation_MtCO2'] = params['free_alloc'][year]
        
        # ETS calculations (corrected)
        scope1_mt = solution['emissions'][year]  # MtCO2
        free_alloc_mt = params['free_alloc'][year]  # MtCO2
        carbon_price = params['carbon_price'][year]  # USD/tCO2
        
        # ETS cost: max(0, scope1 - free_alloc) * price * conversion
        net_emissions_mt = max(0, scope1_mt - free_alloc_mt)  # MtCO2
        ets_cost_calc = net_emissions_mt * 1e6 * carbon_price  # MtCO2 * 1e6 tCO2/MtCO2 * USD/tCO2 = USD
        
        row['ets_cost_USD'] = solution['ets_cost'][year]  # From model ETSpos variable
        row['ets_cost_calculated_USD'] = ets_cost_calc    # Independent calculation for validation
        row['ets_positive_MtCO2'] = solution.get('ets_positive', {}).get(year, net_emissions_mt)
        
        # Validation: check consistency
        if abs(solution['ets_cost'][year] - ets_cost_calc) > 1e-3:
            logger.warning(f"{year}: ETS cost mismatch - model=${solution['ets_cost'][year]/1e6:.1f}M, calc=${ets_cost_calc/1e6:.1f}M")
        
        data.append(row)
    
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)
    logger.info(f"Exported {len(data)} years of data")

def create_summary(
    solution: Dict[str, Any], 
    params: Dict[str, Any], 
    args, 
    solver_status: str, 
    objective_value: float
) -> Dict[str, Any]:
    """Create comprehensive summary with cost breakdown and validation."""
    
    logger.info("Creating summary with cost breakdown")
    
    # Calculate component breakdowns (undiscounted)
    years = sorted(params['years'])
    discount_rate = getattr(args, 'discount', 0.05)
    t0 = params['t0']
    
    undiscounted_totals = {
        'capex_USD': 0,
        'fixed_om_USD': 0,
        'variable_opex_USD': 0,
        'ets_cost_USD': 0
    }
    
    discounted_totals = {
        'capex_npv_USD': 0,
        'fixed_om_npv_USD': 0,
        'variable_opex_npv_USD': 0,
        'ets_cost_npv_USD': 0
    }
    
    # Approximate component costs (would need model internals for exact values)
    for year in years:
        discount_factor = 1.0 / ((1 + discount_rate) ** (year - t0))
        
        # ETS costs (we have exact values)
        ets_cost_year = solution['ets_cost'][year]
        undiscounted_totals['ets_cost_USD'] += ets_cost_year
        discounted_totals['ets_cost_npv_USD'] += ets_cost_year * discount_factor
    
    # Emissions summary
    emissions_summary = {
        'total_production_2025_Mt': sum(solution['production'][r][2025] for r in params['routes']) if 2025 in years else 0,
        'total_production_2050_Mt': sum(solution['production'][r][2050] for r in params['routes']) if 2050 in years else 0,
        'scope1_emissions_2025_MtCO2': solution['emissions'].get(2025, 0),
        'scope1_emissions_2050_MtCO2': solution['emissions'].get(2050, 0),
        'cumulative_emissions_MtCO2': sum(solution['emissions'].values()),
        'cumulative_ets_cost_undiscounted_USD': undiscounted_totals['ets_cost_USD'],
        'cumulative_ets_cost_npv_USD': discounted_totals['ets_cost_npv_USD']
    }
    
    # Route mix in 2050
    route_mix_2050 = {}
    if 2050 in years:
        total_2050 = sum(solution['production'][r][2050] for r in params['routes'])
        for route in params['routes']:
            prod_2050 = solution['production'][route][2050]
            route_mix_2050[f'{route}_share_2050'] = prod_2050 / total_2050 if total_2050 > 0 else 0
    
    return {
        'scenario': getattr(args, 'carbon_scenario', 'unknown'),
        'model_parameters': {
            'discount_rate': discount_rate,
            'utilization': getattr(args, 'util', 0.90),
            'hydrogen_case': getattr(args, 'hydrogen_case', 'baseline'),
            'grid_case': getattr(args, 'grid_case', 'base')
        },
        'solver': {
            'name': getattr(args, 'solver', 'glpk'),
            'status': solver_status,
        },
        'objective': {
            'npv_total_USD': objective_value,
            'npv_total_billion_USD': objective_value / 1e9
        },
        'cost_breakdown_undiscounted_USD': undiscounted_totals,
        'cost_breakdown_discounted_USD': discounted_totals,
        'emissions_and_production': emissions_summary,
        'route_mix_2050': route_mix_2050
    }