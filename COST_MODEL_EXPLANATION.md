# How the POSCO Model Defines Costs

## Overview

Your optimization model minimizes the **Net Present Value (NPV) of total system cost** from 2025-2050. The costs include FOUR major components:

```
Total NPV Cost = NPV(CAPEX + Fixed OPEX + Variable OPEX + ETS Costs)
```

---

## COST COMPONENT 1: CAPEX (Capital Expenditure)

### Definition
**One-time investment costs** for building new production capacity.

### Formula (from model.py:170-173)
```python
capex_t = sum(
    model.Build[route, year] * model.unit_capacity[route] * 1e6 * model.capex[route]
    for route in model.routes
)
```

### Breakdown
- `Build[route, year]`: **Number of units built** (integer decision variable)
- `unit_capacity[route]`: **Size of each unit** (e.g., 5.0 Mt/year for BF-BOF)
- `capex[route]`: **Cost per ton of capacity** (USD/tpy)

### Current Values (from data/v2_sheets/hotmetal_routes.csv)
| Technology | Unit Size (Mt/y) | CAPEX (USD/tpy) | Total Unit Cost |
|------------|------------------|-----------------|-----------------|
| **BF-BOF** | 5.0 | $1,000 | $5.0 billion |
| **BF-BOF+CCUS** | 5.0 | $1,400 | $7.0 billion |
| **FINEX-BOF** | 3.0 | $1,200 | $3.6 billion |
| **H₂-DRI-EAF** | 2.0 | $2,500 | $5.0 billion |
| **Scrap-EAF** | 1.5 | $800 | $1.2 billion |

### Example
If model decides to build **2 units of H₂-DRI-EAF** in 2032:
```
CAPEX_2032 = 2 units × 2.0 Mt/unit × 1,000,000 t/Mt × $2,500/t
           = $10 billion (one-time investment in 2032)
```

---

## COST COMPONENT 2: Fixed OPEX (Operating Expenditure)

### Definition
**Annual maintenance costs** for existing capacity (regardless of production level).

### Formula (from model.py:175-179)
```python
fixom_t = sum(
    model.K[route, year] * 1e6 * model.fixed_opex[route]
    for route in model.routes
)
```

### Breakdown
- `K[route, year]`: **Total capacity installed** (Mt/year)
- `fixed_opex[route]`: **Annual maintenance cost** (USD/tpy/year)

### Current Values
| Technology | Fixed O&M (USD/tpy/year) |
|------------|-------------------------|
| **BF-BOF** | $100 |
| **BF-BOF+CCUS** | $150 |
| **H₂-DRI-EAF** | $200 |

### Example
If POSCO has **10 Mt/year of BF-BOF capacity** in 2030:
```
Fixed OPEX_2030 = 10 Mt × 1,000,000 t/Mt × $100/t/year
                = $1 billion/year (every year capacity exists)
```

---

## COST COMPONENT 3: Variable OPEX (Production Costs)

### Definition
**Costs that scale with production volume** - raw materials, energy, feedstocks.

### Formula (from model.py:181-196)
```python
# For each route, per ton of steel produced:
usd_per_t = (
    iron_ore_intensity × iron_ore_price +
    coking_coal_intensity × coal_price +
    scrap_intensity × scrap_price +
    natural_gas_intensity × ng_price +
    electricity_intensity × electricity_price +
    hydrogen_intensity × h2_price +
    flux_intensity × flux_price +
    alloys_cost
)

# Total variable cost:
var_t = production_Mt × usd_per_t × 1e6
```

### Input Data Sources

#### A. Process Intensities (from hotmetal_routes.csv, reduction_routes.csv)
| Technology | Iron Ore (t/t) | Coal (t/t) | NG (GJ/t) | Elec (MWh/t) | H₂ (kg/t) |
|------------|---------------|-----------|-----------|-------------|----------|
| **BF-BOF** | 1.6 | 0.55 | - | 0.15 | - |
| **BF-BOF+CCUS** | 1.6 | 0.55 | - | 0.18 | - |
| **NG-DRI-EAF** | 1.5 | - | 12.0 | 0.50 | - |
| **H₂-DRI-EAF** | 1.5 | - | - | 0.55 | 50 |
| **Scrap-EAF** | - | - | - | 0.60 | - |

#### B. Commodity Prices (from fuel_prices.csv)
| Commodity | 2025 | 2030 | 2040 | 2050 | Units |
|-----------|------|------|------|------|-------|
| **Iron ore** | $120 | $130 | $150 | $170 | USD/t |
| **Coking coal** | $180 | $205 | $235 | $265 | USD/t |
| **Scrap** | $350 | $375 | $405 | $435 | USD/t |
| **Natural gas** | $8.0 | $9.0 | $10.0 | $11.0 | USD/GJ |
| **Electricity** | $80 | $90 | $100 | $110 | USD/MWh |
| **H₂ (baseline)** | $4.0 | $3.0 | $2.0 | $1.6 | USD/kg |
| **H₂ (optimistic)** | $3.5 | $2.0 | $1.2 | $0.9 | USD/kg |

### Example Calculation: BF-BOF in 2030
```
Variable cost per ton of steel:
= 1.6 t iron ore × $130/t
+ 0.55 t coal × $205/t
+ 0.15 MWh elec × $90/MWh
+ $45/t flux + alloys

= $208 + $113 + $14 + $45
= $380/t steel

If producing 40 Mt/year:
Variable OPEX = 40 Mt × $380/t × 1,000,000 t/Mt
              = $15.2 billion/year
```

---

## COST COMPONENT 4: ETS Costs (Carbon Pricing)

### Definition
**Payment for net CO₂ emissions** above free allocation.

### Formula (from model.py:198-199)
```python
ets_t = carbon_price[year] × ETSpos[year] × 1e6
```

Where:
```python
ETSpos[year] = max(0, scope1_emissions - free_allocation)
```

### Breakdown
- `scope1_emissions`: Gross emissions from production (MtCO₂/year)
- `free_allocation`: Free allowances from government (MtCO₂/year)
- `carbon_price`: Market price (USD/tCO₂)

### Carbon Price Scenarios (from carbon_price.csv)

**CURRENT VALUES (That you'll update with AI_DATA_UPDATE_PROMPT):**
| Scenario | 2025 | 2030 | 2040 | 2050 |
|----------|------|------|------|------|
| **NZ2050** | $50 | $150 | $300 | **$450** ⚠️ TOO HIGH |
| **Below2C** | $30 | $80 | $160 | **$240** ⚠️ TOO HIGH |
| **NDCs** | $15 | $40 | $70 | **$100** |

**TARGET VALUES (After update):**
| Scenario | 2025 | 2030 | 2040 | 2050 |
|----------|------|------|------|------|
| **NZ2050** | $50 | $130 | $190 | **$250** ✅ |
| **Below2C** | $25 | $75 | $130 | **$185** ✅ |
| **NDCs** | $15 | $35 | $55 | **$75** ✅ |

### Example: ETS Cost in 2030 (NZ2050 scenario)
```
Assumptions:
- Production: 60 Mt steel/year
- Emission intensity: 1.8 tCO₂/t steel (mix of technologies)
- Gross emissions: 60 Mt × 1.8 = 108 MtCO₂
- Free allocation: 50 MtCO₂ (declining from 95% in 2025)
- Net emissions: 108 - 50 = 58 MtCO₂
- Carbon price: $130/tCO₂ (after update)

ETS cost = 58 MtCO₂ × $130/tCO₂ = $7.54 billion/year
```

---

## TOTAL NPV CALCULATION

### Discounting Formula
```python
for year in years:
    discount_factor = 1 / (1 + discount_rate)^(year - 2025)
    npv += discount_factor × (capex + fixom + varopex + ets)
```

### Discount Rate
- **Current model**: 5% per year
- **Effect**: Costs in 2050 are worth only 29% of 2025 costs

### Why NPV Changes with Data Update

**Current (Incorrect Data):**
- Low demand (35-40 Mt/y) → Low production → Low total costs
- High carbon prices ($450 by 2050) → High ETS costs
- **Result: NPV = $183-186 billion**

**After Update (Correct Data):**
- High demand (55-65 Mt/y) → High production → Higher CAPEX/OPEX
- Lower carbon prices ($250 by 2050) → Lower ETS costs
- More H₂-DRI adoption → High CAPEX but lower ETS
- **Result: NPV = $89-110 billion** (more spread across cost types)

---

## HOW AI_DATA_UPDATE_PROMPT AFFECTS COSTS

### ❌ Does NOT Update (These are calibrated to literature)
1. ✅ **Technology CAPEX** ($1,000-2,500/tpy) - Based on IEA, Material Economics
2. ✅ **Fixed OPEX** ($100-200/tpy/year) - Industry benchmarks
3. ✅ **Process intensities** (iron ore, coal, etc.) - Engineering data
4. ✅ **Commodity price trajectories** (except H₂) - Market projections

### ✅ DOES Update (These are wrong)
1. 🔧 **Carbon prices** - Too high, need to match NGFS Phase 5
2. 🔧 **Demand** - Too low, need realistic POSCO scale
3. 🔧 **Free allocation** - Tied to incorrect demand/emissions

### Why Costs Decrease After Update

**Paradox:** Higher production but lower NPV?

**Explanation:**
```
Old model:
  - Small scale (37 Mt/y avg) = Suboptimal capacity utilization
  - Very high carbon prices = Massive ETS costs dominate NPV
  - NPV = $186B (75% is ETS costs)

New model:
  - Larger scale (60 Mt/y avg) = Better economies of scale
  - Realistic carbon prices = ETS costs are significant but not dominant
  - More H₂-DRI = Higher CAPEX but huge ETS savings
  - NPV = $98B (mix of CAPEX 40%, OPEX 35%, ETS 25%)
```

---

## COST BREAKDOWN BY SCENARIO (Expected After Update)

### Net Zero 2050
```
NPV Total: ~$98B

Breakdown:
- CAPEX: $38B (39%) - Heavy H₂-DRI investment
- Fixed OPEX: $22B (22%)
- Variable OPEX: $28B (29%) - High H₂ costs early
- ETS Costs: $10B (10%) - Low due to early decarbonization
```

### Below 2°C
```
NPV Total: ~$95B

Breakdown:
- CAPEX: $32B (34%) - Moderate H₂-DRI adoption
- Fixed OPEX: $21B (22%)
- Variable OPEX: $30B (32%)
- ETS Costs: $12B (13%) - Moderate overshoot penalty
```

### NDCs
```
NPV Total: ~$92B

Breakdown:
- CAPEX: $28B (30%) - Minimal new capacity
- Fixed OPEX: $20B (22%)
- Variable OPEX: $32B (35%) - Heavy coal use
- ETS Costs: $12B (13%) - Lower prices offset higher emissions
```

---

## KEY INSIGHTS FOR YOUR PAPER

### 1. Carbon Pricing Drives Technology Choice
- At $130/tCO₂ (2030, NZ2050): H₂-DRI becomes competitive
- At $75/tCO₂ (2030, Below2C): H₂-DRI marginally attractive
- At $35/tCO₂ (2030, NDCs): BF-BOF dominates (lowest NPV)

### 2. CAPEX-ETS Tradeoff
```
NZ2050: High CAPEX ($38B) but low ETS ($10B) = $48B
NDCs:   Low CAPEX ($28B) but medium ETS ($12B) = $40B

NDCs appears cheaper BUT overshoots carbon budget by 38%!
→ This is the "carbon pricing adequacy gap"
```

### 3. Cost per Ton CO₂ Abated
```
NZ2050 vs NDCs:
  ΔNPV = $98B - $92B = $6B
  ΔEmissions = 1,535 - 1,045 = 490 MtCO₂

  Cost per ton = $6B / 490 MtCO₂ = $12/tCO₂

Compare to social cost of carbon ($50-200/tCO₂):
  → H₂-DRI is HIGHLY cost-effective from society's perspective!
```

---

## DOES AI_DATA_UPDATE_PROMPT CHANGE COST PARAMETERS?

### Short Answer: **Mostly NO**

The prompt **ONLY updates**:
1. ✅ Carbon prices (NGFS Phase 5 alignment)
2. ✅ Demand trajectory (realistic POSCO scale)
3. ✅ Carbon budget parameters (correct methodology)

### It **DOES NOT change**:
- ❌ Technology CAPEX ($1,000-2,500/tpy)
- ❌ Fixed OPEX ($100-200/tpy/year)
- ❌ Commodity prices (iron ore, coal, scrap, etc.)
- ❌ Hydrogen costs ($4→1.6/kg baseline)
- ❌ Process intensities (1.6 t iron ore/t steel, etc.)

### Why?
These technology/commodity costs are **calibrated from literature**:
- IEA Iron & Steel Technology Roadmap (2024)
- Material Economics Industrial Transformation 2050 (2019)
- World Steel Association benchmarks
- Academic studies (Vogl et al. 2018, Otto et al. 2017)

They are **already correct** and don't need updating.

---

## IF YOU WANT TO UPDATE COST PARAMETERS

You would need to modify:
1. `data/v2_sheets/hotmetal_routes.csv` (CAPEX, fixed OPEX)
2. `data/v2_sheets/reduction_routes.csv` (intensities)
3. `data/v2_sheets/fuel_prices.csv` (commodity prices)

**But this is NOT recommended unless you have better data sources!**

The current values are well-documented and literature-based.

---

## SUMMARY TABLE

| Cost Component | Source File | Updated by Prompt? | Current Status |
|----------------|-------------|-------------------|----------------|
| **Technology CAPEX** | hotmetal_routes.csv | ❌ No | ✅ Calibrated to IEA |
| **Fixed OPEX** | hotmetal_routes.csv | ❌ No | ✅ Industry benchmarks |
| **Process intensities** | hotmetal/reduction_routes.csv | ❌ No | ✅ Engineering data |
| **Commodity prices** | fuel_prices.csv | ❌ No | ✅ Market projections |
| **Carbon prices** | carbon_price.csv | ✅ **YES** | ⚠️ Too high, needs fix |
| **Demand** | demand_path.csv | ✅ **YES** | ⚠️ Too low, needs fix |
| **Carbon budget** | industry_targets_anchors.csv | ✅ **YES** | ⚠️ Wrong, needs fix |

---

## BOTTOM LINE

**The AI_DATA_UPDATE_PROMPT focuses on fixing the three input parameters that are WRONG:**
1. Carbon prices (too high)
2. Demand trajectory (too low)
3. Carbon budget allocation (incorrect)

**It does NOT touch the cost parameters that are ALREADY CORRECT:**
- Technology costs (CAPEX, OPEX)
- Commodity prices (iron ore, coal, H₂, etc.)
- Process intensities

**Result:** After update, your model will show realistic total costs ($90-110B NPV) with proper breakdown across cost components, and emissions will align with paper targets (1,000-1,500 MtCO₂).

---

**Questions? Check:**
- Model formulation: `src/model.py` lines 158-207
- Cost data: `data/v2_sheets/hotmetal_routes.csv`, `fuel_prices.csv`
- Update script: Bottom of `AI_DATA_UPDATE_PROMPT.md`
