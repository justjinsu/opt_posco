#!/usr/bin/env python3
"""
CLI interface for POSCO v2.0 decarbonization optimization model.

Supports single scenario runs and multi-scenario batch execution with comprehensive
analysis, validation, and visualization generation.
"""

import argparse
import logging
import json
import sys
import time
from pathlib import Path
from typing import Optional

# Import v2.0 modules
from io_v2 import load_parameters
from model_v2 import build_model, solve_model, extract_solution
from export_v2 import export_detailed_results, create_summary_report, save_summary_json
from sanity_v2 import validate_solution, print_solution_summary
from scenarios import run_all_scenarios, run_single_scenario
from viz import create_scenario_plots

def setup_logging(level: str = 'INFO') -> None:
    """Configure logging with enhanced formatting."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def parse_args():
    """Parse CLI arguments with v2.0 options."""
    parser = argparse.ArgumentParser(
        description='POSCO v2.0 Steel Decarbonization Optimization Model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single scenario run
  python run.py --data data/posco_parameters_consolidated_v2_0.xlsx --scenario NGFS_NetZero2050 --solve

  # Multi-scenario batch run
  python run.py --data data/posco_parameters_consolidated_v2_0.xlsx --multi-scenario --viz

  # Build model only (no solve)
  python run.py --data data/posco_parameters_consolidated_v2_0.xlsx --scenario NGFS_Below2C

Scenarios:
  - NGFS_NetZero2050: Net zero by 2050 pathway
  - NGFS_Below2C: Below 2°C pathway  
  - NGFS_NDCs: Nationally Determined Contributions pathway
        """
    )
    
    # Data and scenario
    parser.add_argument('--data', required=True, 
                       help='Excel data file with v2.0 parameter sheets')
    parser.add_argument('--scenario', choices=['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs'],
                       help='Carbon price scenario (required for single scenario)')
    parser.add_argument('--multi-scenario', action='store_true',
                       help='Run all three carbon scenarios')
    
    # Model options
    parser.add_argument('--h2-case', default='baseline', choices=['baseline', 'optimistic'],
                       help='Hydrogen price case (default: baseline)')
    parser.add_argument('--grid-case', default='base', choices=['base', 'fast', 'slow'],
                       help='Grid carbon intensity case (default: base)')
    parser.add_argument('--discount', type=float, default=0.05,
                       help='Annual discount rate (default: 0.05)')
    parser.add_argument('--util', type=float, default=0.90,
                       help='Maximum capacity utilization (default: 0.90)')
    
    # Solver options
    parser.add_argument('--solver', default='highs', choices=['glpk', 'cbc', 'gurobi', 'highs'],
                       help='Optimization solver (default: highs)')
    parser.add_argument('--solve', action='store_true',
                       help='Solve the optimization model')
    
    # Output options
    parser.add_argument('--output', default='outputs',
                       help='Output directory (default: outputs)')
    parser.add_argument('--viz', action='store_true',
                       help='Generate visualization plots')
    parser.add_argument('--validate', action='store_true',
                       help='Run solution validation checks')
    parser.add_argument('--summary', action='store_true',
                       help='Print detailed solution summary')
    
    # Logging
    parser.add_argument('--log-level', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level (default: INFO)')
    
    return parser.parse_args()

def validate_args(args) -> None:
    """Validate CLI arguments."""
    # Check data file exists
    if not Path(args.data).exists():
        raise FileNotFoundError(f"Data file not found: {args.data}")
    
    # Scenario validation
    if not args.multi_scenario and not args.scenario:
        raise ValueError("Must specify either --scenario or --multi-scenario")
    
    if args.multi_scenario and args.scenario:
        raise ValueError("Cannot specify both --scenario and --multi-scenario")
    
    # Parameter validation
    if not (0 < args.discount < 1):
        raise ValueError(f"Invalid discount rate: {args.discount}")
    
    if not (0 < args.util <= 1):
        raise ValueError(f"Invalid utilization: {args.util}")

def run_single_scenario_cli(args) -> int:
    """Run single scenario optimization."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Running single scenario: {args.scenario}")
    start_time = time.time()
    
    try:
        # Run scenario
        result = run_single_scenario(
            data_path=args.data,
            carbon_scenario=args.scenario,
            h2_case=args.h2_case,
            discount_rate=args.discount,
            utilization=args.util,
            output_dir=args.output,
            solver=args.solver
        )
        
        if result['status'] != 'SUCCESS':
            logger.error(f"Scenario failed: {result['status']} - {result.get('error', 'Unknown error')}")
            return 1
        
        # Print results
        runtime = time.time() - start_time
        logger.info(f"✓ Scenario completed successfully in {runtime:.1f}s")
        logger.info(f"NPV: ${result['npv_billion_usd']:.2f}B")
        logger.info(f"Files: {result['files']['detailed_csv']}")
        
        # Generate visualization if requested
        if args.viz:
            try:
                # Create single-scenario plots by temporarily creating aggregated format
                import pandas as pd
                df = pd.read_csv(result['files']['detailed_csv'])
                df['carbon_scenario'] = args.scenario
                
                output_path = Path(args.output)
                temp_path = output_path / 'series_all_scenarios.csv'
                df.to_csv(temp_path, index=False)
                
                create_scenario_plots(args.output)
                logger.info("Visualization plots generated")
                
                # Clean up temp file
                temp_path.unlink()
                
            except Exception as e:
                logger.warning(f"Visualization generation failed: {e}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Single scenario run failed: {e}")
        return 1

def run_multi_scenario_cli(args) -> int:
    """Run multi-scenario optimization."""
    logger = logging.getLogger(__name__)
    
    logger.info("Running multi-scenario optimization")
    start_time = time.time()
    
    try:
        # Run all scenarios
        results = run_all_scenarios(
            data_path=args.data,
            h2_case=args.h2_case,
            discount_rate=args.discount,
            utilization=args.util,
            output_dir=args.output,
            solver=args.solver
        )
        
        # Print summary
        runtime = time.time() - start_time
        run_summary = results['run_summary']
        
        print("\n" + "="*80)
        print("MULTI-SCENARIO OPTIMIZATION SUMMARY")
        print("="*80)
        print(f"Total runtime: {runtime:.1f}s")
        print(f"Scenarios completed: {run_summary['successful_scenarios']}/{run_summary['total_scenarios']}")
        print(f"H2 case: {run_summary['h2_case']}")
        print(f"Discount rate: {run_summary['discount_rate']:.1%}")
        print(f"Utilization: {run_summary['utilization']:.1%}")
        
        # Print scenario results
        for scenario, result in results['scenario_results'].items():
            if result['status'] == 'SUCCESS':
                print(f"✓ {scenario}: NPV = ${result['npv_billion_usd']:.2f}B")
            else:
                print(f"✗ {scenario}: {result['status']}")
        
        print("="*80)
        
        # Generate visualizations if requested
        if args.viz and run_summary['successful_scenarios'] > 0:
            try:
                create_scenario_plots(args.output)
                logger.info("Visualization plots generated")
            except Exception as e:
                logger.warning(f"Visualization generation failed: {e}")
        
        return 0 if run_summary['successful_scenarios'] > 0 else 1
        
    except Exception as e:
        logger.error(f"Multi-scenario run failed: {e}")
        return 1

def build_only_mode(args) -> int:
    """Build model without solving (for testing/validation)."""
    logger = logging.getLogger(__name__)
    
    logger.info(f"Building model for scenario: {args.scenario}")
    
    try:
        # Load parameters
        params = load_parameters(args.data, args.scenario, args.h2_case, args.grid_case)
        logger.info("Parameters loaded successfully")
        
        # Build model
        model = build_model(params, args.discount, args.util)
        logger.info("Model built successfully")
        
        # Print model statistics
        num_variables = sum(var.size for var in model.component_objects(ctype=model.Var))
        num_constraints = sum(con.size for con in model.component_objects(ctype=model.Constraint))
        
        print(f"\nModel Statistics:")
        print(f"  Variables: {num_variables:,}")
        print(f"  Constraints: {num_constraints:,}")
        print(f"  Time horizon: {params['years'][0]}-{params['years'][-1]} ({len(params['years'])} years)")
        print(f"  Hotmetal routes: {len(params['hotmetal_routes'])}")
        print(f"  Reduction routes: {len([r for r in params['reduction_routes'].keys() if r != 'HBI-import'])}")
        print(f"  Scenario: {args.scenario}")
        
        logger.info("Model building completed (use --solve to optimize)")
        return 0
        
    except Exception as e:
        logger.error(f"Model building failed: {e}")
        return 1

def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Print header
    logger.info("="*60)
    logger.info("POSCO v2.0 Decarbonization Optimization Model")
    logger.info("="*60)
    
    try:
        # Validate arguments
        validate_args(args)
        
        # Create output directory
        output_path = Path(args.output)
        output_path.mkdir(exist_ok=True)
        
        # Route to appropriate execution mode
        if args.multi_scenario:
            if args.solve:
                return run_multi_scenario_cli(args)
            else:
                logger.error("Multi-scenario mode requires --solve")
                return 1
                
        elif args.solve:
            return run_single_scenario_cli(args)
            
        else:
            return build_only_mode(args)
    
    except Exception as e:
        logger.error(f"CLI execution failed: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())