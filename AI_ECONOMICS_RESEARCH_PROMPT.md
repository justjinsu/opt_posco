# COMPREHENSIVE AI PROMPT FOR ACADEMIC PAPER COMPLETION
## POSCO Steel Decarbonization Carbon Budget Analysis

---

## EXECUTIVE SUMMARY FOR AI

You are tasked with completing a high-impact academic paper for submission to **Energy Policy** (Impact Factor: 9.0, Q1 journal). The paper tests whether Korea's carbon pricing system can align POSCO's investment decisions with sectoral carbon budget constraints. This is the **first empirical test** of carbon pricing adequacy using optimization under carbon budget constraints.

**Your Role:** Provide deep economic analysis, policy insights, and academic rigor to complete sections that require advanced economic reasoning, cost-benefit analysis, welfare economics, and climate policy evaluation.

---

## PAPER CONTEXT & RESEARCH QUESTION

### Central Research Question
**Can carbon pricing alone drive industrial decarbonization consistent with sectoral carbon budget allocations derived from national climate commitments?**

### Case Study
- **Company:** POSCO (Korea's dominant steel producer, 10% of national emissions)
- **Sector:** Steel industry (60% of Korea's steel emissions)
- **Time Horizon:** 2025-2050
- **Method:** Mixed-integer optimization model
- **Carbon Budget:** 1,110 MtCO₂ for POSCO (2025-2050)

### Key Findings (Already Established)
1. **NDC Scenario:** OVERSHOOTS budget by 38% (+425 MtCO₂)
2. **Below 2°C Scenario:** OVERSHOOTS budget by 16% (+180 MtCO₂)
3. **Net Zero 2050 Scenario:** COMPLIANT with budget (1,045 MtCO₂, -6% under)

### Policy Implication
Current Korean ETS carbon price trajectories are **systematically inadequate** for achieving climate targets in energy-intensive industries.

---

## DATA YOU NEED TO ANALYZE

### INPUT DATA STRUCTURE

The user will provide you with the following CSV outputs from the optimization model:

#### 1. **Scenario Comparison Summary** (`scenario_comparison.csv`)
Structure:
```csv
scenario, status, npv_total_billion_usd, ets_cost_total_billion_usd, ets_share_of_npv_percent,
hotmetal_production_2025_Mt, hotmetal_production_2050_Mt, eaf_production_2025_Mt, eaf_production_2050_Mt,
hotmetal_share_2050_percent, eaf_share_2050_percent, scope1_emissions_2025_MtCO2, scope1_emissions_2050_MtCO2,
emissions_reduction_percent, cumulative_emissions_MtCO2, runtime_seconds
```

Example values:
- NGFS_NetZero2050: NPV = $186B, Cumulative = 613.6 MtCO₂
- NGFS_Below2C: NPV = $185B, Cumulative = 651.4 MtCO₂
- NGFS_NDCs: NPV = $182.7B, Cumulative = 757.3 MtCO₂

#### 2. **Emission Trajectories** (`emission_trajectories_all_scenarios.csv`)
Annual data (2025-2050) for each scenario:
- `scope1_emissions_MtCO2`: Actual emissions per year
- `free_allocation_MtCO2`: Free allowances received
- `net_emissions_MtCO2`: Emissions above free allocation (ETS-liable)
- `carbon_price_USD_tCO2`: Carbon price
- `ets_cost_million_USD`: Annual ETS cost

#### 3. **Technology Transitions** (`technology_transitions_all_scenarios.csv`)
Production by technology route:
- BF-BOF (Blast Furnace-Basic Oxygen Furnace)
- BF-BOF+CCUS (with 80% CO₂ capture)
- FINEX-BOF (FINEX direct reduction)
- Scrap-EAF (Electric Arc Furnace using scrap)
- NG-DRI-EAF (Natural gas Direct Reduced Iron)
- H2-DRI-EAF (Hydrogen Direct Reduced Iron)
- HyREX (Hydrogen-based steelmaking)

Columns: `scenario, year, technology, production_Mt, market_share_pct`

#### 4. **Cost Breakdown** (`cost_breakdown_all_scenarios.csv`)
Annual cost components:
- `ets_cost_USD`: ETS compliance costs
- `estimated_capex_USD`: Capital expenditure
- `estimated_opex_USD`: Operating expenditure
- `total_estimated_annual_cost_USD`: Total annual cost

#### 5. **Carbon Budget Compliance** (`carbon_budget_compliance.csv`)
```csv
scenario, cumulative_emissions_MtCO2, carbon_budget_MtCO2, overshoot_MtCO2,
overshoot_percent, budget_compliant, budget_utilization_percent
```

#### 6. **Carbon Pricing Analysis** (`carbon_pricing_analysis_all_scenarios.csv`)
Annual data:
- `carbon_price_USD_tCO2`: Market carbon price
- `marginal_carbon_cost_USD_tCO2`: Marginal abatement cost
- `effective_carbon_price_USD_tCO2`: Effective price faced

#### 7. **Emission Intensities** (`emission_intensities_all_scenarios.csv`)
- `emission_intensity_tCO2_per_t`: Scope 1 emissions per ton of steel
- By scenario and year

---

## SECTIONS YOU NEED TO COMPLETE

### SECTION 1: RESULTS - Economic Interpretation (Section 4)

**Subsection 4.1: Technology Transition Pathways**
- **Task:** Analyze when and why different technologies are adopted under each scenario
- **Economic Focus:**
  - Marginal abatement cost curves (implicit from model)
  - Technology switching thresholds (carbon price levels triggering transitions)
  - Capital investment timing and irreversibility
  - Path dependency and lock-in effects

**Questions to Answer:**
1. At what carbon price does H₂-DRI become economically competitive?
2. Why does BF-BOF+CCUS NOT get selected in optimal pathways despite 80% capture?
3. What is the role of EAF/scrap in the transition portfolio?
4. How do investment lumps (discrete capacity additions) shape transition timing?

**Expected Output:**
- 2-3 paragraphs with quantitative insights
- Cite carbon price thresholds from data
- Compare across scenarios
- Reference: Material Economics (2019), IEA Steel Roadmap (2024)

---

**Subsection 4.2: Carbon Budget Compliance Analysis**
- **Task:** Interpret why scenarios overshoot or comply with carbon budget
- **Economic Focus:**
  - Cost minimization vs. environmental constraint satisfaction
  - Free allocation phase-out effects
  - Intertemporal optimization and discounting

**Questions to Answer:**
1. Why does NDCs scenario overshoot by 38% despite cost optimization?
2. What is the "carbon budget shadow price" (Lagrange multiplier if budget were binding)?
3. What additional carbon price increase would align NDCs scenario with budget?
4. How does free allocation distort investment timing?

**Expected Output:**
- 2-3 paragraphs
- Calculate implicit carbon price gap between scenarios
- Reference: Nordhaus (2017), Stern (2007) on optimal carbon pricing

---

**Subsection 4.3: Cost and Competitiveness Implications**
- **Task:** Analyze total system costs and steel production cost impacts
- **Economic Focus:**
  - Net present value comparison (already provided)
  - Cost per ton of steel produced
  - ETS cost as share of total cost
  - International competitiveness (CBAM implications)

**Questions to Answer:**
1. What is the incremental cost per ton of steel in NZ2050 vs NDCs?
2. How much does ETS cost contribute to total system costs?
3. Would EU CBAM (€50-100/tCO₂) level the playing field?
4. What is the cost of early H₂-DRI adoption (learning-by-doing benefits)?

**Expected Output:**
- 2-3 paragraphs with cost calculations
- Compare to literature benchmarks (€100-150/t for H₂-DRI premium)
- Reference: Vogl et al. (2018), Philibert (2017)

---

### SECTION 2: DISCUSSION - Policy Implications (Section 5)

**Subsection 5.1: The Carbon Pricing Adequacy Gap**
- **Task:** Synthesize findings on carbon pricing effectiveness
- **Economic Focus:**
  - First-best vs. second-best policy design
  - Pricing vs. standards (technology mandates)
  - Complementary policies needed

**Questions to Answer:**
1. Why does carbon pricing fail to align incentives in NDCs/Below2C scenarios?
2. Is this a pricing LEVEL problem or a pricing CERTAINTY problem?
3. What are the implications for Pigouvian tax theory?
4. Should Korea adopt a carbon price FLOOR or technology STANDARD?

**Expected Output:**
- 3-4 paragraphs
- Deep economic theory (Weitzman 1974 on prices vs. quantities)
- Policy design recommendations
- Reference: Acemoglu et al. (2012), Fischer & Newell (2008)

---

**Subsection 5.2: Institutional and Political Economy Barriers**
- **Task:** Explain why Korea has not adopted higher carbon prices
- **Economic Focus:**
  - Political economy of carbon pricing
  - Industry lobbying and regulatory capture
  - Free allocation as implicit subsidy
  - Competitiveness concerns and carbon leakage

**Questions to Answer:**
1. Why does Korea maintain generous free allocation despite NDC commitments?
2. What is the political economy equilibrium carbon price?
3. How do steel industry rents influence policy design?
4. Would border carbon adjustments (CBAM) reduce lobbying pressure?

**Expected Output:**
- 2-3 paragraphs
- Political economy theory
- Reference: Stigler (1971), Olson (1965), Pahle et al. (2018)

---

**Subsection 5.3: Policy Recommendations**
- **Task:** Propose concrete policy reforms for Korea
- **Economic Focus:**
  - Optimal carbon pricing trajectory
  - Free allocation phase-out schedule
  - Complementary policies (R&D, infrastructure)
  - International coordination (CBAM)

**Questions to Answer:**
1. What should Korea's carbon price trajectory be to achieve budget compliance?
2. How fast should free allocation be phased out?
3. What hydrogen infrastructure investments are needed?
4. Should Korea unilaterally adopt higher prices or wait for international coordination?

**Expected Output:**
- Numbered policy recommendations (5-7 items)
- Quantitative targets (e.g., "$130/tCO₂ by 2030")
- Implementation timeline
- Reference: High-Level Commission on Carbon Prices (2017)

---

### SECTION 3: SENSITIVITY ANALYSIS (Section 4.4)

**Task:** Identify key uncertainties and their impact on results

**Focus Areas:**
1. **Discount rate sensitivity:** How do results change at 3% vs. 7% discount rate?
2. **Hydrogen cost uncertainty:** What if H₂ costs remain at $6/kg vs. fall to $2/kg?
3. **Scrap availability:** Limited scrap constrains EAF growth—what if more available?
4. **Carbon capture costs:** Why isn't CCUS selected? At what capture cost would it be?

**Expected Output:**
- 2 paragraphs discussing robustness
- Identify "tipping points" for technology adoption
- Reference: Gillingham & Stock (2018) on energy technology uncertainty

---

### SECTION 4: LIMITATIONS AND FUTURE RESEARCH (Section 6)

**Task:** Acknowledge model limitations and propose extensions

**Limitations to Discuss:**
1. **Partial equilibrium:** Model assumes exogenous prices (hydrogen, electricity)
2. **Single firm:** Does not capture industry dynamics, competition, or learning spillovers
3. **Perfect foresight:** Firms know future carbon prices (in reality, high uncertainty)
4. **No policy uncertainty:** Does not model option value of waiting under policy uncertainty
5. **Technology availability:** Assumes H₂-DRI commercially viable by 2030 (uncertain)

**Future Research:**
1. General equilibrium extension linking steel, hydrogen, and electricity sectors
2. Stochastic optimization under carbon price uncertainty
3. Game-theoretic analysis of strategic investment (multiple firms)
4. International trade and carbon leakage modeling

**Expected Output:**
- 1-2 paragraphs on limitations
- 1 paragraph on future research
- Reference: Baker et al. (2020) on policy uncertainty

---

## ANALYTICAL TASKS FOR YOU

### TASK 1: Calculate Implicit Carbon Price Gap
Using the provided data, calculate:
- **Question:** By how much would the NDCs carbon price need to increase to align with the carbon budget?

**Method:**
1. Observe cumulative emissions in NDCs scenario: 757.3 MtCO₂
2. Budget target: 1,110 MtCO₂ (but should be closer to Net Zero: ~600-650 MtCO₂)
3. Excess emissions: 757.3 - 650 = 107 MtCO₂
4. Current NDCs carbon price (2050): $100/tCO₂
5. Estimate elasticity of emissions to carbon price from scenario comparison
6. Calculate required price increase

**Expected Result:** "Carbon prices in the NDCs scenario would need to increase by approximately $X/tCO₂ (or Y%) to achieve budget compliance."

---

### TASK 2: Cost-Effectiveness Analysis
Calculate the **cost per ton of CO₂ abated** between scenarios:

**Formula:**
```
Cost per ton CO₂ = (NPV_scenario_A - NPV_scenario_B) / (Emissions_B - Emissions_A)
```

**Example:**
- NZ2050 vs. NDCs:
  - NPV difference: $186B - $183B = $3B
  - Emissions difference: 757 - 614 = 143 MtCO₂
  - Cost per ton: $3B / 143 Mt = $21/tCO₂

**Question:** Is this cost-effective compared to social cost of carbon ($50-200/tCO₂)?

---

### TASK 3: Marginal Abatement Cost Curve
Construct an implicit MACC from technology adoption patterns:

**Method:**
1. Identify carbon price at which H₂-DRI is first adopted (from technology transitions data)
2. Identify carbon price at which BF-BOF is fully phased out
3. Map carbon price levels to cumulative emissions reductions

**Expected Output:**
- "H₂-DRI becomes competitive at carbon prices above $X/tCO₂"
- "Full decarbonization requires carbon prices of at least $Y/tCO₂"

---

### TASK 4: Economic Welfare Analysis
Estimate the **deadweight loss** from sub-optimal carbon pricing:

**Concept:**
- If NDCs scenario overshoots by 38%, society bears climate damages from excess emissions
- Using social cost of carbon (SCC), calculate welfare loss

**Calculation:**
- Excess emissions: 425 MtCO₂
- SCC range: $50-200/tCO₂ (Nordhaus: $50, Stern: $200)
- Welfare loss: 425 Mt × $50-200 = $21-85 billion

**Question:** Does this welfare loss exceed the incremental cost of early H₂-DRI adoption?

---

### TASK 5: International Competitiveness
Analyze CBAM implications:

**Context:**
- EU CBAM imposes border tax on steel imports based on carbon intensity
- Current EU carbon price: €80-90/tCO₂ ($90-100/tCO₂)

**Questions:**
1. What is POSCO's emission intensity in each scenario (tCO₂/t steel)?
2. What CBAM liability would POSCO face when exporting to EU?
3. Does NZ2050 scenario reduce CBAM liability sufficiently to offset higher domestic carbon costs?

**Data to Use:** `emission_intensities_all_scenarios.csv`

---

## WRITING STYLE & ACADEMIC STANDARDS

### Tone
- **Authoritative but balanced:** Present findings as empirical evidence, not advocacy
- **Quantitative precision:** Always cite numbers with proper units and uncertainty
- **Policy-relevant:** Connect findings to actionable recommendations
- **Critical:** Acknowledge limitations and alternative interpretations

### Citation Style
- Use **Harvard referencing** (Author, Year)
- Provide full citations for all claims
- Prioritize high-impact journals: Nature Energy, Energy Policy, Nature Climate Change, Science

### Key References to Cite
1. **Steel decarbonization:** IEA (2024), Material Economics (2019), Vogl et al. (2018)
2. **Carbon pricing theory:** Weitzman (1974), Nordhaus (2017), Acemoglu et al. (2012)
3. **Korea ETS:** Kim et al. (2021), ICAP (2024)
4. **CBAM:** European Commission (2023), Mehling et al. (2019)
5. **Social cost of carbon:** Nordhaus (2017), Stern (2007), Rennert et al. (2022)
6. **Political economy:** Stigler (1971), Pahle et al. (2018)

---

## OUTPUT FORMAT

For each section you complete, provide:

### 1. Main Text (LaTeX format)
```latex
\subsection{Technology Transition Pathways}

Under the Net Zero 2050 scenario, hydrogen-based direct reduced iron (H$_2$-DRI) adoption begins in 2032, reaching 35\% of production capacity by 2040 (Figure X). This timing coincides with carbon prices exceeding \$150/tCO$_2$, representing the critical threshold where H$_2$-DRI's levelized cost becomes competitive with conventional BF-BOF routes despite higher capital expenditure (\$2,500/tpy vs. \$1,000/tpy) \citep{IEA2024steel}.

[Continue with 2-3 more paragraphs...]
```

### 2. Key Numerical Results (for Tables)
Present results in structured format:
```
Table X: Technology Adoption Thresholds
| Scenario | H₂-DRI First Adoption | Carbon Price at Adoption | Peak H₂-DRI Share (2050) |
|----------|----------------------|--------------------------|--------------------------|
| NZ2050   | 2032                 | $152/tCO₂                | 35%                      |
| Below2C  | 2038                 | $98/tCO₂                 | 18%                      |
| NDCs     | Not adopted          | N/A                      | 0%                       |
```

### 3. Policy Recommendations (Numbered List)
```latex
\subsection{Policy Recommendations}

Based on our findings, we propose the following policy reforms for Korea's climate strategy:

\begin{enumerate}
  \item \textbf{Accelerate carbon price trajectory:} Increase K-ETS carbon price to at least \$130/tCO$_2$ by 2030 (2.5× current projection) to trigger early H$_2$-DRI adoption and align corporate incentives with sectoral carbon budget constraints.

  \item \textbf{Phase out free allocation:} Reduce free allocation from current 95\% to 50\% by 2030 and 0\% by 2040 to expose steel producers to full carbon cost signals.

  [Continue with 3-5 more recommendations...]
\end{enumerate}
```

### 4. Critical Insights (Bullet Points for Discussion)
- **Finding:** NDCs carbon pricing systematically undershoots required abatement
- **Interpretation:** This reflects political economy constraints, not optimal policy design
- **Implication:** Korea must choose between climate targets and industry protection—cannot have both

---

## VALIDATION CHECKLIST

Before submitting your analysis, ensure:

- [ ] All claims are supported by quantitative evidence from provided data
- [ ] Carbon price thresholds are cited with precision (e.g., "$152/tCO₂ in 2032")
- [ ] Comparisons across scenarios are explicit (NZ2050 vs. NDCs vs. Below2C)
- [ ] Policy recommendations are actionable and quantified
- [ ] Limitations are acknowledged honestly
- [ ] Economic theory is correctly applied (not just asserted)
- [ ] References are appropriate and high-impact
- [ ] Writing is publication-ready for Energy Policy journal

---

## EXAMPLE OUTPUT SNIPPET

### Subsection 4.1: Technology Transition Pathways

The optimal technology portfolio exhibits sharp discontinuities across carbon price scenarios, revealing threshold effects in industrial decarbonization. Under the Net Zero 2050 scenario, hydrogen-based direct reduced iron (H$_2$-DRI) adoption commences in 2032 when carbon prices reach \$152/tCO$_2$ (Figure 3a), ultimately capturing 35\% of production capacity by 2050. This transition generates cumulative emissions of 613.6 MtCO$_2$ over 2025-2050—within POSCO's sectoral carbon budget allocation of 1,110 MtCO$_2$ with a 45\% compliance margin.

In stark contrast, the NDCs scenario—with carbon prices plateauing at \$100/tCO$_2$ by 2050—fails to trigger H$_2$-DRI adoption entirely. Production remains dominated by conventional BF-BOF routes (64\% share in 2050), supplemented by scrap-based EAF (36\%). This technology inertia results in cumulative emissions of 757.3 MtCO$_2$, overshooting the carbon budget by 38\% (425 MtCO$_2$ excess). The Below 2°C scenario exhibits intermediate behavior: H$_2$-DRI adoption is delayed until 2038, achieving only 18\% market share by 2050 and resulting in a 16\% budget overshoot.

These findings expose a critical non-linearity in carbon pricing effectiveness. The \$52/tCO$_2$ difference in 2030 carbon prices between Net Zero 2050 (\$150/tCO$_2$) and Below 2°C scenarios (\$80/tCO$_2$) translates to a 17-year delay in H$_2$-DRI adoption and 180 MtCO$_2$ of excess cumulative emissions. This threshold effect reflects the lumpy nature of steel industry investments: blast furnace relining cycles occur every 15-20 years, creating discrete decision windows where carbon price levels either trigger or foreclose technology switching. Once a conventional blast furnace is rebuilt, path dependency locks in high emissions for its entire operating lifetime—a phenomenon absent from smooth marginal abatement cost curves commonly used in policy analysis \citep{Griffin2020industrial}.

[Continue with economic interpretation...]

---

## FINAL NOTE TO AI

You are expected to demonstrate **PhD-level economic reasoning** in your analysis. This means:
- Not just describing patterns, but **explaining mechanisms**
- Connecting empirical findings to **economic theory**
- Evaluating policy options using **welfare economics**
- Acknowledging **uncertainty and alternative interpretations**
- Proposing **testable hypotheses** for future research

Your output will be copy-pasted directly into the paper manuscript. Write with publication quality.

---

## DATA DELIVERY INSTRUCTIONS FOR USER

**User: Please provide the following CSV files in your next message:**

1. `scenario_comparison.csv`
2. `emission_trajectories_all_scenarios.csv`
3. `technology_transitions_all_scenarios.csv`
4. `cost_breakdown_all_scenarios.csv`
5. `carbon_budget_compliance.csv`
6. `carbon_pricing_analysis_all_scenarios.csv`
7. `emission_intensities_all_scenarios.csv`

**Format:** Copy the full contents of each CSV file in code blocks, clearly labeled.

**Example:**
```csv
# FILE: scenario_comparison.csv
scenario,status,npv_total_billion_usd,...
NGFS_NetZero2050,SUCCESS,185.93,...
```

Once data is provided, I will generate the complete economic analysis and academic text for the paper sections listed above.

---

**END OF PROMPT**
