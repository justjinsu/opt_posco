#!/usr/bin/env python3
"""
Multi-scenario runner for POSCO v2.0 decarbonization optimization.

Runs three carbon scenarios (NGFS_NetZero2050, NGFS_Below2C, NGFS_NDCs) with fixed 
hydrogen case. Aggregates results to outputs/series_all_scenarios.csv and calls src/viz.py.
"""

import logging
import pandas as pd
import argparse
import json
from pathlib import Path
from typing import Dict, Any, List
import time

from .io import load_parameters
from .model import build_model, solve_model, extract_solution
from .export import export_time_series, create_summary
from .sanity import validate_solution, print_solution_summary

logger = logging.getLogger(__name__)

def run_single_scenario(
    data_path: str,
    carbon_scenario: str,
    h2_case: str = 'baseline',
    discount_rate: float = 0.05,
    utilization: float = 0.90,
    output_dir: str = 'outputs',
    solver: str = 'highs',
    ccus_capture_rate: float = 0.80
) -> Dict[str, Any]:
    """
    Run optimization for a single carbon scenario.
    
    Args:
        data_path: Path to Excel data file
        carbon_scenario: Carbon price scenario (NGFS_NetZero2050, NGFS_Below2C, NGFS_NDCs)
        h2_case: Hydrogen price case ('baseline' or 'optimistic')
        discount_rate: Annual discount rate (default 0.05)
        utilization: Maximum capacity utilization (default 0.90)
        output_dir: Directory for output files
        
    Returns:
        Dictionary with scenario results including solution, summary, and status
    """
    
    logger.info(f"Running scenario: {carbon_scenario}")
    start_time = time.time()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Load parameters
    try:
        params = load_parameters(data_path, carbon_scenario, grid_case='base', hydrogen_case=h2_case)
        logger.info(f"Loaded parameters for {carbon_scenario}")
    except Exception as e:
        logger.error(f"Parameter loading failed for {carbon_scenario}: {e}")
        return {
            'scenario': carbon_scenario,
            'status': 'PARAMETER_ERROR',
            'error': str(e),
            'runtime_seconds': time.time() - start_time
        }
    
    # Build and solve model
    try:
        model = build_model(params, discount_rate, utilization, ccus_capture_rate=ccus_capture_rate)
        solver_status, objective_value = solve_model(model, solver)
        
        if solver_status != 'optimal':
            logger.error(f"Solver failed for {carbon_scenario}: {solver_status}")
            return {
                'scenario': carbon_scenario,
                'status': solver_status,
                'error': f"Solver termination: {solver_status}",
                'runtime_seconds': time.time() - start_time
            }
            
        logger.info(f"Optimal solution found for {carbon_scenario}: NPV = ${objective_value/1e9:.2f}B")
        
    except Exception as e:
        logger.error(f"Model building/solving failed for {carbon_scenario}: {e}")
        return {
            'scenario': carbon_scenario,
            'status': 'MODEL_ERROR',
            'error': str(e),
            'runtime_seconds': time.time() - start_time
        }
    
    # Extract solution
    try:
        solution = extract_solution(model, params)
        logger.info(f"Solution extracted for {carbon_scenario}")
    except Exception as e:
        logger.error(f"Solution extraction failed for {carbon_scenario}: {e}")
        return {
            'scenario': carbon_scenario,
            'status': 'EXTRACTION_ERROR',
            'error': str(e),
            'runtime_seconds': time.time() - start_time
        }
    
    # Validate solution
    try:
        # Create mock args for export functions
        mock_args = argparse.Namespace(
            carbon_scenario=carbon_scenario,
            h2_case=h2_case,
            discount=discount_rate,
            util=utilization
        )
        
        validate_solution(solution, params, model)
        logger.info(f"Solution validation passed for {carbon_scenario}")
        
        # Print solution summary
        print_solution_summary(solution, params)
        
    except Exception as e:
        logger.warning(f"Solution validation failed for {carbon_scenario}: {e}")
        # Continue with export even if validation fails
    
    # Export detailed results
    try:
        csv_path = output_path / f"series_{carbon_scenario}.csv"
        export_time_series(solution, params, str(csv_path))
        
        # Create summary report
        summary = create_summary(solution, params, mock_args, solver_status, objective_value)
        json_path = output_path / f"summary_{carbon_scenario}.json"
        with open(json_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Results exported for {carbon_scenario}")
        
    except Exception as e:
        logger.error(f"Export failed for {carbon_scenario}: {e}")
        return {
            'scenario': carbon_scenario,
            'status': 'EXPORT_ERROR',
            'error': str(e),
            'runtime_seconds': time.time() - start_time
        }
    
    runtime = time.time() - start_time
    logger.info(f"Scenario {carbon_scenario} completed successfully in {runtime:.1f}s")
    
    return {
        'scenario': carbon_scenario,
        'status': 'SUCCESS',
        'solver_status': solver_status,
        'objective_value': objective_value,
        'npv_billion_usd': objective_value / 1e9,
        'solution': solution,
        'summary': summary,
        'runtime_seconds': runtime,
        'ccus_capture_rate': ccus_capture_rate,
        'files': {
            'detailed_csv': str(csv_path),
            'summary_json': str(json_path)
        }
    }

def run_all_scenarios(
    data_path: str,
    h2_case: str = 'baseline',
    discount_rate: float = 0.05,
    utilization: float = 0.90,
    output_dir: str = 'outputs',
    solver: str = 'highs',
    ccus_capture_rate: float = 0.80
) -> Dict[str, Any]:
    """
    Run optimization for all three carbon scenarios.
    
    Args:
        data_path: Path to Excel data file
        h2_case: Hydrogen price case ('baseline' or 'optimistic')
        discount_rate: Annual discount rate (default 0.05)
        utilization: Maximum capacity utilization (default 0.90)
        output_dir: Directory for output files
        
    Returns:
        Dictionary with aggregated results from all scenarios
    """
    
    logger.info("Starting multi-scenario optimization run")
    logger.info(f"H2 case: {h2_case}, Discount rate: {discount_rate:.1%}, Utilization: {utilization:.1%}, CCUS capture: {ccus_capture_rate:.1%}")
    
    # Define scenarios to run
    scenarios = ['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs']
    
    # Run each scenario
    scenario_results = {}
    successful_scenarios = []
    
    for scenario in scenarios:
        try:
            result = run_single_scenario(
                data_path=data_path,
                carbon_scenario=scenario,
                h2_case=h2_case,
                discount_rate=discount_rate,
                utilization=utilization,
                output_dir=output_dir,
                solver=solver,
                ccus_capture_rate=ccus_capture_rate
            )
            scenario_results[scenario] = result
            
            if result['status'] == 'SUCCESS':
                successful_scenarios.append(scenario)
                logger.info(f"✓ {scenario}: NPV = ${result['npv_billion_usd']:.2f}B")
            else:
                logger.error(f"✗ {scenario}: {result['status']} - {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            logger.error(f"Unexpected error running {scenario}: {e}")
            scenario_results[scenario] = {
                'scenario': scenario,
                'status': 'UNEXPECTED_ERROR',
                'error': str(e)
            }
    
    logger.info(f"Completed {len(successful_scenarios)}/{len(scenarios)} scenarios successfully")
    
    # Aggregate results from successful scenarios
    if successful_scenarios:
        try:
            aggregate_results(scenario_results, successful_scenarios, output_dir)
            logger.info("Results aggregation completed")
        except Exception as e:
            logger.error(f"Results aggregation failed: {e}")
    
    # Create scenario comparison report
    comparison_report = create_scenario_comparison(scenario_results, output_dir)
    
    return {
        'run_summary': {
            'total_scenarios': len(scenarios),
            'successful_scenarios': len(successful_scenarios),
            'failed_scenarios': len(scenarios) - len(successful_scenarios),
            'h2_case': h2_case,
            'discount_rate': discount_rate,
            'utilization': utilization,
            'ccus_capture_rate': ccus_capture_rate
        },
        'scenario_results': scenario_results,
        'comparison_report': comparison_report
    }

def aggregate_results(scenario_results: Dict[str, Any], successful_scenarios: List[str], output_dir: str) -> None:
    """
    Aggregate detailed results from all successful scenarios into a single CSV file.
    
    Args:
        scenario_results: Results from all scenarios
        successful_scenarios: List of scenarios that completed successfully
        output_dir: Directory for output files
    """
    
    logger.info("Aggregating results from successful scenarios")
    
    # Load and combine detailed CSV files
    all_data = []
    
    for scenario in successful_scenarios:
        result = scenario_results[scenario]
        if result['status'] == 'SUCCESS':
            csv_path = result['files']['detailed_csv']
            try:
                df = pd.read_csv(csv_path)
                df['carbon_scenario'] = scenario
                all_data.append(df)
                logger.info(f"Loaded {len(df)} rows from {scenario}")
            except Exception as e:
                logger.warning(f"Failed to load results for {scenario}: {e}")
    
    if not all_data:
        logger.error("No data to aggregate")
        return
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Reorder columns to put scenario first
    cols = ['carbon_scenario'] + [col for col in combined_df.columns if col != 'carbon_scenario']
    combined_df = combined_df[cols]
    
    # Export aggregated results
    output_path = Path(output_dir) / 'series_all_scenarios.csv'
    combined_df.to_csv(output_path, index=False)
    
    logger.info(f"Aggregated results saved to {output_path}")
    logger.info(f"Total rows: {len(combined_df)}, scenarios: {combined_df['carbon_scenario'].nunique()}")

def create_scenario_comparison(scenario_results: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    """
    Create high-level comparison report across scenarios.
    
    Args:
        scenario_results: Results from all scenarios
        output_dir: Directory for output files
        
    Returns:
        Dictionary with comparison metrics
    """
    
    logger.info("Creating scenario comparison report")
    
    comparison_data = []
    
    for scenario, result in scenario_results.items():
        if result['status'] == 'SUCCESS':
            solution = result['solution']
            summary = result['summary']
            
            # Extract key metrics
            years = sorted(solution['scope1_emissions'].keys())
            first_year, last_year = years[0], years[-1]
            
            # Production metrics
            hotmetal_first = sum(solution['hotmetal_production'][r][first_year] for r in solution['hotmetal_production'].keys())
            hotmetal_last = sum(solution['hotmetal_production'][r][last_year] for r in solution['hotmetal_production'].keys())
            eaf_first = solution['eaf_production'][first_year]
            eaf_last = solution['eaf_production'][last_year]
            
            # Technology shares in final year
            total_final = hotmetal_last + eaf_last
            hotmetal_share_final = (hotmetal_last / total_final * 100) if total_final > 0 else 0
            eaf_share_final = (eaf_last / total_final * 100) if total_final > 0 else 0
            
            # Emissions metrics
            emissions_first = solution['scope1_emissions'][first_year]
            emissions_last = solution['scope1_emissions'][last_year]
            emissions_reduction = ((emissions_first - emissions_last) / emissions_first * 100) if emissions_first > 0 else 0
            
            # Economic metrics
            npv_total = result['objective_value'] / 1e9  # Billion USD
            ets_cost_total = sum(solution['ets_cost'].values()) / 1e9  # Billion USD
            
            comparison_data.append({
                'scenario': scenario,
                'status': 'SUCCESS',
                'npv_total_billion_usd': npv_total,
                'ets_cost_total_billion_usd': ets_cost_total,
                'ets_share_of_npv_percent': (ets_cost_total / npv_total * 100) if npv_total > 0 else 0,
                f'hotmetal_production_{first_year}_Mt': hotmetal_first,
                f'hotmetal_production_{last_year}_Mt': hotmetal_last,
                f'eaf_production_{first_year}_Mt': eaf_first,
                f'eaf_production_{last_year}_Mt': eaf_last,
                f'hotmetal_share_{last_year}_percent': hotmetal_share_final,
                f'eaf_share_{last_year}_percent': eaf_share_final,
                f'scope1_emissions_{first_year}_MtCO2': emissions_first,
                f'scope1_emissions_{last_year}_MtCO2': emissions_last,
                'emissions_reduction_percent': emissions_reduction,
                'cumulative_emissions_MtCO2': sum(solution['scope1_emissions'].values()),
                'runtime_seconds': result['runtime_seconds']
            })
        else:
            comparison_data.append({
                'scenario': scenario,
                'status': result['status'],
                'error': result.get('error', 'Unknown error'),
                'runtime_seconds': result.get('runtime_seconds', 0)
            })
    
    # Create comparison DataFrame and export
    comparison_df = pd.DataFrame(comparison_data)
    comparison_path = Path(output_dir) / 'scenario_comparison.csv'
    comparison_df.to_csv(comparison_path, index=False)
    
    logger.info(f"Scenario comparison saved to {comparison_path}")
    
    return {
        'comparison_file': str(comparison_path),
        'summary_metrics': comparison_data
    }

def main():
    """CLI entry point for multi-scenario runner."""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='POSCO v2.0 Multi-Scenario Optimization')
    parser.add_argument('--data', type=str, required=True, help='Path to Excel data file')
    parser.add_argument('--h2-case', type=str, default='baseline', choices=['baseline', 'optimistic'],
                       help='Hydrogen price case (default: baseline)')
    parser.add_argument('--discount', type=float, default=0.05, help='Discount rate (default: 0.05)')
    parser.add_argument('--util', type=float, default=0.90, help='Max utilization (default: 0.90)')
    parser.add_argument('--output', type=str, default='outputs', help='Output directory (default: outputs)')
    parser.add_argument('--viz', action='store_true', help='Generate visualization plots')
    parser.add_argument('--ccus-capture', type=float, default=0.80,
                        help='CCUS capture rate (0.80 = 80%% capture, 0 disables CCUS)')
    parser.add_argument('--scenario', type=str,
                        help='Run a single carbon scenario (e.g., NGFS_NetZero2050) instead of the full set')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not Path(args.data).exists():
        logger.error(f"Data file not found: {args.data}")
        return 1
    
    if not (0 < args.discount < 1):
        logger.error(f"Invalid discount rate: {args.discount}")
        return 1
    
    if not (0 < args.util <= 1):
        logger.error(f"Invalid utilization: {args.util}")
        return 1
    
    if not (0 <= args.ccus_capture <= 1):
        logger.error(f"Invalid CCUS capture rate: {args.ccus_capture}")
        return 1
    
    # Run scenarios
    try:
        if args.scenario:
            result = run_single_scenario(
                data_path=args.data,
                carbon_scenario=args.scenario,
                h2_case=args.h2_case,
                discount_rate=args.discount,
                utilization=args.util,
                output_dir=args.output,
                ccus_capture_rate=args.ccus_capture
            )
            results = {
                'run_summary': {
                    'total_scenarios': 1,
                    'successful_scenarios': 1 if result['status'] == 'SUCCESS' else 0,
                    'failed_scenarios': 0 if result['status'] == 'SUCCESS' else 1,
                    'h2_case': args.h2_case,
                    'discount_rate': args.discount,
                    'utilization': args.util,
                    'ccus_capture_rate': args.ccus_capture
                },
                'scenario_results': {args.scenario: result}
            }
        else:
            results = run_all_scenarios(
                data_path=args.data,
                h2_case=args.h2_case,
                discount_rate=args.discount,
                utilization=args.util,
                output_dir=args.output,
                ccus_capture_rate=args.ccus_capture
            )
        
        # Print summary
        print("\n" + "="*80)
        print("MULTI-SCENARIO OPTIMIZATION SUMMARY")
        print("="*80)
        
        run_summary = results['run_summary']
        print(f"Scenarios completed: {run_summary['successful_scenarios']}/{run_summary['total_scenarios']}")
        print(f"H2 case: {run_summary['h2_case']}")
        print(f"Discount rate: {run_summary['discount_rate']:.1%}")
        print(f"Utilization: {run_summary['utilization']:.1%}")
        print(f"CCUS capture rate: {run_summary.get('ccus_capture_rate', args.ccus_capture):.1%}")
        
        # Print scenario results
        for scenario, result in results['scenario_results'].items():
            if result['status'] == 'SUCCESS':
                print(f"✓ {scenario}: NPV = ${result['npv_billion_usd']:.2f}B")
            else:
                print(f"✗ {scenario}: {result['status']}")
        
        # Generate visualizations if requested
        if args.viz and run_summary['successful_scenarios'] > 0:
            try:
                from viz import create_scenario_plots
                create_scenario_plots(args.output)
                logger.info("Visualization plots generated")
            except ImportError:
                logger.warning("Visualization module not available")
            except Exception as e:
                logger.error(f"Visualization generation failed: {e}")
        
        print("="*80)
        
        return 0 if run_summary['successful_scenarios'] > 0 else 1
        
    except Exception as e:
        logger.error(f"Multi-scenario run failed: {e}")
        return 1

if __name__ == '__main__':
    exit(main())
