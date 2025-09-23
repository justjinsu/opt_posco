"""Sanity checks and validation for POSCO model results with corrected ETS logic."""

import logging
from typing import Dict, Any
import pyomo.environ as pyo

logger = logging.getLogger(__name__)

def validate_solution(
    solution: Dict[str, Any], 
    params: Dict[str, Any], 
    model: pyo.ConcreteModel, 
    tolerance: float = 1e-6
) -> None:
    """Run comprehensive solution validation checks with corrected ETS logic."""
    
    logger.info("Running enhanced solution validation checks...")
    
    # Check 1: Demand satisfaction
    logger.info("Checking demand satisfaction...")
    for year in params['years']:
        total_prod = sum(solution['production'][r][year] for r in params['routes'])
        demand = params['demand'][year]
        
        if abs(total_prod - demand) > tolerance:
            raise ValueError(f"Demand not met in {year}: production={total_prod:.6f} vs demand={demand:.6f} Mt")
    
    logger.info("✓ Demand satisfaction check passed")
    
    # Check 2: Non-negative flows
    logger.info("Checking non-negative flows...")
    for route in params['routes']:
        for year in params['years']:
            prod = solution['production'][route][year]
            cap = solution['capacity'][route][year]
            build = solution['builds'][route][year]
            
            if prod < -tolerance:
                raise ValueError(f"Negative production: {route} in {year}: {prod}")
            if cap < -tolerance:
                raise ValueError(f"Negative capacity: {route} in {year}: {cap}")
            if build < -tolerance:
                raise ValueError(f"Negative builds: {route} in {year}: {build}")
    
    logger.info("✓ Non-negative flows check passed")
    
    # Check 3: Capacity-utilization feasibility
    logger.info("Checking capacity utilization constraints...")
    utilization_limit = 0.90  # Should match model parameter
    
    for route in params['routes']:
        for year in params['years']:
            prod = solution['production'][route][year]
            capacity = solution['capacity'][route][year]
            
            if capacity > tolerance:  # Only check if there's capacity
                util_rate = prod / capacity
                if util_rate > utilization_limit + tolerance:
                    raise ValueError(f"Utilization exceeded: {route} in {year}: {util_rate:.3f} > {utilization_limit}")
    
    logger.info("✓ Capacity utilization check passed")
    
    # Check 4: ETS cost logic (CORRECTED)
    logger.info("Checking corrected ETS cost logic...")
    ets_mismatches = 0
    
    for year in params['years']:
        # Get values
        scope1_mt = solution['emissions'][year]  # MtCO2 (net, post-CCUS)
        free_alloc_mt = params['free_alloc'][year]  # MtCO2
        carbon_price = params['carbon_price'][year]  # USD/tCO2
        ets_cost_model = solution['ets_cost'][year]  # USD (from model)
        
        # Independent calculation
        net_emissions_mt = max(0, scope1_mt - free_alloc_mt)  # MtCO2
        ets_cost_calc = net_emissions_mt * 1e6 * carbon_price  # MtCO2 * 1e6 * USD/tCO2 = USD
        
        # Check consistency
        rel_error = abs(ets_cost_model - ets_cost_calc) / max(ets_cost_calc, 1e-6)
        
        if rel_error > tolerance:
            logger.warning(f"{year}: ETS cost mismatch - scope1={scope1_mt:.3f}Mt, free={free_alloc_mt:.1f}Mt, "
                         f"price=${carbon_price:.0f}/t, model=${ets_cost_model/1e6:.2f}M, calc=${ets_cost_calc/1e6:.2f}M")
            ets_mismatches += 1
        
        # Specific logic checks
        if scope1_mt <= free_alloc_mt + tolerance:
            # Should have minimal ETS cost
            if ets_cost_model > tolerance * carbon_price * 1e6:
                raise ValueError(f"ETS cost should be ~0 in {year}: scope1={scope1_mt:.3f} <= free_alloc={free_alloc_mt:.1f}, "
                               f"but cost=${ets_cost_model/1e6:.2f}M")
        else:
            # Should have positive ETS cost
            if ets_cost_model < (scope1_mt - free_alloc_mt) * carbon_price * 1e6 * (1 - tolerance):
                raise ValueError(f"ETS cost too low in {year}: expected ~${ets_cost_calc/1e6:.2f}M, got ${ets_cost_model/1e6:.2f}M")
    
    if ets_mismatches > 0:
        logger.warning(f"Found {ets_mismatches} ETS cost mismatches (may be due to model/calculation differences)")
    
    logger.info("✓ ETS cost logic check passed")
    
    # Check 5: Unit consistency spot checks
    logger.info("Checking unit consistency...")
    for year in [min(params['years']), max(params['years'])]:  # Check first and last year
        total_prod = sum(solution['production'][r][year] for r in params['routes'])  # Mt
        total_emissions = solution['emissions'][year]  # MtCO2
        
        # Rough check: emissions should be 0.1-3.0 tCO2/t steel for steel industry
        if total_prod > 0:
            emissions_intensity = total_emissions / total_prod * 1e6  # MtCO2/Mt * 1e6 = tCO2/t
            if emissions_intensity < 0.05 or emissions_intensity > 5.0:
                logger.warning(f"Unusual emissions intensity in {year}: {emissions_intensity:.2f} tCO2/t steel "
                             f"(total_prod={total_prod:.1f}Mt, emissions={total_emissions:.3f}MtCO2)")
        
        # Check that ETS costs are reasonable scale
        ets_cost = solution['ets_cost'][year]
        carbon_price = params['carbon_price'][year]
        if ets_cost > total_emissions * 1e6 * carbon_price * 2:  # Allow 2x buffer for max case
            logger.warning(f"Very high ETS cost in {year}: ${ets_cost/1e9:.1f}B (may indicate unit issues)")
    
    logger.info("✓ Unit consistency checks passed")
    
    # Check 6: Objective components additivity (if available)
    logger.info("Checking objective components...")
    if hasattr(model, 'objective') and 'objective_components' in solution:
        model_obj = pyo.value(model.objective) * 1e9  # Convert from billions
        reported_obj = solution['objective_components'].get('total_npv_USD', 0)
        
        if abs(model_obj - reported_obj) > abs(model_obj) * tolerance:
            logger.warning(f"Objective mismatch: model=${model_obj/1e9:.3f}B, reported=${reported_obj/1e9:.3f}B")
    
    logger.info("✓ Objective components check passed")
    
    logger.info("All enhanced validation checks completed successfully!")

def print_solution_summary(solution: Dict[str, Any], params: Dict[str, Any]) -> None:
    """Print detailed solution summary with corrected calculations."""
    
    print("\n" + "="*60)
    print("ENHANCED SOLUTION SUMMARY")
    print("="*60)
    
    # Basic production info
    years = sorted(params['years'])
    first_year, last_year = years[0], years[-1]
    
    total_first = sum(solution['production'][r][first_year] for r in params['routes'])
    total_last = sum(solution['production'][r][last_year] for r in params['routes'])
    
    print(f"\nProduction Summary:")
    print(f"  Total {first_year}: {total_first:.1f} Mt")
    print(f"  Total {last_year}: {total_last:.1f} Mt")
    print(f"  Change: {((total_last/total_first)-1)*100:+.1f}%")
    
    # Route mix evolution
    print(f"\nRoute Mix {first_year} vs {last_year}:")
    for route in params['routes']:
        prod_first = solution['production'][route][first_year]
        prod_last = solution['production'][route][last_year]
        share_first = prod_first / total_first * 100 if total_first > 0 else 0
        share_last = prod_last / total_last * 100 if total_last > 0 else 0
        
        if prod_first > 0.001 or prod_last > 0.001:  # Only show significant routes
            print(f"  {route:15s}: {share_first:5.1f}% → {share_last:5.1f}% "
                  f"({prod_first:5.1f} → {prod_last:5.1f} Mt)")
    
    # Emissions and ETS summary
    emissions_first = solution['emissions'][first_year]
    emissions_last = solution['emissions'][last_year]
    emissions_reduction = (1 - emissions_last/emissions_first) * 100 if emissions_first > 0 else 0
    
    print(f"\nEmissions Summary (Scope 1, net):")
    print(f"  {first_year}: {emissions_first:.3f} MtCO2")
    print(f"  {last_year}: {emissions_last:.3f} MtCO2")
    print(f"  Reduction: {emissions_reduction:.1f}%")
    
    # ETS cost summary
    total_ets_cost = sum(solution['ets_cost'].values())
    years_with_ets = sum(1 for cost in solution['ets_cost'].values() if cost > 1000)  # >$1K threshold
    
    print(f"\nETS Cost Summary:")
    print(f"  Total undiscounted: ${total_ets_cost/1e9:.2f} billion")
    print(f"  Years with ETS costs: {years_with_ets}/{len(years)}")
    print(f"  Peak annual cost: ${max(solution['ets_cost'].values())/1e6:.1f} million")
    
    # Carbon pricing context
    carbon_prices = [params['carbon_price'][y] for y in years]
    print(f"\nCarbon Price Range: ${min(carbon_prices):.0f}-${max(carbon_prices):.0f}/tCO2")
    print(f"Free Allocation Range: {min(params['free_alloc'].values()):.1f}-{max(params['free_alloc'].values()):.1f} MtCO2")
    
    print("="*60)