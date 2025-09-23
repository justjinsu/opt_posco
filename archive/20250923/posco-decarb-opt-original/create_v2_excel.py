 #!/usr/bin/env python3
"""Create the v2.0 Excel file from CSV sheets."""

import pandas as pd
import os
from pathlib import Path

def create_v2_excel():
    """Combine CSV sheets into Excel workbook."""
    
    sheets_dir = Path("data/v2_sheets")
    output_file = Path("data/posco_parameters_consolidated_v2_0.xlsx")
    
    # Add missing sheets with sample data
    additional_sheets = {
        'grid_CI': pd.DataFrame({
            'year': [2025, 2030, 2035, 2040, 2045, 2050],
            'base_kgCO2_per_kWh': [0.45, 0.35, 0.25, 0.20, 0.15, 0.10],
            'fast_kgCO2_per_kWh': [0.30, 0.20, 0.15, 0.10, 0.08, 0.05],
            'slow_kgCO2_per_kWh': [0.50, 0.45, 0.35, 0.25, 0.20, 0.15]
        }),
        'product_shares': pd.DataFrame({
            'year': [2025, 2030, 2035, 2040, 2045, 2050],
            'flat_share': [0.6, 0.6, 0.6, 0.6, 0.6, 0.6],
            'long_share': [0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        }),
        'free_alloc_params': pd.DataFrame({
            'parameter': ['baseline_2025_factor', 'linear_decline_rate'],
            'value': [0.75, 0.02]  # 75% of industry cap in 2025, declining 2%/year
        })
    }
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Read existing CSV sheets
        for csv_file in sheets_dir.glob("*.csv"):
            sheet_name = csv_file.stem
            df = pd.read_csv(csv_file)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added sheet: {sheet_name}")
        
        # Add additional sheets
        for sheet_name, df in additional_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"Added sheet: {sheet_name}")
    
    print(f"Created Excel file: {output_file}")

if __name__ == "__main__":
    create_v2_excel()