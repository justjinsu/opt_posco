# POSCO v2.0 Decarbonization Optimization Model

A comprehensive optimization framework for POSCO's steel decarbonization pathways with separated technology modules, multi-scenario analysis, and detailed cost-benefit assessment.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Data Structure](#data-structure)
- [Model Formulation](#model-formulation)
- [Output Files](#output-files)
- [Visualization](#visualization)
- [Technical Details](#technical-details)
- [Contributing](#contributing)

## Overview

The POSCO v2.0 model optimizes steel production technology mix and investment pathways to minimize total system cost while meeting decarbonization targets. The model features:

- **Separated Technology Modules**: Distinct modeling of reduction routes (NG-DRI-dom, H2-DRI-dom) and melting processes (EAF)
- **Imported HBI Option**: Modeling of imported Hot Briquetted Iron with zero domestic Scope 1 emissions
- **Metallics Balance & Quality Constraints**: Detailed metallics flow modeling with quality requirements
- **Consistent ETS Accounting**: Emissions Trading System cost calculation with free allocation
- **Multi-Scenario Analysis**: Automated execution across three carbon pricing scenarios

### Carbon Scenarios

1. **NGFS_NetZero2050**: Net zero by 2050 pathway with aggressive carbon pricing
2. **NGFS_Below2C**: Below 2°C pathway with moderate carbon pricing escalation  
3. **NGFS_NDCs**: Nationally Determined Contributions pathway with gradual carbon pricing

## Key Features

### Technology Separation
- **Hotmetal Routes**: BF-BOF, FINEX-BOF, BF-BOF+CCUS
- **Reduction Routes**: NG-DRI-dom (domestic natural gas), H2-DRI-dom (domestic hydrogen)
- **HBI Import**: Imported metallics with freight costs, no domestic emissions
- **EAF Melting**: Single downstream module consuming scrap, HBI, and domestic reduction products

### Advanced Constraints
- **Metallics Balance**: `EAF_output = yield × (scrap + HBI + domestic_reduction)`
- **Quality Constraint**: `(HBI + domestic_reduction) ≥ α_min × total_metallics`
- **Resource Limits**: Scrap supply, HBI import capacity, DR-grade ore availability
- **Capacity Utilization**: Maximum 90% utilization across all technologies

### Economic Modeling
- **NPV Optimization**: Discounted total system cost minimization
- **Detailed Cost Breakdown**: CAPEX, fixed O&M, variable O&M, and ETS costs by module
- **ETS Logic**: `ETS_cost = max(0, Scope1_emissions - free_allocation) × carbon_price`
- **Price Trajectories**: Dynamic fuel, electricity, hydrogen, and carbon pricing

## Architecture

```
posco-opt/
├── data/
│   ├── v2_sheets/              # Individual CSV parameter sheets
│   └── posco_parameters_consolidated_v2_0.xlsx  # Consolidated data file
├── src/
│   ├── io_v2.py               # Data loading and validation
│   ├── model_v2.py            # Optimization model with Pyomo
│   ├── export_v2.py           # Results export and reporting
│   ├── sanity_v2.py           # Solution validation and checks
│   ├── scenarios.py           # Multi-scenario runner
│   ├── viz.py                 # Visualization and plotting
│   └── run.py                 # CLI interface
├── outputs/                   # Generated results and plots
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites
- Python 3.8+
- GLPK solver (or CBC, Gurobi)
- Git

### Setup

```bash
# Clone repository
git clone <repository-url>
cd posco-opt

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install GLPK solver (Ubuntu/Debian)
sudo apt-get install glpk-utils

# Install GLPK solver (macOS)
brew install glpk

# Install GLPK solver (Windows)
# Download from https://sourceforge.net/projects/winglpk/
```

### Verify Installation

```bash
# Test model building
python src/run.py --data data/posco_parameters_consolidated_v2_0.xlsx --scenario NGFS_NetZero2050

# Should output model statistics without errors
```

## Quick Start

### Single Scenario Run

```bash
# Run NetZero2050 scenario with optimization and visualization
python src/run.py \
  --data data/posco_parameters_consolidated_v2_0.xlsx \
  --scenario NGFS_NetZero2050 \
  --solve \
  --viz
```

### Multi-Scenario Analysis

```bash
# Run all three carbon scenarios
python src/run.py \
  --data data/posco_parameters_consolidated_v2_0.xlsx \
  --multi-scenario \
  --solve \
  --viz

# Results in outputs/series_all_scenarios.csv
```

### Build Model Only (No Solving)

```bash
# Test model formulation without optimization
python src/run.py \
  --data data/posco_parameters_consolidated_v2_0.xlsx \
  --scenario NGFS_Below2C
```

## Usage Examples

### CLI Options

```bash
python src/run.py [OPTIONS]

Required:
  --data FILE                  Excel data file with v2.0 parameter sheets

Scenario Selection:
  --scenario {NGFS_NetZero2050,NGFS_Below2C,NGFS_NDCs}  Single scenario
  --multi-scenario             Run all three scenarios

Model Options:
  --h2-case {baseline,optimistic}     Hydrogen price case (default: baseline)
  --grid-case {base,fast,slow}        Grid carbon intensity (default: base)
  --discount FLOAT                    Annual discount rate (default: 0.05)
  --util FLOAT                        Max capacity utilization (default: 0.90)

Execution:
  --solve                             Solve optimization model
  --solver {glpk,cbc,gurobi}         Optimization solver (default: glpk)

Output:
  --output DIR                        Output directory (default: outputs)
  --viz                              Generate visualization plots
  --validate                         Run solution validation checks
  --log-level {DEBUG,INFO,WARNING,ERROR}  Logging level (default: INFO)
```

### Advanced Examples

```bash
# High discount rate analysis
python src/run.py --data data/posco_parameters_consolidated_v2_0.xlsx \
  --scenario NGFS_NetZero2050 --solve --discount 0.10

# Optimistic hydrogen pricing
python src/run.py --data data/posco_parameters_consolidated_v2_0.xlsx \
  --multi-scenario --solve --h2-case optimistic --viz

# Custom output directory with detailed logging
python src/run.py --data data/posco_parameters_consolidated_v2_0.xlsx \
  --scenario NGFS_Below2C --solve --output results_custom --log-level DEBUG
```

## Data Structure

### Excel File Structure

The consolidated Excel file (`posco_parameters_consolidated_v2_0.xlsx`) contains 12 sheets:

1. **hotmetal_routes**: BF-BOF, FINEX-BOF, BF-BOF+CCUS parameters
2. **reduction_routes**: NG-DRI-dom, H2-DRI-dom, HBI-import parameters  
3. **melting_EAF**: Electric Arc Furnace parameters
4. **metallics_balance**: Scrap supply, HBI capacity, quality constraints
5. **hbi_price**: HBI pricing by production route and freight costs
6. **fuel_prices**: Iron ore, coal, natural gas, electricity, hydrogen prices
7. **grid_CI**: Grid carbon intensity by case
8. **carbon_price**: Carbon pricing trajectories by scenario
9. **industry_targets_anchors**: Industry emission caps and targets
10. **demand_path**: POSCO crude steel demand projection
11. **free_alloc_params**: ETS free allocation parameters
12. **ccus_params**: Carbon capture utilization & storage parameters

### Units Convention

- **Production/Capacity**: Mt/year (million tonnes per year)
- **Costs**: USD/tpy (per tonne per year capacity), USD/t (per tonne product)
- **Emission Factors**: tCO2/t (tonnes CO2 per tonne product)
- **Material Intensities**: t/t, GJ/t, MWh/t, kg/t (per tonne product)
- **Prices**: USD/t, USD/GJ, USD/MWh, USD/kg

## Model Formulation

### Objective Function

```
minimize: NPV = Σ_t discount_factor_t × (CAPEX_t + FixedOM_t + VariableOM_t + ETS_cost_t)
```

### Key Constraints

**Demand Balance:**
```
Σ_r Q_hotmetal[r,t] + Q_EAF[t] = demand[t]  ∀t
```

**Metallics Balance:**
```
Q_EAF[t] = yield_EAF × (Q_scrap[t] + Q_HBI[t] + Σ_r Q_reduction[r,t])  ∀t
```

**Quality Constraint:**
```
Q_HBI[t] + Σ_r Q_reduction[r,t] ≥ α_min[t] × (Q_scrap[t] + Q_HBI[t] + Σ_r Q_reduction[r,t])  ∀t
```

**ETS Balance:**
```
ETS_positive[t] ≥ Scope1_emissions[t] - free_allocation[t]  ∀t
ETS_cost[t] = carbon_price[t] × ETS_positive[t] × 1e6
```

**Capacity Dynamics:**
```
K[r,t] = K[r,t-1] + unit_capacity[r] × Build[r,t]  ∀r,t
Q[r,t] ≤ utilization_max × K[r,t]  ∀r,t
```

## Output Files

### Detailed Results (`detailed_results_{scenario}.csv`)

Annual results with comprehensive cost breakdown:
- Production by technology route (Mt/year)
- Capacity investments and utilization
- Emissions and ETS costs
- Cost breakdown by module (CAPEX, OPEX, fuel, power, hydrogen, materials)
- Market prices and validation checks

### Summary Report (`summary_{scenario}.json`)

High-level metrics including:
- NPV total and breakdown
- Production summary (first vs last year)
- Emissions performance
- Technology mix evolution
- Route shares in final year

### Aggregated Results (`series_all_scenarios.csv`)

Combined data from all scenarios for comparative analysis.

### Scenario Comparison (`scenario_comparison.csv`)

Cross-scenario metrics for executive summary.

## Visualization

The visualization module generates 8 comprehensive plots:

1. **Emissions Pathways**: Absolute emissions and intensity by scenario
2. **Production Mix Evolution**: Stacked production by technology route
3. **Technology Transition**: Pie charts comparing first vs last year shares
4. **Carbon Pricing & ETS**: Price trajectories and annual ETS costs
5. **Cost Breakdown**: Total costs and cost intensity by scenario
6. **Metallics Composition**: EAF input mix (scrap, HBI, domestic reduction)
7. **Capacity Utilization**: Utilization rates over time
8. **Scenario Comparison Summary**: Key metrics across all scenarios

### Generating Plots

```bash
# Generate plots for existing results
python src/viz.py --output outputs

# Generate during optimization run
python src/run.py --data data/posco_parameters_consolidated_v2_0.xlsx \
  --multi-scenario --solve --viz
```

## Technical Details

### Solver Configuration

The model uses mixed-integer linear programming (MILP) with:
- **Default Solver**: GLPK (open source)
- **Alternative Solvers**: CBC (open source), Gurobi (commercial)
- **Variables**: ~1,000-5,000 depending on time horizon
- **Constraints**: ~2,000-10,000 depending on problem size

### Performance Considerations

- **Single Scenario**: 30-60 seconds on standard hardware
- **Multi-Scenario**: 2-5 minutes for all three scenarios
- **Memory Usage**: ~100-500 MB depending on problem size
- **Output Size**: ~1-10 MB per scenario

### Numerical Stability

- **Objective Scaling**: 1e-9 factor for numerical stability
- **Unit Consistency**: Mt ↔ t conversions validated
- **Tolerance Checks**: 1e-6 tolerance for constraint validation
- **ETS Precision**: Handles solver precision issues in ETS calculations

### Validation Framework

The model includes 10 comprehensive validation categories:

1. **Basic Feasibility**: Non-negativity and bounds checking
2. **Demand Satisfaction**: Production-demand balance validation
3. **Metallics Balance**: EAF input-output consistency
4. **Quality Constraints**: Metallics quality requirement verification
5. **Capacity Constraints**: Utilization limit compliance
6. **Resource Limits**: Supply constraint adherence
7. **ETS Logic**: Emissions trading cost validation
8. **Unit Consistency**: Cross-validation of unit conversions
9. **Scenario-Specific**: Technology transition reasonableness
10. **Objective Components**: Cost component additivity checks

## Contributing

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd posco-opt

# Create development environment
python -m venv venv-dev
source venv-dev/bin/activate

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8 mypy

# Run tests
pytest tests/

# Format code
black src/
flake8 src/
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Include comprehensive docstrings
- Maintain unit test coverage >80%

### Adding New Scenarios

1. Update `carbon_price` sheet in Excel data file
2. Add scenario name to CLI choices in `run.py`
3. Update scenario colors in `viz.py` if needed
4. Test with build-only mode before full optimization

### Extending Technology Routes

1. Add new route to appropriate sheet (`hotmetal_routes` or `reduction_routes`)
2. Update technology colors in `viz.py`
3. Verify constraint compatibility in `model_v2.py`
4. Run validation tests with new route

## License

This project is proprietary to POSCO and authorized users only.

## Contact

For technical support or questions:
- Primary Developer: [Contact Information]
- Project Lead: [Contact Information]
- Repository: [Repository URL]

---

**POSCO v2.0 Decarbonization Optimization Model**  
Version 2.0 | Last Updated: 2025-01-15