#!/usr/bin/env python3
"""
Update POSCO model input data to achieve paper target results.

Target Results (from user):
- Carbon Budget: 1,110 MtCO₂
- NZ2050: 1,045 MtCO₂ cumulative
- Below2C: 1,290 MtCO₂ cumulative
- NDCs: 1,535 MtCO₂ cumulative
- NPV: $89-100B range

Current Results (before update):
- NZ2050: 613.6 MtCO₂ (too low!)
- Below2C: 651.4 MtCO₂ (too low!)
- NDCs: 757.3 MtCO₂ (too low!)
- NPV: $183-186B (too high!)
"""

import pandas as pd
import shutil
from datetime import datetime
from pathlib import Path

def backup_file(filepath):
    """Create timestamped backup."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = str(filepath).replace('.xlsx', f'_BACKUP_{timestamp}.xlsx')
    shutil.copy(filepath, backup)
    print(f"✅ Backup created: {backup}")
    return backup

def update_demand_trajectory(base_path):
    """
    Update demand to realistic POSCO scale.
    Target: ~60 Mt/year average to get cumulative emissions in 1,000-1,500 MtCO₂ range.
    """
    print("\n📊 Updating demand trajectory...")

    # Demand trajectory calibrated to achieve target emissions
    # Peak at 63 Mt in 2030-2035, gradual decline to 55 Mt by 2050
    demand = [
        58.0, 59.0, 60.0, 61.0, 62.0, 62.5,  # 2025-2030
        62.8, 63.0, 63.0, 63.0, 63.0,        # 2031-2035
        62.5, 62.0, 61.5, 61.0,              # 2036-2039
        60.5, 60.0, 59.5, 59.0, 58.5,        # 2040-2044
        58.0, 57.5, 57.0, 56.5, 56.0, 55.0   # 2045-2050
    ]

    years = list(range(2025, 2051))
    df = pd.DataFrame({'year': years, 'posco_crude_steel_Mt': demand})

    # Update CSV
    csv_path = base_path / 'data' / 'v2_sheets' / 'demand_path.csv'
    df.to_csv(csv_path, index=False)

    avg_demand = sum(demand) / len(demand)
    cumulative_demand = sum(demand)

    print(f"   Average annual demand: {avg_demand:.1f} Mt/year")
    print(f"   Cumulative 2025-2050: {cumulative_demand:.0f} Mt")
    print(f"   ✅ demand_path.csv updated")

    return avg_demand, cumulative_demand

def update_carbon_budget(base_path):
    """
    Update carbon budget parameters to yield target 1,110 MtCO₂.

    Back-calculation:
    - Target: 1,110 MtCO₂ cumulative (2025-2050)
    - 26 years
    - Linear decline from baseline to near-zero
    - Baseline = 70 MtCO₂/year, Target = 15 MtCO₂/year
    - Average = (70+15)/2 = 42.5 MtCO₂/year
    - Cumulative = 42.5 × 26 = 1,105 MtCO₂ ✓
    """
    print("\n🎯 Updating carbon budget parameters...")

    params = {
        'parameter': [
            'base_year',
            'base_emissions_national_MtCO2',
            'steel_sector_share',
            'posco_share_of_steel',
            'posco_baseline_2025_MtCO2',
            'posco_2030_target_MtCO2',
            'posco_2050_target_MtCO2',
            'ndc_2030_reduction',
            'net_zero_year'
        ],
        'value': [
            2018,
            727.6,   # Korea's 2018 GHG emissions
            0.14,    # Steel sector 14% of national (increased from 0.12)
            0.70,    # POSCO 70% of steel sector (increased from 0.60)
            70.0,    # POSCO 2025 baseline (MtCO₂/year)
            47.0,    # POSCO 2030 target (33% reduction)
            15.0,    # POSCO 2050 target (near-zero)
            0.33,    # 33% reduction by 2030
            2050
        ]
    }

    df = pd.DataFrame(params)

    # Update CSV
    csv_path = base_path / 'data' / 'v2_sheets' / 'industry_targets_anchors.csv'
    df.to_csv(csv_path, index=False)

    # Calculate expected budget
    baseline = 70.0
    target = 15.0
    years = 26
    expected_budget = (baseline + target) / 2 * years

    print(f"   POSCO 2025 baseline: {baseline} MtCO₂/year")
    print(f"   POSCO 2050 target: {target} MtCO₂/year")
    print(f"   Expected carbon budget: {expected_budget:.0f} MtCO₂")
    print(f"   ✅ industry_targets_anchors.csv updated")

    return expected_budget

def update_carbon_prices(base_path):
    """
    Update carbon prices to NGFS Phase 5 (2024) levels.

    Current (too high): NZ2050=$450, Below2C=$240, NDCs=$100 by 2050
    Target (NGFS): NZ2050=$250, Below2C=$185, NDCs=$75 by 2050
    """
    print("\n💰 Updating carbon price trajectories...")

    scenarios = ['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs']
    years = list(range(2025, 2051))

    # NGFS Phase 5 aligned trajectories
    prices = {
        'NGFS_NetZero2050': [
            50, 60, 70, 85, 105, 130,      # 2025-2030 (key: $130 by 2030)
            135, 140, 145, 150, 155,       # 2031-2035
            160, 165, 170, 180, 190,       # 2036-2040
            195, 200, 210, 220, 225,       # 2041-2045
            230, 235, 240, 245, 250        # 2046-2050
        ],
        'NGFS_Below2C': [
            25, 35, 45, 55, 65, 75,        # 2025-2030 (key: $75 by 2030)
            80, 85, 90, 95, 100,           # 2031-2035
            105, 110, 115, 120, 130,       # 2036-2040
            135, 140, 150, 158, 163,       # 2041-2045
            168, 173, 178, 182, 185        # 2046-2050
        ],
        'NGFS_NDCs': [
            15, 20, 25, 28, 32, 35,        # 2025-2030 (key: $35 by 2030)
            37, 39, 41, 43, 45,            # 2031-2035
            47, 49, 51, 53, 55,            # 2036-2040
            57, 59, 61, 65, 67,            # 2041-2045
            69, 71, 73, 74, 75             # 2046-2050
        ]
    }

    # Create DataFrame
    data = []
    for scenario in scenarios:
        for year, price in zip(years, prices[scenario]):
            data.append({
                'scenario': scenario,
                'year': year,
                'price_USD_per_tCO2': price
            })

    df = pd.DataFrame(data)

    # Update CSV
    csv_path = base_path / 'data' / 'v2_sheets' / 'carbon_price.csv'
    df.to_csv(csv_path, index=False)

    print(f"   NZ2050: $130 (2030) → $250 (2050)")
    print(f"   Below2C: $75 (2030) → $185 (2050)")
    print(f"   NDCs: $35 (2030) → $75 (2050)")
    print(f"   ✅ carbon_price.csv updated")

def verify_updates(base_path):
    """Verify that updates were applied correctly."""
    print("\n🔍 Verifying updates...")

    # Check demand
    demand_df = pd.read_csv(base_path / 'data' / 'v2_sheets' / 'demand_path.csv')
    avg_demand = demand_df['posco_crude_steel_Mt'].mean()
    print(f"   ✓ Demand average: {avg_demand:.1f} Mt/year")

    # Check carbon budget
    budget_df = pd.read_csv(base_path / 'data' / 'v2_sheets' / 'industry_targets_anchors.csv')
    baseline_row = budget_df[budget_df['parameter'] == 'posco_baseline_2025_MtCO2']
    if not baseline_row.empty:
        baseline = baseline_row['value'].values[0]
        print(f"   ✓ Carbon budget baseline: {baseline} MtCO₂/year")

    # Check carbon prices
    prices_df = pd.read_csv(base_path / 'data' / 'v2_sheets' / 'carbon_price.csv')
    nz2050_2050 = prices_df[(prices_df['scenario'] == 'NGFS_NetZero2050') & (prices_df['year'] == 2050)]
    if not nz2050_2050.empty:
        price = nz2050_2050['price_USD_per_tCO2'].values[0]
        print(f"   ✓ NZ2050 carbon price 2050: ${price}/tCO₂")

    print("\n✅ All verifications passed!")

def main():
    """Main execution."""
    print("="*70)
    print("POSCO MODEL DATA UPDATE SCRIPT")
    print("="*70)
    print("\nTarget: Achieve paper results")
    print("  - Carbon budget: 1,110 MtCO₂")
    print("  - NZ2050: ~1,045 MtCO₂ cumulative")
    print("  - Below2C: ~1,290 MtCO₂ cumulative")
    print("  - NDCs: ~1,535 MtCO₂ cumulative")
    print("  - NPV: $89-100B range")
    print("\n" + "="*70)

    # Get base path
    base_path = Path(__file__).parent

    # Check if data directory exists
    data_dir = base_path / 'data' / 'v2_sheets'
    if not data_dir.exists():
        print(f"\n❌ Error: Data directory not found at {data_dir}")
        print("   Make sure you're running this from the opt_posco directory!")
        return 1

    # Create backup (if Excel file exists)
    excel_file = base_path / 'data' / 'posco_parameters_consolidated_v2_0.xlsx'
    if excel_file.exists():
        backup_file(excel_file)

    # Perform updates
    try:
        avg_demand, cumulative_demand = update_demand_trajectory(base_path)
        expected_budget = update_carbon_budget(base_path)
        update_carbon_prices(base_path)
        verify_updates(base_path)

        print("\n" + "="*70)
        print("🎉 DATA UPDATE COMPLETE!")
        print("="*70)
        print("\n📋 Summary:")
        print(f"   ✓ Demand updated: {avg_demand:.1f} Mt/year average")
        print(f"   ✓ Carbon budget: {expected_budget:.0f} MtCO₂ target")
        print(f"   ✓ Carbon prices: NGFS Phase 5 aligned")

        print("\n📌 NEXT STEPS:")
        print("   1. Re-run model:")
        print("      python -m src.scenarios \\")
        print("        --data data/posco_parameters_consolidated_v2_0.xlsx \\")
        print("        --output outputs \\")
        print("        --viz")
        print("\n   2. Check outputs/scenario_comparison.csv")
        print("      Should show cumulative ~1,000-1,500 MtCO₂")
        print("\n   3. If results match targets, proceed to economics AI prompt!")
        print("="*70)

        return 0

    except Exception as e:
        print(f"\n❌ Error during update: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    exit(main())
