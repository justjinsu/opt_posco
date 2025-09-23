#!/usr/bin/env python3
"""
Simple test to isolate the solver issue with POSCO v2.0 model.
"""

import sys
sys.path.append('src')

from io_v2 import load_parameters
from model_v2 import build_model, solve_model
import pyomo.environ as pyo

# Load parameters
print("Loading parameters...")
params = load_parameters('data/posco_parameters_consolidated_v2_0.xlsx', 'NGFS_NetZero2050')

# Build model
print("Building model...")
model = build_model(params, discount_rate=0.05, utilization=0.90)

print(f"Model has {len(list(model.component_objects(pyo.Var)))} variable groups")
print(f"Model has {len(list(model.component_objects(pyo.Constraint)))} constraint groups")

# Try to write LP file to inspect
print("Writing LP file for inspection...")
model.write('debug_model.lp', format='lp')
print("LP file written to debug_model.lp")

# Try different solvers
print("\nTesting different solvers...")

# Test 1: Try with HiGHS if available
try:
    opt_highs = pyo.SolverFactory('highs')
    if opt_highs.available():
        print("Trying HiGHS solver...")
        result = opt_highs.solve(model, tee=True)
        print(f"HiGHS result: {result.solver.termination_condition}")
    else:
        print("HiGHS not available")
except Exception as e:
    print(f"HiGHS failed: {e}")

# Test 2: Try with CPLEX if available  
try:
    opt_cplex = pyo.SolverFactory('cplex')
    if opt_cplex.available():
        print("Trying CPLEX solver...")
        result = opt_cplex.solve(model, tee=False)
        print(f"CPLEX result: {result.solver.termination_condition}")
    else:
        print("CPLEX not available")
except Exception as e:
    print(f"CPLEX failed: {e}")

# Test 3: Try CBC with different options
try:
    print("Trying CBC with minimal options...")
    opt_cbc = pyo.SolverFactory('cbc')
    result = opt_cbc.solve(model, tee=False, options={'sec': 60})
    print(f"CBC result: {result.solver.termination_condition}")
except Exception as e:
    print(f"CBC failed: {e}")

print("Test completed.")