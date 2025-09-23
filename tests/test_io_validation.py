"""Tests for IO validation and error handling."""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from src.io import load_parameters, _validate_columns

def test_missing_file():
    """Test error when parameter file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_parameters('nonexistent_file.xlsx', 'NGFS_NetZero2050')

def test_validate_columns():
    """Test column validation function."""
    # Good case
    df_good = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    _validate_columns(df_good, ['col1', 'col2'], 'test_sheet')  # Should not raise
    
    # Missing column case
    df_bad = pd.DataFrame({'col1': [1, 2]})
    with pytest.raises(ValueError, match="Missing columns in sheet 'test_sheet': \['col2'\]"):
        _validate_columns(df_bad, ['col1', 'col2'], 'test_sheet')

def create_minimal_excel(filepath: str) -> None:
    """Create minimal valid Excel file for testing."""
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        
        # tech_routes sheet
        pd.DataFrame({
            'route': ['BF-BOF', 'H2-DRI'],
            'unit_capacity_Mtpy': [5.0, 2.0],
            'capex_USD_per_tpy': [1000, 3000],
            'fixed_opex_USD_per_tpy': [100, 200]
        }).to_excel(writer, sheet_name='tech_routes', index=False)
        
        # process_intensity sheet
        pd.DataFrame({
            'route': ['BF-BOF', 'H2-DRI'],
            'iron_ore_t_per_t': [1.5, 1.2],
            'coking_coal_t_per_t': [0.5, 0.0],
            'scrap_t_per_t': [0.1, 0.0],
            'ng_GJ_per_t': [2.0, 5.0],
            'electricity_MWh_per_t': [0.5, 2.0],
            'h2_kg_per_t': [0, 50],
            'fluxes_t_per_t': [0.2, 0.1],
            'alloys_USD_per_t': [50, 100]
        }).to_excel(writer, sheet_name='process_intensity', index=False)
        
        # ef_scope1 sheet
        pd.DataFrame({
            'route': ['BF-BOF', 'H2-DRI'],
            'tCO2_per_t': [2.0, 0.1]
        }).to_excel(writer, sheet_name='ef_scope1', index=False)
        
        # fuel_prices sheet
        pd.DataFrame({
            'commodity': ['iron_ore_USD_per_t', 'hydrogen_USD_per_kg_baseline'],
            '2025': [100, 5],
            '2030': [110, 4],
            '2050': [120, 3]
        }).to_excel(writer, sheet_name='fuel_prices', index=False)
        
        # grid_CI sheet
        pd.DataFrame({
            'year': [2025, 2030, 2050],
            'base_kgCO2_per_kWh': [0.5, 0.3, 0.1]
        }).to_excel(writer, sheet_name='grid_CI', index=False)
        
        # carbon_price sheet
        pd.DataFrame({
            'scenario': ['NGFS_NetZero2050', 'NGFS_NetZero2050'],
            'year': [2025, 2050],
            'price_USD_per_tCO2': [50, 200]
        }).to_excel(writer, sheet_name='carbon_price', index=False)
        
        # demand_path sheet
        pd.DataFrame({
            'year': [2025, 2030, 2050],
            'posco_crude_steel_Mt': [40, 35, 30]
        }).to_excel(writer, sheet_name='demand_path', index=False)
        
        # free_alloc_params sheet
        pd.DataFrame({
            'free_alloc_baseline_posco_2025_MtCO2': [50]
        }).to_excel(writer, sheet_name='free_alloc_params', index=False)
        
        # industry_targets_anchors sheet
        pd.DataFrame({
            'anchor_year': [2025, 2030, 2050],
            'industry_cap_MtCO2': [500, 400, 200]
        }).to_excel(writer, sheet_name='industry_targets_anchors', index=False)

def test_load_parameters_success():
    """Test successful parameter loading."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        create_minimal_excel(tmp_path)
        
        # This should work without errors
        params = load_parameters(tmp_path, 'NGFS_NetZero2050')
        
        # Basic checks
        assert 'routes' in params
        assert 'years' in params
        assert 'demand' in params
        assert len(params['routes']) == 2
        assert 'BF-BOF' in params['routes']
        assert 'H2-DRI' in params['routes']
        
        # Check price function works
        price = params['price_fn']('iron_ore_USD_per_t', 2025)
        assert price == 100
        
    finally:
        os.unlink(tmp_path)

def test_missing_sheet_error():
    """Test error when required sheet is missing."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        # Create file with only one sheet
        with pd.ExcelWriter(tmp_path, engine='openpyxl') as writer:
            pd.DataFrame({'route': ['BF-BOF']}).to_excel(writer, sheet_name='tech_routes', index=False)
        
        # Should raise error about missing sheets
        with pytest.raises(ValueError, match="Missing required sheets"):
            load_parameters(tmp_path, 'NGFS_NetZero2050')
    
    finally:
        os.unlink(tmp_path)

def test_unknown_carbon_scenario():
    """Test error when carbon scenario not found."""
    with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        create_minimal_excel(tmp_path)
        
        # Should raise error for unknown scenario
        with pytest.raises(ValueError, match="Carbon scenario 'UnknownScenario' not found"):
            load_parameters(tmp_path, 'UnknownScenario')
    
    finally:
        os.unlink(tmp_path)

if __name__ == '__main__':
    pytest.main([__file__])