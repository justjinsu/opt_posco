#!/usr/bin/env python3
"""
Analyze ETS cost logic and emission factors.
"""

import pandas as pd
import sys
sys.path.append('src')
from io_v2 import load_parameters

# Load parameters
params = load_parameters('data/posco_parameters_consolidated_v2_0.xlsx', 'NGFS_NetZero2050')

print('=== HOTMETAL ROUTES EMISSIONS ===')
for route, data in params['hotmetal_routes'].items():
    print(f'{route}:')
    print(f'  Emission factor (pre-CCUS): {data["ef_scope1_pre"]:.3f} tCO2/t')
    print(f'  CCUS capture rate: {data["ccus_capture"]:.1%}')
    print(f'  Net emission factor: {data["ef_scope1_pre"] * (1.0 - data["ccus_capture"]):.3f} tCO2/t')
    print()

print('=== REDUCTION ROUTES EMISSIONS ===')
for route, data in params['reduction_routes'].items():
    if route != 'HBI-import':
        print(f'{route}:')
        print(f'  Emission factor: {data["ef_scope1_pre"]:.3f} tCO2/t')
        print()

print('=== FREE ALLOCATION vs EXPECTED EMISSIONS ===')
# Calculate expected emissions from a typical steel production scenario
typical_ef = 2.0  # Typical BF-BOF emission factor (tCO2/t steel)
years = [2025, 2030, 2040, 2050]
for year in years:
    if year in params['free_allocation'] and year in params['demand']:
        expected_emissions = params['demand'][year] * typical_ef
        free_alloc = params['free_allocation'][year]
        print(f'{year}: ')
        print(f'  Demand: {params["demand"][year]:.1f} Mt steel')
        print(f'  Expected emissions (~2.0 tCO2/t): {expected_emissions:.1f} MtCO2')
        print(f'  Free allocation: {free_alloc:.1f} MtCO2')
        print(f'  Expected ETS exposure: {max(0, expected_emissions - free_alloc):.1f} MtCO2')
        print(f'  Carbon price: ${params["carbon_prices"][year]:.0f}/tCO2')
        print()

print('=== SAMPLE CALCULATION FROM RESULTS ===')
# Look at 2025 results
print('From CSV results for 2025:')
print('  BF-BOF production: 38.2 Mt')
print('  Free allocation: 75.0 MtCO2')
print('  Scope1 emissions in CSV: (empty/NaN)')
print('  ETS cost: $0')
print()
print('Expected calculation:')
print('  BF-BOF emissions = 38.2 Mt * 2.0 tCO2/t = 76.4 MtCO2')
print('  ETS exposure = max(0, 76.4 - 75.0) = 1.4 MtCO2')
print('  ETS cost = 1.4 MtCO2 * $50/tCO2 = $70M')
print()
print('ISSUE: The scope1_emissions field is showing as empty (NaN) in results!')