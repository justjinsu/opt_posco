#!/usr/bin/env python3
import sys, logging
from pathlib import Path
import importlib.util
import pandas as pd

def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module

src = Path('src')
posco_io = load_module('posco_io', src / 'io.py')
posco_model = load_module('posco_model', src / 'model.py')
posco_export = load_module('posco_export', src / 'export.py')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger(__name__)

scenarios = [
    ('NGFS_NetZero2050', 'Net Zero 2050', '$383 in 2030, $638 in 2050'),
    ('NGFS_Below2C', 'Below 2°C', '$71 in 2030, $166 in 2050'),
    ('NGFS_NDCs', 'NDCs', '$118 in 2030, $130 in 2050')
]

output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)

results = {}

for scenario_id, name, prices in scenarios:
    logger.info("="*80)
    logger.info(f"SCENARIO: {name} ({prices})")
    logger.info("="*80)

    try:
        params = posco_io.load_parameters('data/posco_parameters_consolidated.xlsx', scenario_id, 'base', 'baseline')
        logger.info("✓ Parameters loaded")

        model = posco_model.build_model(params, 0.05, 0.90)
        logger.info("✓ Model built")

        logger.info("Solving...")
        status, obj = posco_model.solve_model(model, 'highs')

        if status != 'optimal':
            logger.error(f"✗ Status: {status}")
            continue

        logger.info(f"✓ OPTIMAL! NPV: ${obj/1e9:.2f}B")

        solution = posco_model.extract_solution(model, params)
        out_file = f'outputs/series_{scenario_id}.csv'
        posco_export.export_time_series(solution, params, out_file)
        logger.info(f"✓ Exported to {out_file}")

        # Calculate results
        df = pd.read_csv(out_file)
        cum = df['scope1_emissions_MtCO2'].sum()
        budget = 1110
        over = cum - budget
        over_pct = (over/budget)*100

        # 2050 mix
        p2050 = {}
        for col in df.columns:
            if col.startswith('production_') and col.endswith('_Mt') and col != 'production_total_Mt':
                tech = col.replace('production_', '').replace('_Mt', '')
                val = df[df['year']==2050][col].values[0]
                p2050[tech] = val

        total_2050 = sum(p2050.values())

        results[scenario_id] = {
            'name': name,
            'cum_emissions': cum,
            'overshoot': over,
            'overshoot_pct': over_pct,
            'npv': obj/1e9,
            'tech_2050': {k: (v/total_2050)*100 for k,v in p2050.items() if v/total_2050 > 0.01}
        }

        logger.info(f"\nCumulative emissions: {cum:.0f} MtCO2 ({over:+.0f}, {over_pct:+.1f}%)")
        logger.info(f"2050 Tech Mix:")
        for tech, share in results[scenario_id]['tech_2050'].items():
            logger.info(f"  {tech}: {share:.1f}%")
        logger.info("")

    except Exception as e:
        logger.error(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

# Summary
logger.info("\n" + "="*80)
logger.info("FINAL SUMMARY - NGFS Phase V Results")
logger.info("="*80)
for scenario_id, res in results.items():
    logger.info(f"\n{res['name']}:")
    logger.info(f"  Cumulative: {res['cum_emissions']:.0f} MtCO2 ({res['overshoot']:+.0f}, {res['overshoot_pct']:+.1f}%)")
    logger.info(f"  NPV: ${res['npv']:.2f}B")
    logger.info(f"  2050 Top technologies:")
    for tech, share in sorted(res['tech_2050'].items(), key=lambda x: -x[1])[:3]:
        logger.info(f"    {tech}: {share:.1f}%")

logger.info("\n" + "="*80)
logger.info("✓ ALL SCENARIOS COMPLETE!")
logger.info("="*80)
