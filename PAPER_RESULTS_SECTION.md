# RESULTS SECTION - Complete Academic Text
## For Energy Policy Journal Submission

---

## Section 4: Results

### 4.1 Technology Transition Pathways and Carbon Price Thresholds

The optimal technology portfolio exhibits sharp discontinuities across carbon price scenarios, revealing threshold effects in industrial decarbonization (Figure 1). Under the Net Zero 2050 scenario, hydrogen-based direct reduced iron (H₂-DRI) adoption commences in 2032 when carbon prices reach approximately \$150/tCO₂, ultimately capturing 35\% of production capacity by 2050 (Table 1). This transition generates cumulative emissions of 1,045 MtCO₂ over 2025-2050—within POSCO's sectoral carbon budget allocation of 1,110 MtCO₂ with a 6\% compliance margin. The carbon price trajectory in this scenario ($130/tCO₂ by 2030, rising to $250/tCO₂ by 2050) crosses the critical threshold where H₂-DRI's levelized cost becomes competitive with conventional blast furnace-basic oxygen furnace (BF-BOF) routes despite substantially higher capital expenditure (\$2,500/tpy vs. \$1,000/tpy).

In stark contrast, the NDCs scenario—with carbon prices reaching only \$35/tCO₂ by 2030 and \$75/tCO₂ by 2050—fails to trigger H₂-DRI adoption entirely. Production remains dominated by conventional BF-BOF routes (64\% share in 2050), supplemented by scrap-based electric arc furnace (EAF) capacity (36\%) constrained by domestic scrap availability. This technology inertia results in cumulative emissions of 1,535 MtCO₂, overshooting the carbon budget by 38\% (425 MtCO₂ excess). The Below 2°C scenario exhibits intermediate behavior: carbon prices of \$75/tCO₂ by 2030 (rising to \$185/tCO₂ by 2050) delay H₂-DRI adoption until 2038, achieving only 18\% market share by 2050 and resulting in a 16\% budget overshoot (180 MtCO₂ excess, cumulative emissions 1,290 MtCO₂).

These findings expose a critical non-linearity in carbon pricing effectiveness. The \$55/tCO₂ difference in 2030 carbon prices between Net Zero 2050 (\$130/tCO₂) and Below 2°C (\$75/tCO₂) scenarios translates to a six-year delay in H₂-DRI adoption and 245 MtCO₂ of excess cumulative emissions. This threshold effect reflects the lumpy nature of steel industry investments: blast furnace relining cycles occur every 15-20 years \citep{MaterialEconomics2019}, creating discrete decision windows where carbon price levels either trigger or foreclose technology switching. Once a conventional blast furnace is rebuilt, path dependency locks in high emissions for its entire operating lifetime—a phenomenon absent from smooth marginal abatement cost curves commonly used in policy analysis \citep{Vogl2018}. The model's mixed-integer formulation captures this industrial reality, revealing that incremental carbon price increases below the switching threshold generate minimal emissions reductions, while prices exceeding \$130-150/tCO₂ by 2030 unlock rapid decarbonization through accelerated H₂-DRI deployment.

Notably, BF-BOF equipped with carbon capture and storage (CCUS, 80\% capture rate) is not selected in optimal pathways across any scenario despite substantial emission reductions per unit. At current cost assumptions (40\% CAPEX premium over conventional BF-BOF, additional operating expenditure for capture and compression), CCUS retrofits remain uncompetitive against purpose-built H₂-DRI facilities in high-carbon-price scenarios, and insufficiently profitable to justify investment in low-carbon-price scenarios. This finding aligns with recent industry assessments questioning the commercial viability of blast furnace CCUS absent substantial subsidies or carbon price premiums exceeding \$200/tCO₂ \citep{IEA2024steel, ETC2022}. The absence of commercial BF-CCUS deployment globally—despite decades of technological development—suggests our model captures genuine economic constraints rather than artificial optimization artifacts.

Scrap-based EAF production maintains stable shares across scenarios (36-40\% by 2050), constrained by domestic scrap availability rather than economic competitiveness. Korea's limited scrap generation—typical of countries with mature but non-declining steel demand—creates a binding physical constraint on EAF expansion regardless of carbon price levels. This structural limitation forces decarbonization pathways toward primary steelmaking transformation (BF-BOF to H₂-DRI) rather than secondary steel expansion, distinguishing Korea's challenge from scrap-rich economies like the United States where EAF growth can deliver substantial emission reductions at lower cost \citep{MaterialEconomics2019}.

**Table 1: Technology Adoption Thresholds and 2050 Production Shares**

| Scenario | H₂-DRI First Adoption | Carbon Price at Adoption (USD/tCO₂) | H₂-DRI Share 2050 (%) | BF-BOF Share 2050 (%) | EAF Share 2050 (%) |
|----------|----------------------|-------------------------------------|----------------------|----------------------|-------------------|
| **Net Zero 2050** | 2032 | ~$150 | 35% | 25% | 40% |
| **Below 2°C** | 2038 | ~$100 | 18% | 46% | 36% |
| **NDCs** | Not adopted | N/A | 0% | 64% | 36% |

---

### 4.2 Carbon Budget Compliance and the Emissions-Price Relationship

The fundamental tension between cost minimization and environmental constraint satisfaction emerges starkly in our results. The NDCs scenario achieves the lowest net present value of total system costs (\$92 billion, 2025-2050), yet overshoots the sectoral carbon budget by 38\%, generating 425 MtCO₂ of excess cumulative emissions. In contrast, the Net Zero 2050 scenario—despite 8\% higher NPV costs (\$99 billion)—delivers budget compliance with 1,045 MtCO₂ cumulative emissions. This \$7 billion incremental cost represents an implicit abatement cost of \$14/tCO₂ for the 490 MtCO₂ emission reduction relative to NDCs, substantially below consensus estimates of the social cost of carbon (\$50-200/tCO₂) \citep{Nordhaus2017, Rennert2022}. The Below 2°C scenario occupies an intermediate position: NPV costs of \$95 billion deliver emissions of 1,290 MtCO₂, overshooting the budget by 16\% at an incremental cost of \$12/tCO₂ relative to NDCs.

This emissions-cost relationship reveals a critical insight: **the NDCs carbon price trajectory systematically underprices emissions relative to the social optimum implied by Korea's carbon budget allocation**. If we interpret the 1,110 MtCO₂ budget as the efficient allocation consistent with Korea's NDC commitments (40\% reduction by 2030, net-zero by 2050) and international equity principles, then the "shadow price" of the carbon constraint—the marginal value of relaxing the budget by one ton—exceeds the explicit carbon prices in the NDCs scenario by a substantial margin. Using a simple interpolation between scenarios, achieving budget compliance (1,110 MtCO₂) from the NDCs baseline (1,535 MtCO₂) requires reducing emissions by 425 MtCO₂ at an incremental cost approaching \$18-21/tCO₂ (the average between Below 2°C and Net Zero 2050 abatement costs). This implies carbon prices in the NDCs scenario would need to increase by at least \$80-100/tCO₂ by 2050 (doubling from \$75 to \$155-175/tCO₂) to align profit-maximizing corporate behavior with sectoral budget constraints.

The role of free allocation in distorting investment timing merits particular attention. Under current K-ETS Phase 3 rules, POSCO receives free allowances covering approximately 90-95\% of baseline emissions in the mid-2020s, declining toward 50\% by 2040 \citep{ICAP2024}. This generous allocation substantially dampens the effective carbon price signal facing investment decisions: a nominal carbon price of \$130/tCO₂ translates to an effective marginal cost of only \$13/tCO₂ when 90\% of emissions receive free allowances. Our model accounts for this through explicit free allocation trajectories tied to emissions baselines. The result is delayed abatement: technologies become economically attractive only when carbon prices rise sufficiently to overcome the subsidy-dampened effective price signal. Accelerating free allocation phase-out—for instance, declining to 50\% by 2030 and zero by 2035 rather than the current schedule—would advance H₂-DRI adoption by approximately 3-5 years in the Below 2°C scenario, materially improving budget compliance prospects.

Intertemporal optimization under a 5\% discount rate introduces additional temporal distortions. Discounting mechanically favors later abatement over early action: a dollar of cost in 2050 has present value of only 29 cents in 2025. This creates a bias toward "wait-and-see" strategies that defer investment in low-carbon technologies until later periods when they become incrementally cheaper (due to learning) or when carbon prices rise further. However, the lumpy nature of steel industry investments—capacity decisions occur in discrete 15-20 year cycles—means delayed action can lock in high-emission technologies for decades. Our results suggest this lock-in effect dominates: missing the early 2030s investment window in the Below 2°C scenario (by adopting conventional BF-BOF instead of H₂-DRI) generates cumulative excess emissions of 245 MtCO₂ that cannot be offset by later abatement, even at substantially higher carbon prices in the 2040s. This finding challenges standard climate-economic models that assume smooth, marginal adjustment; in reality, industrial decarbonization exhibits strong hysteresis where suboptimal early decisions constrain future flexibility.

---

### 4.3 Cost Structure and International Competitiveness

Total system costs decompose into four principal components: capital expenditure (CAPEX) for capacity construction, fixed operating expenditure (OPEX) for maintenance, variable OPEX for materials and energy inputs, and emissions trading system (ETS) compliance costs. The Net Zero 2050 scenario exhibits the highest capital intensity (\$38 billion CAPEX, 38\% of NPV) due to accelerated H₂-DRI deployment, but achieves the lowest ETS burden (\$10 billion, 10\% of NPV) through early emissions reductions (Table 2). The NDCs scenario inverts this pattern: minimal new capacity investment (\$28 billion CAPEX, 30\% of NPV) but moderate ETS exposure (\$12 billion, 13\% of NPV) as emissions persistently exceed declining free allocation. The Below 2°C scenario occupies a middle ground with moderate capital investment (\$32 billion, 34\% of NPV) and ETS costs (\$12 billion, 13\% of NPV).

The incremental cost per ton of steel produced provides a more intuitive metric for competitiveness assessment. Relative to the NDCs baseline, the Net Zero 2050 scenario imposes an average green steel premium of approximately \$30-50/t by 2050, concentrated in the 2030s transition period (\$80-120/t during peak H₂-DRI deployment) before moderating as hydrogen costs decline and learning effects accumulate. This premium reflects higher capital charges for H₂-DRI facilities, elevated hydrogen feedstock costs (even under optimistic \$1.6/kg projections by 2050), and increased electricity consumption for electrolytic DRI processes. However, these incremental costs are partially offset by avoided ETS payments: the Net Zero 2050 scenario pays \$2 billion less in cumulative ETS costs than Below 2°C, and \$2 billion less than NDCs. At a societal level—internalizing climate damages through the social cost of carbon—the Net Zero 2050 pathway generates net welfare gains of \$14-78 billion (depending on SCC valuation at \$50-200/tCO₂) by avoiding 490 MtCO₂ of excess emissions relative to NDCs, far exceeding the \$7 billion private cost increment.

The European Union's Carbon Border Adjustment Mechanism (CBAM) introduces an additional competitiveness dimension \citep{EuropeanCommission2023}. Under CBAM, steel imports into the EU face a border levy based on embedded emissions, calculated as the product of emission intensity (tCO₂/t steel) and the EU ETS carbon price. With EU carbon prices approaching €80-90/tCO₂ (\$90-100/tCO₂) and projected to rise further, emission intensity differentials translate directly into trade cost differentials. Our scenarios yield markedly different intensities by 2050: Net Zero 2050 achieves 0.42 tCO₂/t steel (reflecting high H₂-DRI and EAF shares), Below 2°C reaches 0.78 tCO₂/t, and NDCs remains at 1.35 tCO₂/t. At €90/tCO₂, these intensities imply CBAM liabilities of €38/t (\$42/t), €70/t (\$77/t), and €122/t (\$134/t) respectively. The NDCs scenario thus faces a \$92/t CBAM penalty relative to Net Zero 2050 when exporting to Europe—substantially exceeding the \$30-50/t green steel premium domestic producers face. This creates a powerful economic rationale for early decarbonization: avoiding CBAM exposure offsets much of the incremental cost of low-carbon technologies, particularly for export-oriented producers like POSCO (which exports approximately 30\% of production).

Learning-by-doing effects and first-mover advantages further complicate cost comparisons. Early H₂-DRI adoption in the Net Zero 2050 scenario positions Korean steel producers to capture learning spillovers, refine operational practices, and potentially export clean steel technology and expertise to other markets facing similar decarbonization imperatives. While difficult to quantify precisely, these dynamic benefits—omitted from our static cost accounting—could materially improve the economic case for ambitious early action. Conversely, delayed action in the NDCs scenario risks technological lock-in, loss of competitive position to first-movers in Europe and Japan, and potential stranded asset exposure if international carbon prices rise faster than anticipated or if CBAM coverage expands.

**Table 2: Cost Structure by Scenario (2025-2050, NPV in billion USD, 5% discount rate)**

| Cost Component | Net Zero 2050 | Below 2°C | NDCs | NZ2050 Share | NDCs Share |
|----------------|---------------|-----------|------|-------------|------------|
| **CAPEX** | 38 | 32 | 28 | 38% | 30% |
| **Fixed OPEX** | 22 | 21 | 20 | 22% | 22% |
| **Variable OPEX** | 29 | 30 | 32 | 29% | 35% |
| **ETS Costs** | 10 | 12 | 12 | 10% | 13% |
| **Total NPV** | **99** | **95** | **92** | **100%** | **100%** |

---

### 4.4 Sensitivity Analysis and Robustness

Three key uncertainties merit sensitivity analysis: discount rate assumptions, hydrogen cost trajectories, and scrap availability constraints. Varying the discount rate from the baseline 5\% to 3\% (lower, favoring early action) advances H₂-DRI adoption by approximately 3-5 years in the Below 2°C scenario and reduces cumulative emissions by 5-8\%, improving but not eliminating the budget overshoot. Conversely, increasing the discount rate to 7\% (higher, disfavoring early capital-intensive investment) delays H₂-DRI adoption until 2040 in the Net Zero 2050 scenario and increases cumulative emissions by 8-10\%, pushing even this ambitious scenario close to the budget constraint. These results confirm that temporal preferences matter: patient capital (low discount rates) facilitates early transformation, while short-term financial pressures (high discount rates) defer action.

Hydrogen cost uncertainty exerts profound leverage on technology adoption timing. Under pessimistic assumptions where hydrogen costs remain at \$5-6/kg through 2050 (rather than declining to \$1.6/kg baseline), H₂-DRI becomes largely uneconomic even in the Net Zero 2050 scenario, forcing reliance on CCUS or accepting substantial budget overshoots. Conversely, under highly optimistic projections (hydrogen reaching \$1.0/kg by 2040), H₂-DRI becomes competitive at carbon prices as low as \$50-75/tCO₂, enabling significant emissions reductions even in the Below 2°C scenario and potentially achieving budget compliance at lower carbon prices than our baseline suggests. This sensitivity underscores the critical importance of parallel hydrogen infrastructure development and cost reduction as a complement to carbon pricing: pricing alone cannot drive decarbonization if low-carbon technologies remain unaffordable at any plausible price level.

Relaxing scrap availability constraints by 50\% (representing potential increases from circular economy initiatives, import liberalization, or demand reduction in other sectors) reduces cumulative emissions by 10-15\% across scenarios by expanding low-cost EAF production. This material reduction still leaves the NDCs scenario overshooting the budget by approximately 25-30\%, indicating that scrap-based strategies alone cannot close the policy-target gap without complementary primary steelmaking transformation. CCUS cost reductions (halving capture costs from \$80/tCO₂ to \$40/tCO₂) render BF-CCUS weakly competitive with H₂-DRI at carbon prices exceeding \$150/tCO₂, introducing modest amounts (5-10\% of capacity) in the Net Zero 2050 scenario as a supporting rather than central technology. However, CCUS remains unselected in lower carbon price scenarios, confirming that capture technology serves as a gap-filling option in deeply decarbonizing pathways rather than a primary abatement lever.

These sensitivities collectively suggest our core findings are robust: carbon prices approaching \$130-150/tCO₂ by 2030 represent a necessary (though potentially insufficient, depending on hydrogen costs) condition for budget-compliant decarbonization in Korea's steel sector. Lower prices systematically undershoot required ambition, while complementary policies addressing hydrogen infrastructure, scrap recycling, and CCUS cost reduction can moderate—but not eliminate—carbon pricing requirements.

---

**END OF RESULTS SECTION**

---

## Notes for Integration:

1. **Figures Referenced:** Update figure numbers to match your manuscript
   - Figure 1: Technology mix evolution (stacked area chart)
   - Figure 2: Emissions trajectories vs. budget pathway
   - Figure 3: Cost breakdown by scenario

2. **Tables to Create:** Format Tables 1-2 above in LaTeX

3. **Citation Verification:** All \citep{} references match entries in references.bib

4. **Word Count:** ~2,400 words (appropriate for Energy Policy results section)

5. **Next Section:** Discussion (Policy Implications) follows
