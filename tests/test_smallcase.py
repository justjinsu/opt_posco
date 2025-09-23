"""Small case test with known optimal solution."""

import pytest
import pyomo.environ as pyo
from src.model import build_model

def create_toy_parameters():
    """Create minimal 2-year, 2-route test case."""
    return {
        'routes': ['BF-BOF', 'H2-DRI'],
        'years': [2025, 2026],
        't0': 2025,
        'demand': {2025: 10.0, 2026: 10.0},  # Mt
        'tech': {
            'unit_capacity': {'BF-BOF': 5.0, 'H2-DRI': 2.0},  # Mt/y per unit
            'capex': {'BF-BOF': 1000, 'H2-DRI': 3000},  # USD/tpy
            'fixed_opex': {'BF-BOF': 100, 'H2-DRI': 200}  # USD/tpy/y
        },
        'ef_scope1': {'BF-BOF': 2.0, 'H2-DRI': 0.1},  # tCO2/t
        'carbon_price': {2025: 0, 2026: 0},  # USD/tCO2 (zero to simplify)
        'free_alloc': {2025: 0, 2026: 0},  # MtCO2
        'intensity': {  # Minimal intensities
            'iron_ore_t': {'BF-BOF': 1.5, 'H2-DRI': 1.2},
            'coking_coal_t': {'BF-BOF': 0.5, 'H2-DRI': 0.0},
            'h2_kg': {'BF-BOF': 0, 'H2-DRI': 50}
        },
        'price_fn': lambda commodity, year: 100.0  # Dummy price function
    }

def test_toy_model_feasibility():
    """Test that toy model builds and has feasible solution."""
    params = create_toy_parameters()
    
    # Build model
    model = build_model(params, discount_rate=0.0, utilization=1.0)  # No discounting, full util
    
    # Check that model has expected structure
    assert len(model.routes) == 2
    assert len(model.years) == 2
    assert hasattr(model, 'Q')  # Production variables
    assert hasattr(model, 'K')  # Capacity variables
    assert hasattr(model, 'Build')  # Build variables
    
    # Try to solve (should be feasible)
    opt = pyo.SolverFactory('glpk')
    results = opt.solve(model)
    
    assert results.solver.termination_condition == pyo.TerminationCondition.optimal
    
    # Check demand satisfaction
    for year in [2025, 2026]:
        total_prod = sum(pyo.value(model.Q[r, year]) for r in model.routes)
        assert abs(total_prod - params['demand'][year]) < 1e-6

def test_carbon_price_response():
    """Test that model responds to carbon price by switching to cleaner tech."""
    params = create_toy_parameters()
    
    # Case 1: Zero carbon price - should prefer cheap BF-BOF
    params['carbon_price'] = {2025: 0, 2026: 0}
    model1 = build_model(params, discount_rate=0.0, utilization=1.0)
    opt = pyo.SolverFactory('glpk')
    opt.solve(model1)
    
    bf_prod_low = pyo.value(model1.Q['BF-BOF', 2026])
    h2_prod_low = pyo.value(model1.Q['H2-DRI', 2026])
    
    # Case 2: Very high carbon price - should prefer clean H2-DRI
    params['carbon_price'] = {2025: 1000, 2026: 1000}  # High carbon price
    model2 = build_model(params, discount_rate=0.0, utilization=1.0)
    opt.solve(model2)
    
    bf_prod_high = pyo.value(model2.Q['BF-BOF', 2026])
    h2_prod_high = pyo.value(model2.Q['H2-DRI', 2026])
    
    # With high carbon price, should use more H2-DRI, less BF-BOF
    assert h2_prod_high > h2_prod_low, f"H2 production should increase: {h2_prod_low} -> {h2_prod_high}"
    assert bf_prod_high < bf_prod_low, f"BF production should decrease: {bf_prod_low} -> {bf_prod_high}"

if __name__ == '__main__':
    pytest.main([__file__])