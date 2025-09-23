"""
Excel data loader with validation for POSCO steel decarbonization model.

Units:
- Production: Mt (million tons)
- Capacity: Mt/y (million tons per year)  
- Costs: USD (US dollars)
- Emissions: tCO2 (tons CO2) or MtCO2 (million tons CO2)
- Energy: GJ (gigajoules), MWh (megawatt-hours)
- Materials: t (metric tons)
"""

import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Conversion factor for Mt to t
MT_TO_T = 1e6

def load_parameters(
    xlsx_path: str, 
    carbon_scenario: str,
    grid_case: str = 'base',
    hydrogen_case: str = 'baseline'
) -> Dict[str, Any]:
    """
    Load POSCO model parameters from Excel file.
    
    Args:
        xlsx_path: Path to Excel parameter file
        carbon_scenario: Carbon price scenario (e.g., 'NGFS_NetZero2050')
        grid_case: Grid carbon intensity case ('base', 'fast', 'slow')
        hydrogen_case: Hydrogen price case ('baseline', 'optimistic')
        
    Returns:
        Dictionary containing all model parameters with validated data
        
    Units in returned dict:
        - demand: Mt/year
        - tech.capex: USD/tpy (per ton per year capacity)
        - tech.fixed_opex: USD/tpy/year
        - intensity.*: physical units per t crude steel
        - ef_scope1: tCO2/t crude steel
        - price_fn: function(commodity: str, year: int) -> USD per physical unit
        - carbon_price: USD/tCO2
        - free_alloc: MtCO2/year
        - grid_ci: kgCO2/kWh
    """
    xlsx_path = Path(xlsx_path)
    if not xlsx_path.exists():
        raise FileNotFoundError(f"Parameter file not found: {xlsx_path}")
    
    logger.info(f"Loading parameters from {xlsx_path}")
    logger.info(f"Carbon scenario: {carbon_scenario}, Grid: {grid_case}, H2: {hydrogen_case}")
    
    try:
        xls = pd.ExcelFile(xlsx_path)
    except Exception as e:
        raise ValueError(f"Cannot read Excel file {xlsx_path}: {e}")
    
    # Required sheets
    required_sheets = [
        'tech_routes', 'process_intensity', 'ef_scope1', 'fuel_prices',
        'grid_CI', 'carbon_price', 'demand_path', 'free_alloc_params'
    ]
    
    # Check for missing sheets
    missing_sheets = [s for s in required_sheets if s not in xls.sheet_names]
    if missing_sheets:
        raise ValueError(f"Missing required sheets: {missing_sheets}")
    
    params = {}
    
    # Load technology routes
    logger.info("Loading technology routes")
    tech_df = pd.read_excel(xls, 'tech_routes')
    required_cols = ['route', 'unit_capacity_Mtpy', 'capex_USD_per_tpy', 'fixed_opex_USD_per_tpy']
    _validate_columns(tech_df, required_cols, 'tech_routes')
    
    params['routes'] = tech_df['route'].tolist()
    params['tech'] = {
        'unit_capacity': dict(zip(tech_df['route'], tech_df['unit_capacity_Mtpy'])),
        'capex': dict(zip(tech_df['route'], tech_df['capex_USD_per_tpy'])),
        'fixed_opex': dict(zip(tech_df['route'], tech_df['fixed_opex_USD_per_tpy']))
    }
    
    # Load process intensities
    logger.info("Loading process intensities")
    intensity_df = pd.read_excel(xls, 'process_intensity')
    intensity_cols = [
        'iron_ore_t_per_t', 'coking_coal_t_per_t', 'scrap_t_per_t',
        'ng_GJ_per_t', 'electricity_MWh_per_t', 'h2_kg_per_t',
        'fluxes_t_per_t', 'alloys_USD_per_t'
    ]
    required_intensity_cols = ['route'] + intensity_cols
    _validate_columns(intensity_df, required_intensity_cols, 'process_intensity')
    
    params['intensity'] = {}
    for col in intensity_cols:
        params['intensity'][col.replace('_per_t', '')] = dict(zip(
            intensity_df['route'], intensity_df[col]
        ))
    
    # Load emission factors
    logger.info("Loading emission factors")
    ef_df = pd.read_excel(xls, 'ef_scope1')
    _validate_columns(ef_df, ['route', 'tCO2_per_t'], 'ef_scope1')
    params['ef_scope1'] = dict(zip(ef_df['route'], ef_df['tCO2_per_t']))
    
    # Load fuel prices
    logger.info("Loading fuel prices")
    prices_df = pd.read_excel(xls, 'fuel_prices')
    params['years'] = [c for c in prices_df.columns if str(c).isdigit()]
    if not params['years']:
        raise ValueError("No year columns found in fuel_prices sheet")
    
    params['years'] = sorted([int(y) for y in params['years']])
    params['t0'] = min(params['years'])
    
    # Create price function
    price_data = {}
    for _, row in prices_df.iterrows():
        commodity = row.iloc[0]  # First column should be commodity name
        price_data[commodity] = {}
        for year in params['years']:
            if str(year) in prices_df.columns:
                price_data[commodity][year] = row[str(year)]
    
    # Handle hydrogen price case
    h2_key = f"hydrogen_USD_per_kg_{hydrogen_case}"
    if h2_key not in price_data:
        raise ValueError(f"Hydrogen price case '{hydrogen_case}' not found. Available: {list(price_data.keys())}")
    
    # Map hydrogen case to standard name
    price_data['hydrogen_USD_per_kg'] = price_data[h2_key]
    
    def price_fn(commodity: str, year: int) -> float:
        """Get price for commodity in given year (USD per physical unit)."""
        if commodity not in price_data:
            raise ValueError(f"Unknown commodity: {commodity}")
        if year not in price_data[commodity]:
            # Linear interpolation/extrapolation
            years_avail = sorted(price_data[commodity].keys())
            if year < min(years_avail):
                return price_data[commodity][min(years_avail)]
            elif year > max(years_avail):
                return price_data[commodity][max(years_avail)]
            else:
                # Linear interpolation
                y1 = max(y for y in years_avail if y <= year)
                y2 = min(y for y in years_avail if y >= year)
                if y1 == y2:
                    return price_data[commodity][y1]
                p1, p2 = price_data[commodity][y1], price_data[commodity][y2]
                return p1 + (p2 - p1) * (year - y1) / (y2 - y1)
        return price_data[commodity][year]
    
    params['price_fn'] = price_fn
    
    # Load grid carbon intensity
    logger.info("Loading grid carbon intensity")
    grid_df = pd.read_excel(xls, 'grid_CI')
    grid_col = f"{grid_case}_kgCO2_per_kWh"
    if grid_col not in grid_df.columns:
        raise ValueError(f"Grid case '{grid_case}' not found in grid_CI sheet")
    
    params['grid_ci'] = dict(zip(grid_df['year'], grid_df[grid_col]))
    
    # Load carbon price
    logger.info("Loading carbon price")
    carbon_df = pd.read_excel(xls, 'carbon_price')
    carbon_scenario_df = carbon_df[carbon_df['scenario'] == carbon_scenario]
    if carbon_scenario_df.empty:
        available = carbon_df['scenario'].unique().tolist()
        raise ValueError(f"Carbon scenario '{carbon_scenario}' not found. Available: {available}")
    
    params['carbon_price'] = dict(zip(
        carbon_scenario_df['year'], 
        carbon_scenario_df['price_USD_per_tCO2']
    ))
    
    # Load demand
    logger.info("Loading demand path")
    demand_df = pd.read_excel(xls, 'demand_path')
    _validate_columns(demand_df, ['year', 'posco_crude_steel_Mt'], 'demand_path')
    params['demand'] = dict(zip(demand_df['year'], demand_df['posco_crude_steel_Mt']))
    
    # Load and compute free allocation
    logger.info("Loading free allocation parameters")
    
    # Load baseline and industry targets
    free_params_df = pd.read_excel(xls, 'free_alloc_params')
    baseline_2025 = free_params_df.loc[0, 'free_alloc_baseline_posco_2025_MtCO2']
    
    # Load or build industry cap
    if 'industry_cap' in xls.sheet_names:
        logger.info("Using precomputed industry cap")
        industry_df = pd.read_excel(xls, 'industry_cap')
        industry_cap = dict(zip(industry_df['year'], industry_df['industry_cap_MtCO2']))
    else:
        logger.info("Building industry cap from anchors")
        anchors_df = pd.read_excel(xls, 'industry_targets_anchors')
        _validate_columns(anchors_df, ['anchor_year', 'industry_cap_MtCO2'], 'industry_targets_anchors')
        
        anchor_years = anchors_df['anchor_year'].tolist()
        anchor_caps = anchors_df['industry_cap_MtCO2'].tolist()
        
        # Linear interpolation for all years
        industry_cap = {}
        for year in params['years']:
            industry_cap[year] = np.interp(year, anchor_years, anchor_caps)
    
    # Compute free allocation linked to industry cap
    industry_cap_2025 = industry_cap.get(2025, industry_cap[min(industry_cap.keys())])
    params['free_alloc'] = {}
    for year in params['years']:
        scaling_factor = industry_cap[year] / industry_cap_2025
        params['free_alloc'][year] = baseline_2025 * scaling_factor
    
    # Load product shares if available
    if 'product_shares' in xls.sheet_names:
        logger.info("Loading product shares")
        product_df = pd.read_excel(xls, 'product_shares')
        params['product_shares'] = {
            'flat_auto_exposed': dict(zip(product_df['year'], product_df['flat_automotive_exposed_share'])),
            'flat_other': dict(zip(product_df['year'], product_df['flat_other_share'])),
            'long': dict(zip(product_df['year'], product_df['long_share']))
        }
    else:
        # Default: no product quality constraints
        params['product_shares'] = None
    
    # Store options
    params['options'] = {
        'carbon_scenario': carbon_scenario,
        'grid_case': grid_case,
        'hydrogen_case': hydrogen_case
    }
    
    # Validation
    _validate_parameters(params)
    
    logger.info(f"Loaded parameters: {len(params['routes'])} routes, {len(params['years'])} years")
    logger.info(f"Years: {params['years'][0]}-{params['years'][-1]}")
    logger.info(f"Routes: {params['routes']}")
    logger.info(f"Free allocation 2025: {params['free_alloc'].get(2025, 'N/A'):.3f} MtCO2")
    
    return params


def _validate_columns(df: pd.DataFrame, required_cols: List[str], sheet_name: str) -> None:
    """Validate that DataFrame has required columns."""
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        available = list(df.columns)
        raise ValueError(f"Missing columns in sheet '{sheet_name}': {missing}. Available: {available}")


def _validate_parameters(params: Dict[str, Any]) -> None:
    """Validate loaded parameters for consistency and sanity."""
    
    # Check for negative values where they shouldn't occur
    for route in params['routes']:
        if params['tech']['capex'][route] < 0:
            raise ValueError(f"Negative CAPEX for route {route}")
        if params['tech']['fixed_opex'][route] < 0:
            raise ValueError(f"Negative fixed OPEX for route {route}")
        if params['ef_scope1'][route] < 0:
            raise ValueError(f"Negative emission factor for route {route}")
    
    # Check price function for key commodities
    test_year = params['t0']
    key_commodities = ['iron_ore_USD_per_t', 'coking_coal_USD_per_t', 'ng_USD_per_GJ']
    for commodity in key_commodities:
        try:
            price = params['price_fn'](commodity, test_year)
            if price < 0:
                raise ValueError(f"Negative price for {commodity} in {test_year}")
        except Exception as e:
            logger.warning(f"Could not validate price for {commodity}: {e}")
    
    # Check demand coverage
    demand_years = set(params['demand'].keys())
    param_years = set(params['years'])
    if not param_years.issubset(demand_years):
        missing = param_years - demand_years
        raise ValueError(f"Demand data missing for years: {sorted(missing)}")
    
    # Check that all years have carbon prices
    carbon_years = set(params['carbon_price'].keys())
    if not param_years.issubset(carbon_years):
        missing = param_years - carbon_years
        raise ValueError(f"Carbon price data missing for years: {sorted(missing)}")
    
    logger.info("Parameter validation passed")


def toUSD_Mt(mt_quantity: float, usd_per_t: float) -> float:
    """Convert Mt quantity at USD/t price to total USD cost."""
    return mt_quantity * MT_TO_T * usd_per_t


def toUSD_capacity_Mt(mt_capacity: float, usd_per_tpy: float) -> float:
    """Convert Mt/y capacity at USD/(t/y) price to total USD cost."""
    return mt_capacity * MT_TO_T * usd_per_tpy


def validate_units_test():
    """Unit test for conversion functions."""
    # Test Mt to USD conversion
    assert toUSD_Mt(1.0, 100.0) == 1e8  # 1 Mt * 100 USD/t = 100M USD
    assert toUSD_capacity_Mt(1.0, 1000.0) == 1e9  # 1 Mt/y * 1000 USD/tpy = 1B USD
    logger.info("Unit conversion tests passed")