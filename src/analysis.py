"""Enhanced analysis and visualization for POSCO model results."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import logging
from typing import Dict, Any, List
import os
from pathlib import Path

from carbon_budget import (
    calculate_korea_steel_carbon_budget,
    compare_scenarios_to_budget,
    create_budget_vs_emissions_data
)

logger = logging.getLogger(__name__)

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

def create_enhanced_exports(
    all_solutions: Dict[str, Dict[str, Any]], 
    all_params: Dict[str, Dict[str, Any]], 
    outdir: str
) -> None:
    """Create comprehensive analysis exports across all scenarios."""
    
    logger.info("Creating enhanced analysis exports")
    
    # Create analysis subdirectories
    analysis_dir = Path(outdir) / "analysis"
    analysis_dir.mkdir(exist_ok=True)
    
    # 1. Multi-scenario emission trajectories
    create_emission_analysis(all_solutions, all_params, analysis_dir)
    
    # 2. Cost breakdown analysis
    create_cost_analysis(all_solutions, all_params, analysis_dir)
    
    # 3. Technology transition analysis
    create_technology_analysis(all_solutions, all_params, analysis_dir)
    
    # 4. Carbon pricing impact analysis
    create_carbon_pricing_analysis(all_solutions, all_params, analysis_dir)

    # 5. Carbon budget compliance analysis
    create_carbon_budget_analysis(all_solutions, all_params, analysis_dir)

    logger.info(f"Enhanced analysis exports completed in {analysis_dir}")

def create_emission_analysis(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create detailed emission trajectory analysis."""
    
    logger.info("Creating emission trajectory analysis")
    
    # Prepare data for all scenarios
    emission_data = []
    intensity_data = []
    
    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        
        for year in params['years']:
            # Emission trajectory
            total_prod = sum(solution['production'][r][year] for r in params['routes'])
            scope1_emissions = solution['emissions'][year]  # MtCO2
            free_alloc = params['free_alloc'][year]
            carbon_price = params['carbon_price'][year]
            
            emission_data.append({
                'scenario': scenario,
                'year': year,
                'scope1_emissions_MtCO2': scope1_emissions,
                'total_production_Mt': total_prod,
                'free_allocation_MtCO2': free_alloc,
                'carbon_price_USD_tCO2': carbon_price,
                'net_emissions_MtCO2': max(0, scope1_emissions - free_alloc),
                'ets_cost_million_USD': solution['ets_cost'][year] / 1e6
            })
            
            # Emission intensity
            if total_prod > 0:
                intensity_data.append({
                    'scenario': scenario,
                    'year': year,
                    'emission_intensity_tCO2_per_t': scope1_emissions / total_prod * 1e6,
                    'production_Mt': total_prod
                })
    
    # Export CSVs
    pd.DataFrame(emission_data).to_csv(outdir / "emission_trajectories_all_scenarios.csv", index=False)
    pd.DataFrame(intensity_data).to_csv(outdir / "emission_intensities_all_scenarios.csv", index=False)
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('POSCO Emission Analysis Across Scenarios', fontsize=16, fontweight='bold')
    
    df_emit = pd.DataFrame(emission_data)
    df_intensity = pd.DataFrame(intensity_data)
    
    # Plot 1: Scope 1 emissions trajectory
    ax1 = axes[0,0]
    for scenario in df_emit['scenario'].unique():
        data = df_emit[df_emit['scenario'] == scenario]
        ax1.plot(data['year'], data['scope1_emissions_MtCO2'] * 1e6, 
                marker='o', linewidth=2, label=scenario)
    ax1.set_title('Scope 1 Emissions Trajectory', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Scope 1 Emissions (tCO2)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Emission intensity
    ax2 = axes[0,1]
    for scenario in df_intensity['scenario'].unique():
        data = df_intensity[df_intensity['scenario'] == scenario]
        ax2.plot(data['year'], data['emission_intensity_tCO2_per_t'], 
                marker='s', linewidth=2, label=scenario)
    ax2.set_title('Emission Intensity', fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Emission Intensity (tCO2/t steel)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: ETS cost evolution
    ax3 = axes[1,0]
    for scenario in df_emit['scenario'].unique():
        data = df_emit[df_emit['scenario'] == scenario]
        ax3.plot(data['year'], data['ets_cost_million_USD'], 
                marker='^', linewidth=2, label=scenario)
    ax3.set_title('ETS Cost Evolution', fontweight='bold')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('ETS Cost (Million USD/year)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Free allocation vs emissions
    ax4 = axes[1,1]
    for scenario in df_emit['scenario'].unique():
        data = df_emit[df_emit['scenario'] == scenario]
        ax4.plot(data['year'], data['free_allocation_MtCO2'], 
                linestyle='--', alpha=0.7, label=f'{scenario} - Free Alloc')
        ax4.plot(data['year'], data['scope1_emissions_MtCO2'], 
                linestyle='-', linewidth=2, label=f'{scenario} - Emissions')
    ax4.set_title('Emissions vs Free Allocation', fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('MtCO2/year')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(outdir / "emission_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("Emission analysis completed")

def create_cost_analysis(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create detailed cost breakdown analysis."""
    
    logger.info("Creating cost breakdown analysis")
    
    # Prepare cost breakdown data
    cost_data = []
    annual_cost_data = []
    
    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        
        # Calculate approximate cost components by year
        for year in params['years']:
            total_prod = sum(solution['production'][r][year] for r in params['routes'])
            ets_cost = solution['ets_cost'][year]
            
            # Rough estimates (would need model internals for exact values)
            est_capex = total_prod * 500 * 1e6  # Rough estimate: $500/t capacity
            est_opex = total_prod * 300 * 1e6   # Rough estimate: $300/t/year O&M
            
            cost_data.append({
                'scenario': scenario,
                'year': year,
                'total_production_Mt': total_prod,
                'ets_cost_USD': ets_cost,
                'estimated_capex_USD': est_capex,
                'estimated_opex_USD': est_opex,
                'total_estimated_annual_cost_USD': ets_cost + est_capex + est_opex,
                'ets_cost_share_pct': (ets_cost / (ets_cost + est_capex + est_opex)) * 100 if (ets_cost + est_capex + est_opex) > 0 else 0
            })
            
            annual_cost_data.append({
                'scenario': scenario,
                'year': year,
                'cost_type': 'ETS',
                'cost_million_USD': ets_cost / 1e6
            })
            annual_cost_data.append({
                'scenario': scenario,
                'year': year,
                'cost_type': 'CAPEX (Est.)',
                'cost_million_USD': est_capex / 1e6
            })
            annual_cost_data.append({
                'scenario': scenario,
                'year': year,
                'cost_type': 'OPEX (Est.)',
                'cost_million_USD': est_opex / 1e6
            })
    
    # Export cost data
    pd.DataFrame(cost_data).to_csv(outdir / "cost_breakdown_all_scenarios.csv", index=False)
    
    # Create cost visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('POSCO Cost Analysis Across Scenarios', fontsize=16, fontweight='bold')
    
    df_cost = pd.DataFrame(cost_data)
    df_annual = pd.DataFrame(annual_cost_data)
    
    # Plot 1: ETS cost over time
    ax1 = axes[0,0]
    for scenario in df_cost['scenario'].unique():
        data = df_cost[df_cost['scenario'] == scenario]
        ax1.plot(data['year'], data['ets_cost_USD'] / 1e6, 
                marker='o', linewidth=2, label=scenario)
    ax1.set_title('ETS Cost Evolution', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('ETS Cost (Million USD/year)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Cost composition stacked area (for one scenario)
    if len(all_solutions) > 0:
        main_scenario = list(all_solutions.keys())[0]
        data = df_cost[df_cost['scenario'] == main_scenario]
        
        ax2 = axes[0,1]
        ax2.stackplot(
            data['year'],
            data['ets_cost_USD'] / 1e6,
            data['estimated_capex_USD'] / 1e6,
            data['estimated_opex_USD'] / 1e6,
            labels=['ETS', 'CAPEX (Est.)', 'OPEX (Est.)'],
            alpha=0.8
        )
        ax2.set_title(f'Cost Composition - {main_scenario}', fontweight='bold')
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Annual Cost (Million USD)')
        ax2.legend(loc='upper left')
        ax2.grid(True, alpha=0.3)
    
    # Plot 3: ETS cost share
    ax3 = axes[1,0]
    for scenario in df_cost['scenario'].unique():
        data = df_cost[df_cost['scenario'] == scenario]
        ax3.plot(data['year'], data['ets_cost_share_pct'], 
                marker='s', linewidth=2, label=scenario)
    ax3.set_title('ETS Cost Share of Total', fontweight='bold')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('ETS Cost Share (%)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Cost per ton of steel
    ax4 = axes[1,1]
    for scenario in df_cost['scenario'].unique():
        data = df_cost[df_cost['scenario'] == scenario]
        cost_per_ton = data['total_estimated_annual_cost_USD'] / (data['total_production_Mt'] * 1e6)
        ax4.plot(data['year'], cost_per_ton, 
                marker='^', linewidth=2, label=scenario)
    ax4.set_title('Total Cost per Ton Steel', fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Cost (USD/t steel)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(outdir / "cost_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("Cost analysis completed")

def create_technology_analysis(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create technology transition analysis."""
    
    logger.info("Creating technology transition analysis")
    
    # Prepare technology mix data
    tech_data = []
    
    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        
        for year in params['years']:
            total_prod = sum(solution['production'][r][year] for r in params['routes'])
            
            for route in params['routes']:
                production = solution['production'][route][year]
                share = (production / total_prod * 100) if total_prod > 0 else 0
                
                tech_data.append({
                    'scenario': scenario,
                    'year': year,
                    'technology': route,
                    'production_Mt': production,
                    'market_share_pct': share
                })
    
    # Export technology data
    pd.DataFrame(tech_data).to_csv(outdir / "technology_transitions_all_scenarios.csv", index=False)
    
    # Create technology visualizations
    df_tech = pd.DataFrame(tech_data)
    
    scenarios = df_tech['scenario'].unique()
    n_scenarios = len(scenarios)
    
    fig, axes = plt.subplots(1, n_scenarios, figsize=(6*n_scenarios, 6))
    if n_scenarios == 1:
        axes = [axes]
    
    fig.suptitle('Technology Mix Evolution by Scenario', fontsize=16, fontweight='bold')
    
    for i, scenario in enumerate(scenarios):
        data = df_tech[df_tech['scenario'] == scenario]
        pivot = data.pivot(index='year', columns='technology', values='market_share_pct').fillna(0)
        
        ax = axes[i]
        bottom = np.zeros(len(pivot.index))
        
        for tech in pivot.columns:
            if pivot[tech].sum() > 0.1:  # Only plot technologies with >0.1% total share
                ax.bar(pivot.index, pivot[tech], bottom=bottom, label=tech, alpha=0.8)
                bottom += pivot[tech]
        
        ax.set_title(f'{scenario}', fontweight='bold')
        ax.set_xlabel('Year')
        ax.set_ylabel('Market Share (%)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(outdir / "technology_transitions.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("Technology analysis completed")

def create_carbon_pricing_analysis(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create carbon pricing impact analysis."""
    
    logger.info("Creating carbon pricing impact analysis")
    
    # Prepare carbon pricing data
    carbon_data = []
    
    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        
        for year in params['years']:
            carbon_price = params['carbon_price'][year]
            free_alloc = params['free_alloc'][year]
            emissions = solution['emissions'][year]
            ets_cost = solution['ets_cost'][year]
            
            # Calculate marginal cost of carbon (ETS cost per ton of net emissions)
            net_emissions = max(0, emissions - free_alloc)
            marginal_cost = (ets_cost / (net_emissions * 1e6)) if net_emissions > 0 else 0
            
            carbon_data.append({
                'scenario': scenario,
                'year': year,
                'carbon_price_USD_tCO2': carbon_price,
                'free_allocation_MtCO2': free_alloc,
                'scope1_emissions_MtCO2': emissions,
                'net_emissions_MtCO2': net_emissions,
                'ets_cost_million_USD': ets_cost / 1e6,
                'marginal_carbon_cost_USD_tCO2': marginal_cost,
                'effective_carbon_price_USD_tCO2': carbon_price if net_emissions > 0 else 0
            })
    
    # Export carbon pricing data
    pd.DataFrame(carbon_data).to_csv(outdir / "carbon_pricing_analysis_all_scenarios.csv", index=False)
    
    # Create carbon pricing visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Carbon Pricing Impact Analysis', fontsize=16, fontweight='bold')
    
    df_carbon = pd.DataFrame(carbon_data)
    
    # Plot 1: Carbon price trajectories
    ax1 = axes[0,0]
    for scenario in df_carbon['scenario'].unique():
        data = df_carbon[df_carbon['scenario'] == scenario]
        ax1.plot(data['year'], data['carbon_price_USD_tCO2'], 
                marker='o', linewidth=2, label=scenario)
    ax1.set_title('Carbon Price Trajectories', fontweight='bold')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Carbon Price (USD/tCO2)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Free allocation decline
    ax2 = axes[0,1]
    for scenario in df_carbon['scenario'].unique():
        data = df_carbon[df_carbon['scenario'] == scenario]
        ax2.plot(data['year'], data['free_allocation_MtCO2'], 
                marker='s', linewidth=2, label=scenario)
    ax2.set_title('Free Allocation Decline', fontweight='bold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Free Allocation (MtCO2/year)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: ETS cost vs carbon price
    ax3 = axes[1,0]
    for scenario in df_carbon['scenario'].unique():
        data = df_carbon[df_carbon['scenario'] == scenario]
        scatter = ax3.scatter(data['carbon_price_USD_tCO2'], data['ets_cost_million_USD'], 
                            label=scenario, alpha=0.7, s=50)
    ax3.set_title('ETS Cost vs Carbon Price', fontweight='bold')
    ax3.set_xlabel('Carbon Price (USD/tCO2)')
    ax3.set_ylabel('ETS Cost (Million USD/year)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Net emissions over time
    ax4 = axes[1,1]
    for scenario in df_carbon['scenario'].unique():
        data = df_carbon[df_carbon['scenario'] == scenario]
        ax4.plot(data['year'], data['net_emissions_MtCO2'], 
                marker='^', linewidth=2, label=scenario)
    ax4.set_title('Net Emissions (Above Free Allocation)', fontweight='bold')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Net Emissions (MtCO2/year)')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(outdir / "carbon_pricing_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("Carbon pricing analysis completed")

def create_summary_dashboard(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create a comprehensive dashboard summary."""
    
    logger.info("Creating summary dashboard")
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 4, height_ratios=[1, 1, 1], width_ratios=[1, 1, 1, 1])
    
    # Collect data for dashboard
    scenarios = list(all_solutions.keys())
    years = sorted(list(all_params[scenarios[0]]['years']))
    
    # Main title
    fig.suptitle('POSCO Steel Decarbonization - Comprehensive Dashboard', 
                fontsize=20, fontweight='bold', y=0.95)
    
    # Plot positions
    plots = [
        (0, 0, 'Emission Trajectories'),
        (0, 1, 'Technology Mix 2050'),
        (0, 2, 'ETS Cost Evolution'),
        (0, 3, 'Carbon Pricing'),
        (1, 0, 'Production Levels'),
        (1, 1, 'Emission Intensity'),
        (1, 2, 'Cost per Ton'),
        (1, 3, 'Free Allocation'),
        (2, slice(0, 4), 'Key Metrics Summary Table')
    ]
    
    # Create individual plots
    for i, (row, col, title) in enumerate(plots[:-1]):
        ax = fig.add_subplot(gs[row, col])
        
        if title == 'Emission Trajectories':
            for scenario in scenarios:
                solution = all_solutions[scenario]
                emissions = [solution['emissions'][y] * 1e6 for y in years]  # Convert to tCO2
                ax.plot(years, emissions, marker='o', label=scenario, linewidth=2)
            ax.set_title(title, fontweight='bold')
            ax.set_ylabel('Scope 1 (tCO2/year)')
            ax.legend()
            
        elif title == 'Technology Mix 2050':
            if 2050 in years:
                scenario = scenarios[0]  # Show first scenario
                solution = all_solutions[scenario]
                params = all_params[scenario]
                
                production_2050 = {r: solution['production'][r][2050] for r in params['routes']}
                total = sum(production_2050.values())
                
                if total > 0:
                    sizes = [production_2050[r] for r in params['routes'] if production_2050[r] > 0.01]
                    labels = [r for r in params['routes'] if production_2050[r] > 0.01]
                    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
                ax.set_title(f'{title} - {scenario}', fontweight='bold')
            
        # Add more plots as needed...
        
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(outdir / "summary_dashboard.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info("Summary dashboard completed")

def create_carbon_budget_analysis(all_solutions: Dict, all_params: Dict, outdir: Path) -> None:
    """Create carbon budget compliance analysis and visualization."""

    logger.info("Creating carbon budget compliance analysis")

    # Calculate Korea steel sector carbon budget
    carbon_budget = calculate_korea_steel_carbon_budget()

    # Compare scenarios to budget
    budget_comparison = compare_scenarios_to_budget(all_solutions, carbon_budget)

    # Export budget comparison data
    comparison_df = pd.DataFrame([
        {
            'scenario': scenario,
            **metrics
        }
        for scenario, metrics in budget_comparison.items()
    ])
    comparison_df.to_csv(outdir / "carbon_budget_compliance.csv", index=False)

    # Create budget vs emissions visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Carbon Budget Compliance Analysis', fontsize=16, fontweight='bold')

    # Plot 1: Bar chart - Cumulative emissions vs budget
    scenarios = comparison_df['scenario'].str.replace('NGFS_', '').str.replace('2050', ' 2050')
    cumulative_emissions = comparison_df['cumulative_emissions_MtCO2']
    budget_value = comparison_df['carbon_budget_MtCO2'].iloc[0]

    colors = ['#2E8B57' if comp else '#DC143C' for comp in comparison_df['budget_compliant']]

    bars = ax1.bar(scenarios, cumulative_emissions, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax1.axhline(y=budget_value, color='red', linestyle='--', linewidth=3, label='Carbon Budget Limit')

    # Add percentage labels on bars
    for i, (bar, overshoot) in enumerate(zip(bars, comparison_df['overshoot_percent'])):
        height = bar.get_height()
        if overshoot <= 0:
            label = f"{abs(overshoot):.0f}% under"
            color = 'darkgreen'
        else:
            label = f"{overshoot:.0f}% over"
            color = 'darkred'
        ax1.text(bar.get_x() + bar.get_width()/2., height + 20,
                label, ha='center', va='bottom', fontweight='bold', color=color)

    ax1.set_title('Cumulative Emissions vs Carbon Budget (2025-2050)', fontweight='bold')
    ax1.set_ylabel('Cumulative Emissions (MtCO₂)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, max(cumulative_emissions) * 1.15)

    # Plot 2: Budget utilization percentage
    budget_utilization = comparison_df['budget_utilization_percent']
    bars2 = ax2.bar(scenarios, budget_utilization, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    ax2.axhline(y=100, color='red', linestyle='--', linewidth=3, label='Budget Limit (100%)')

    # Add percentage labels
    for bar, util in zip(bars2, budget_utilization):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
                f"{util:.0f}%", ha='center', va='bottom', fontweight='bold')

    ax2.set_title('Carbon Budget Utilization', fontweight='bold')
    ax2.set_ylabel('Budget Utilization (%)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, max(budget_utilization) * 1.15)

    plt.tight_layout()
    plt.savefig(outdir / "carbon_budget_compliance.png", dpi=300, bbox_inches='tight')

    # Also save to figures directory for LaTeX
    figures_dir = Path("figures")
    figures_dir.mkdir(exist_ok=True)
    plt.savefig(figures_dir / "carbon_budget_compliance.png", dpi=300, bbox_inches='tight')

    plt.close()

    # Create annual emissions trajectory with budget pathway
    fig, ax = plt.subplots(figsize=(12, 8))

    budget_trajectory = carbon_budget['annual_trajectory_posco']
    years = sorted(budget_trajectory.keys())
    budget_pathway = [budget_trajectory[year] for year in years]

    # Plot budget pathway
    ax.plot(years, budget_pathway, 'r--', linewidth=3, label='Carbon Budget Pathway', alpha=0.8)

    # Plot scenario trajectories
    colors_dict = {
        'NGFS_NetZero2050': '#2E8B57',
        'NGFS_Below2C': '#FF8C00',
        'NGFS_NDCs': '#DC143C'
    }

    for scenario, solution in all_solutions.items():
        params = all_params[scenario]
        annual_emissions = [solution['emissions'][year] for year in params['years']]
        scenario_label = scenario.replace('NGFS_', '').replace('2050', ' 2050')

        ax.plot(params['years'], annual_emissions,
               color=colors_dict.get(scenario, '#808080'),
               linewidth=2.5, marker='o', markersize=4,
               label=scenario_label, alpha=0.9)

    ax.set_title('Annual Emissions Trajectories vs Carbon Budget Pathway',
                fontsize=14, fontweight='bold')
    ax.set_xlabel('Year')
    ax.set_ylabel('Annual Emissions (MtCO₂/year)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(outdir / "emissions_vs_budget_trajectory.png", dpi=300, bbox_inches='tight')
    plt.savefig(figures_dir / "scope1_scenarios.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Log summary results
    logger.info("Carbon budget analysis summary:")
    for scenario, metrics in budget_comparison.items():
        status = "COMPLIANT" if metrics['budget_compliant'] else "OVERSHOOT"
        logger.info(f"  {scenario}: {status} - {metrics['overshoot_percent']:.1f}% {'under' if metrics['overshoot_percent'] <= 0 else 'over'} budget")

    logger.info("Carbon budget analysis completed")