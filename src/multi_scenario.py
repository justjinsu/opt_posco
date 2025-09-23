#!/usr/bin/env python3
"""Multi-scenario runner for comprehensive POSCO analysis."""

import argparse
import logging
import json
import sys
from pathlib import Path
from typing import Dict, Any

from . import io, model, export, sanity, analysis

def setup_logging(level: str = 'INFO') -> None:
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run_scenario(
    params_file: str,
    scenario: str,
    grid_case: str,
    hydrogen_case: str,
    discount: float,
    util: float,
    solver: str,
    outdir: Path
) -> tuple:
    """Run a single scenario and return solution and parameters."""
    
    logger = logging.getLogger(__name__)
    logger.info(f"Running scenario: {scenario}")
    
    # Load parameters for this scenario
    params = io.load_parameters(params_file, scenario, grid_case, hydrogen_case)
    
    # Build and solve model
    opt_model = model.build_model(params, discount, util)
    status, obj_value = model.solve_model(opt_model, solver)
    
    if status != 'optimal':
        logger.error(f"Scenario {scenario} failed to solve: {status}")
        return None, None
    
    # Extract solution
    solution = model.extract_solution(opt_model, params)
    
    # Run validation
    sanity.validate_solution(solution, params, opt_model)
    
    # Export individual scenario results
    series_path = outdir / f"series_{scenario}.csv"
    export.export_time_series(solution, params, str(series_path))
    
    # Create enhanced summary
    summary_data = export.create_summary(
        solution, params, 
        argparse.Namespace(**{
            'carbon_scenario': scenario,
            'discount': discount,
            'util': util,
            'hydrogen_case': hydrogen_case,
            'grid_case': grid_case,
            'solver': solver
        }),
        status, obj_value
    )
    
    summary_path = outdir / f"summary_{scenario}.json"
    with open(summary_path, 'w') as f:
        json.dump(summary_data, f, indent=2)
    
    logger.info(f"Scenario {scenario} completed - NPV: ${obj_value/1e9:.2f}B")
    
    return solution, params

def main():
    """Run multiple scenarios and create comprehensive analysis."""
    
    parser = argparse.ArgumentParser(description='Multi-scenario POSCO Analysis')
    parser.add_argument('--params', required=True, help='Excel parameter file')
    parser.add_argument('--scenarios', nargs='+', default=['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs'],
                       help='Carbon scenarios to run')
    parser.add_argument('--grid_case', default='base', help='Grid carbon intensity case')
    parser.add_argument('--hydrogen_case', default='baseline', help='Hydrogen price case')
    parser.add_argument('--discount', type=float, default=0.05, help='Discount rate')
    parser.add_argument('--util', type=float, default=0.90, help='Max utilization')
    parser.add_argument('--solver', default='glpk', help='Optimization solver')
    parser.add_argument('--outdir', default='outputs', help='Output directory')
    
    args = parser.parse_args()
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("POSCO Multi-Scenario Analysis")
    logger.info(f"Running scenarios: {args.scenarios}")
    
    # Create output directory
    outdir = Path(args.outdir)
    outdir.mkdir(exist_ok=True)
    
    # Run all scenarios
    all_solutions = {}
    all_params = {}
    
    for scenario in args.scenarios:
        try:
            solution, params = run_scenario(
                args.params, scenario, args.grid_case, args.hydrogen_case,
                args.discount, args.util, args.solver, outdir
            )
            
            if solution is not None and params is not None:
                all_solutions[scenario] = solution
                all_params[scenario] = params
            else:
                logger.warning(f"Skipping failed scenario: {scenario}")
                
        except Exception as e:
            logger.error(f"Error in scenario {scenario}: {e}")
            continue
    
    if len(all_solutions) == 0:
        logger.error("No scenarios completed successfully")
        sys.exit(1)
    
    # Create comprehensive cross-scenario analysis
    logger.info("Creating enhanced analysis and visualizations")
    
    try:
        # Enhanced analysis with multiple outputs
        analysis.create_enhanced_exports(all_solutions, all_params, str(outdir))
        
        # Create consolidated CSV for all scenarios
        create_consolidated_outputs(all_solutions, all_params, outdir)
        
        logger.info("Multi-scenario analysis completed successfully")
        logger.info(f"Results available in: {outdir}")
        logger.info(f"Enhanced analysis in: {outdir}/analysis/")
        
    except Exception as e:
        logger.error(f"Error in enhanced analysis: {e}")
        logger.info("Individual scenario results are still available")

def create_consolidated_outputs(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create consolidated CSV outputs across all scenarios."""
    
    logger = logging.getLogger(__name__)
    logger.info("Creating consolidated outputs")
    
    import pandas as pd
    
    # Consolidated time series data
    all_series_data = []
    
    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        
        for year in params['years']:
            row = {
                'scenario': scenario,
                'year': year,
                'total_production_Mt': sum(solution['production'][r][year] for r in params['routes']),
                'scope1_emissions_MtCO2': solution['emissions'][year],
                'carbon_price_USD_tCO2': params['carbon_price'][year],
                'free_allocation_MtCO2': params['free_alloc'][year],
                'ets_cost_million_USD': solution['ets_cost'][year] / 1e6,
                'net_emissions_MtCO2': max(0, solution['emissions'][year] - params['free_alloc'][year])
            }
            
            # Add production by technology
            for route in params['routes']:
                row[f'prod_{route}_Mt'] = solution['production'][route][year]
            
            all_series_data.append(row)
    
    # Export consolidated time series
    df_consolidated = pd.DataFrame(all_series_data)
    df_consolidated.to_csv(outdir / "series_all_scenarios.csv", index=False)
    
    logger.info(f"Consolidated outputs created: {len(all_series_data)} data points")

if __name__ == '__main__':
    main()