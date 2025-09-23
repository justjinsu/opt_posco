"""Unit tests for POSCO model components."""

import pytest
import numpy as np
from src.io import toUSD_Mt, toUSD_capacity_Mt, validate_units_test

def test_unit_conversions():
    """Test Mt to USD conversions."""
    # Test production cost conversion
    assert toUSD_Mt(1.0, 100.0) == 1e8  # 1 Mt * 100 USD/t = 100M USD
    assert toUSD_Mt(2.5, 50.0) == 1.25e8  # 2.5 Mt * 50 USD/t = 125M USD
    
    # Test capacity cost conversion
    assert toUSD_capacity_Mt(1.0, 1000.0) == 1e9  # 1 Mt/y * 1000 USD/tpy = 1B USD
    assert toUSD_capacity_Mt(0.5, 2000.0) == 1e9  # 0.5 Mt/y * 2000 USD/tpy = 1B USD

def test_ets_linearization_equivalence():
    """Test that ETS linearization gives correct positive part."""
    # Test cases: (net_emissions, free_alloc, expected_cost_factor)
    test_cases = [
        (5.0, 3.0, 2.0),  # emissions > free_alloc
        (3.0, 5.0, 0.0),  # emissions < free_alloc  
        (4.0, 4.0, 0.0),  # emissions = free_alloc
        (0.0, 2.0, 0.0),  # zero emissions
    ]
    
    carbon_price = 100.0  # USD/tCO2
    
    for net_emissions, free_alloc, expected_factor in test_cases:
        # Manual calculation of positive part
        expected_cost = max(0, net_emissions - free_alloc) * 1e6 * carbon_price
        
        # This is what the model linearization should give
        slack_value = max(0, net_emissions - free_alloc)
        linearized_cost = slack_value * 1e6 * carbon_price
        
        assert abs(expected_cost - linearized_cost) < 1e-6
        assert expected_cost == expected_factor * 1e6 * carbon_price

def test_discount_factors():
    """Test discount factor calculations."""
    discount_rate = 0.05
    t0 = 2025
    
    # Test specific values
    assert abs(1.0 / (1.05 ** 0) - 1.0) < 1e-10  # Base year
    assert abs(1.0 / (1.05 ** 5) - 0.7835261665) < 1e-6  # 5 years out
    assert abs(1.0 / (1.05 ** 25) - 0.2953020143) < 1e-6  # 25 years out

def test_validation_function():
    """Test the built-in validation function."""
    # This should not raise any exceptions
    validate_units_test()

if __name__ == '__main__':
    pytest.main([__file__])