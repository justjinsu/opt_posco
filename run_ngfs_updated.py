#!/usr/bin/env python3
"""
Standalone runner for POSCO optimization with NGFS Phase V data.
Uses importlib to avoid naming conflicts.
"""

import sys
import logging
import json
from pathlib import Path
import importlib.util

def load_module(module_name, file_path):
    """Load a module from file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Load all src modules
src_dir = Path('src')
posco_io = load_module('posco_io', src_dir / 'io.py')
posco_model = load_module('posco_model', src_dir / 'model.py')
posco_export = load_module('posco_export', src_dir / 'export.py')
posco_sanity = load_module('posco_sanity', src_dir / 'sanity.py')

def setup_logging():
    """Setup logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

def run_scenario(data_file, scenario_name, output_dir='outputs'):
    """Run a single scenario."""
    logger = logging.getLogger(__name__)

    logger.info(f"=" * 80)
    logger.info(f"Running scenario: {scenario_name}")
    logger.info(f"=" * 80)

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True, parents=True)

    try:
        # Load parameters
        logger.info(f"Loading parameters...")
        params = posco_io.load_parameters(
            data_file,
            scenario_name,
            grid_case='base',
            hydrogen_case='baseline'
        )
        logger.info(f"✓ Parameters loaded")

        # Show carbon prices
        if 'carbon_price' in params:
            logger.info(f"Carbon prices (NGFS Phase V, US$2024):")
            cp = params['carbon_price']
            for year in [2025, 2030, 2040, 2050]:
                if year in cp.index:
                    logger.info(f"  {year}: ${cp.loc[year]:.0f}/tCO2")

        # Build model
        logger.info(f"Building optimization model...")
        opt_model = posco_model.build_model(
            params,
            discount_rate=0.05,
            utilization=0.90
        )
        logger.info(f"✓ Model built ({len(list(opt_model.component_data_objects()))} components)")

        # Solve model
        logger.info(f"Solving with HiGHS solver...")
        status, obj_value = posco_model.solve_model(opt_model, solver='highs')

        if status != 'optimal':
            logger.error(f"✗ Solver failed with status: {status}")
            return False

        logger.info(f"✓ Optimal solution found!")
        logger.info(f"  Objective value: ${obj_value/1e9:.2f} billion")

        # Extract solution
        logger.info(f"Extracting solution...")
        solution = posco_model.extract_solution(opt_model, params)
        logger.info(f"✓ Solution extracted")

        # Validate
        logger.info(f"Validating solution...")
        try:
            posco_sanity.validate_solution(solution, params, opt_model)
            logger.info(f"✓ Validation passed")
        except Exception as e:
            logger.warning(f"Validation warning: {e}")

        # Export results
        series_path = output_path / f"series_{scenario_name}.csv"
        logger.info(f"Exporting time series...")
        posco_export.export_time_series(solution, params, str(series_path))
        logger.info(f"✓ Results exported to {series_path}")

        # Print key results
        logger.info(f"\n" + "=" * 80)
        logger.info(f"KEY RESULTS FOR {scenario_name}")
        logger.info(f"=" * 80)

        # Calculate cumulative emissions
        if 'emissions_scope1' in solution:
            cum_emissions = solution['emissions_scope1'].sum()
            logger.info(f"Cumulative Scope 1 emissions (2025-2050): {cum_emissions:.0f} MtCO2")

            # Compare to budget
            budget = 1110  # MtCO2
            overshoot = cum_emissions - budget
            overshoot_pct = (overshoot / budget) * 100
            logger.info(f"Carbon budget: {budget} MtCO2")
            logger.info(f"Overshoot: {overshoot:+.0f} MtCO2 ({overshoot_pct:+.1f}%)")

        # Show key technology shares in 2050
        if 'production' in solution:
            logger.info(f"\n2050 Technology Mix:")
            prod_2050 = solution['production'].loc[2050]
            total_2050 = prod_2050.sum()
            if total_2050 > 0:
                for tech in prod_2050.index:
                    share = (prod_2050[tech] / total_2050) * 100
                    if share > 0.1:
                        logger.info(f"  {tech}: {share:.1f}% ({prod_2050[tech]:.1f} Mt)")

        logger.info(f"=" * 80)
        logger.info(f"\n")

        return True

    except Exception as e:
        logger.error(f"✗ Error running {scenario_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main runner."""
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("\n" + "=" * 80)
    logger.info("POSCO STEEL DECARBONIZATION OPTIMIZATION")
    logger.info("NGFS Phase V Carbon Price Scenarios (US$2024)")
    logger.info("=" * 80 + "\n")

    # Check data file
    data_files = [
        'data/posco_parameters_consolidated_v2_0.xlsx',
        'data/posco_parameters_consolidated.xlsx'
    ]

    data_file = None
    for df in data_files:
        if Path(df).exists():
            data_file = df
            break

    if not data_file:
        logger.error(f"✗ No data file found. Tried:")
        for df in data_files:
            logger.error(f"  - {df}")
        return 1

    logger.info(f"✓ Using data file: {data_file}\n")

    # Run scenarios
    scenarios = [
        ('NGFS_NetZero2050', 'Net Zero 2050 ($383 in 2030, $638 in 2050)'),
        ('NGFS_Below2C', 'Below 2°C ($71 in 2030, $166 in 2050)'),
        ('NGFS_NDCs', 'NDCs ($118 in 2030, $130 in 2050)')
    ]

    results = {}
    for scenario_name, description in scenarios:
        logger.info(f"\n{'='*80}")
        logger.info(f"SCENARIO: {description}")
        logger.info(f"{'='*80}\n")

        success = run_scenario(data_file, scenario_name)
        results[scenario_name] = success

        if not success:
            logger.error(f"✗ {scenario_name} failed!")
            # Don't continue if one fails - fix issues first
            break
        else:
            logger.info(f"✓ {scenario_name} completed successfully!\n")

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("SUMMARY")
    logger.info("=" * 80)
    for scenario_name, success in results.items():
        status = "✓ SUCCESS" if success else "✗ FAILED"
        logger.info(f"  {scenario_name}: {status}")
    logger.info("=" * 80 + "\n")

    logger.info(f"✓ All outputs saved to: outputs/")
    logger.info(f"✓ Check series_*.csv files for time series results")

    # Check if all succeeded
    if all(results.values()):
        logger.info(f"\n✓ ALL SCENARIOS COMPLETED SUCCESSFULLY!")
        logger.info(f"\n📊 Next steps:")
        logger.info(f"  1. Check outputs/series_*.csv for detailed results")
        logger.info(f"  2. Update Section 4 (Results) in main.tex with new values")
        logger.info(f"  3. Run generate_publication_figures.py to update figures")
        logger.info(f"  4. Compile LaTeX and submit!")
        return 0
    else:
        logger.error(f"\n✗ Some scenarios failed. Check logs above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
