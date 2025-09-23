#!/usr/bin/env python3
"""
Visualization module for POSCO v2.0 decarbonization optimization results.

Creates comprehensive matplotlib charts for multi-scenario analysis, production mix,
emissions pathways, cost breakdowns, and technology transitions.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Set style for professional plots
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Color schemes for different elements
SCENARIO_COLORS = {
    'NGFS_NetZero2050': '#2E8B57',  # Sea Green
    'NGFS_Below2C': '#4169E1',      # Royal Blue  
    'NGFS_NDCs': '#DC143C'          # Crimson
}

TECHNOLOGY_COLORS = {
    'BF-BOF': '#8B4513',           # Saddle Brown (traditional)
    'FINEX-BOF': '#A0522D',        # Sienna (improved traditional)
    'BF-BOF+CCUS': '#CD853F',      # Peru (traditional with CCUS)
    'NG-DRI-dom': '#4682B4',       # Steel Blue (NG reduction)
    'H2-DRI-dom': '#00CED1',       # Dark Turquoise (H2 reduction)
    'EAF': '#32CD32',              # Lime Green (electric)
    'HBI-import': '#FF6347',       # Tomato (imported)
    'Scrap': '#696969'             # Dim Gray (recycled)
}

def create_scenario_plots(output_dir: str) -> None:
    """
    Create all visualization plots for multi-scenario analysis.
    
    Args:
        output_dir: Directory containing results and where plots will be saved
    """
    
    logger.info("Creating visualization plots for multi-scenario analysis")
    
    output_path = Path(output_dir)
    if not output_path.exists():
        raise ValueError(f"Output directory does not exist: {output_dir}")
    
    # Look for aggregated results file
    csv_path = output_path / 'series_all_scenarios.csv'
    if not csv_path.exists():
        raise FileNotFoundError(f"Aggregated results file not found: {csv_path}")
    
    # Create figures directory
    figs_dir = output_path / 'figs'
    figs_dir.mkdir(exist_ok=True)
    
    # Load data
    df = pd.read_csv(csv_path)
    scenarios = df['carbon_scenario'].unique()
    
    logger.info(f"Creating plots for {len(scenarios)} scenarios: {list(scenarios)}")
    
    # Generate all plots
    plot_functions = [
        plot_emissions_pathways,
        plot_production_mix_evolution,
        plot_technology_transition,
        plot_carbon_pricing_and_ets,
        plot_cost_breakdown_by_scenario,
        plot_metallics_composition,
        plot_capacity_utilization,
        plot_scenario_comparison_summary
    ]
    
    for plot_func in plot_functions:
        try:
            plot_func(df, str(figs_dir))
            logger.info(f"Generated plot: {plot_func.__name__}")
        except Exception as e:
            logger.error(f"Failed to generate {plot_func.__name__}: {e}")
    
    logger.info(f"All plots saved to {figs_dir}")

def plot_emissions_pathways(df: pd.DataFrame, output_dir: str) -> None:
    """Plot Scope 1 emissions pathways by scenario."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Absolute emissions
    scenarios = df['carbon_scenario'].unique()
    
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        ax1.plot(scenario_data['year'], scenario_data['scope1_emissions_MtCO2'], 
                marker='o', linewidth=2.5, label=scenario, 
                color=SCENARIO_COLORS.get(scenario, 'gray'))
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Scope 1 Emissions (MtCO2/year)')
    ax1.set_title('Emissions Pathways by Carbon Scenario')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Emissions intensity
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        total_production = scenario_data['total_steel_Mt']
        emissions_intensity = scenario_data['scope1_emissions_MtCO2'] / total_production
        
        ax2.plot(scenario_data['year'], emissions_intensity, 
                marker='s', linewidth=2.5, label=scenario,
                color=SCENARIO_COLORS.get(scenario, 'gray'))
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Emissions Intensity (tCO2/t steel)')
    ax2.set_title('Emissions Intensity by Scenario')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/emissions_pathways.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_production_mix_evolution(df: pd.DataFrame, output_dir: str) -> None:
    """Plot evolution of production mix by technology route."""
    
    scenarios = df['carbon_scenario'].unique()
    fig, axes = plt.subplots(1, len(scenarios), figsize=(5*len(scenarios), 6))
    
    if len(scenarios) == 1:
        axes = [axes]
    
    for i, scenario in enumerate(scenarios):
        scenario_data = df[df['carbon_scenario'] == scenario].sort_values('year')
        
        # Stack production by technology
        hotmetal_cols = [col for col in df.columns if col.startswith('hotmetal_') and col.endswith('_Mt')]
        eaf_col = 'eaf_production_Mt'
        
        # Prepare data for stacking
        bottom = np.zeros(len(scenario_data))
        
        # Plot hotmetal routes
        for col in hotmetal_cols:
            route_name = col.replace('hotmetal_', '').replace('_Mt', '')
            if route_name in TECHNOLOGY_COLORS:
                axes[i].bar(scenario_data['year'], scenario_data[col], 
                           bottom=bottom, label=route_name,
                           color=TECHNOLOGY_COLORS[route_name], alpha=0.8)
                bottom += scenario_data[col]
        
        # Plot EAF
        axes[i].bar(scenario_data['year'], scenario_data[eaf_col], 
                   bottom=bottom, label='EAF', 
                   color=TECHNOLOGY_COLORS['EAF'], alpha=0.8)
        
        axes[i].set_xlabel('Year')
        axes[i].set_ylabel('Steel Production (Mt/year)')
        axes[i].set_title(f'{scenario}')
        axes[i].legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('Steel Production Mix Evolution by Scenario', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/production_mix_evolution.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_technology_transition(df: pd.DataFrame, output_dir: str) -> None:
    """Plot technology share transition from first to last year."""
    
    scenarios = df['carbon_scenario'].unique()
    years = sorted(df['year'].unique())
    first_year, last_year = years[0], years[-1]
    
    fig, axes = plt.subplots(2, len(scenarios), figsize=(5*len(scenarios), 10))
    
    if len(scenarios) == 1:
        axes = axes.reshape(-1, 1)
    
    for i, scenario in enumerate(scenarios):
        scenario_data = df[df['carbon_scenario'] == scenario]
        
        for j, year in enumerate([first_year, last_year]):
            year_data = scenario_data[scenario_data['year'] == year].iloc[0]
            
            # Calculate shares
            total_production = year_data['total_steel_Mt']
            
            if total_production > 0:
                shares = {}
                
                # Hotmetal routes
                hotmetal_cols = [col for col in df.columns if col.startswith('hotmetal_') and col.endswith('_Mt')]
                for col in hotmetal_cols:
                    route_name = col.replace('hotmetal_', '').replace('_Mt', '')
                    shares[route_name] = year_data[col] / total_production * 100
                
                # EAF
                shares['EAF'] = year_data['eaf_production_Mt'] / total_production * 100
                
                # Filter out zero shares
                shares = {k: v for k, v in shares.items() if v > 0.1}
                
                # Create pie chart
                colors = [TECHNOLOGY_COLORS.get(tech, 'gray') for tech in shares.keys()]
                wedges, texts, autotexts = axes[j, i].pie(shares.values(), 
                                                         labels=shares.keys(),
                                                         colors=colors,
                                                         autopct='%1.1f%%',
                                                         startangle=90)
                
                # Enhance text
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_weight('bold')
            
            axes[j, i].set_title(f'{scenario} - {year}')
    
    plt.suptitle('Technology Mix Transition: First vs Last Year', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/technology_transition.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_carbon_pricing_and_ets(df: pd.DataFrame, output_dir: str) -> None:
    """Plot carbon pricing evolution and ETS costs."""
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    scenarios = df['carbon_scenario'].unique()
    
    # Plot 1: Carbon price trajectories
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        ax1.plot(scenario_data['year'], scenario_data['carbon_price_USD_per_tCO2'], 
                marker='o', linewidth=3, label=scenario,
                color=SCENARIO_COLORS.get(scenario, 'gray'))
    
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Carbon Price (USD/tCO2)')
    ax1.set_title('Carbon Price Trajectories by Scenario')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')  # Log scale for better visibility
    
    # Plot 2: Annual ETS costs
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        ets_cost_millions = scenario_data['ets_cost_USD'] / 1e6
        
        ax2.plot(scenario_data['year'], ets_cost_millions, 
                marker='s', linewidth=3, label=scenario,
                color=SCENARIO_COLORS.get(scenario, 'gray'))
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Annual ETS Cost (Million USD)')
    ax2.set_title('Annual ETS Costs by Scenario')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/carbon_pricing_and_ets.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_cost_breakdown_by_scenario(df: pd.DataFrame, output_dir: str) -> None:
    """Plot cost breakdown by major categories and scenario."""
    
    scenarios = df['carbon_scenario'].unique()
    
    # Calculate total costs by category
    cost_categories = ['total_capex_USD', 'total_fixom_USD', 'total_varopex_USD', 'ets_cost_USD']
    category_labels = ['CAPEX', 'Fixed O&M', 'Variable O&M', 'ETS Cost']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Total cumulative costs by scenario
    scenario_totals = []
    
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        totals = {}
        
        for i, category in enumerate(cost_categories):
            totals[category_labels[i]] = scenario_data[category].sum() / 1e9  # Billion USD
        
        scenario_totals.append(totals)
    
    # Create stacked bar chart
    bottom = np.zeros(len(scenarios))
    colors = plt.cm.Set3(np.linspace(0, 1, len(category_labels)))
    
    for i, category in enumerate(category_labels):
        values = [totals[category] for totals in scenario_totals]
        ax1.bar(scenarios, values, bottom=bottom, label=category, color=colors[i])
        bottom += values
    
    ax1.set_ylabel('Cumulative Cost (Billion USD)')
    ax1.set_title('Total System Costs by Scenario')
    ax1.legend()
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Cost intensity (cost per tonne steel)
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        total_cost = scenario_data[cost_categories].sum(axis=1)
        total_production = scenario_data['total_steel_Mt']
        cost_intensity = total_cost / (total_production * 1e6)  # USD per tonne
        
        ax2.plot(scenario_data['year'], cost_intensity, 
                marker='o', linewidth=2.5, label=scenario,
                color=SCENARIO_COLORS.get(scenario, 'gray'))
    
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Cost Intensity (USD/t steel)')
    ax2.set_title('Cost Intensity by Scenario')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/cost_breakdown_by_scenario.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_metallics_composition(df: pd.DataFrame, output_dir: str) -> None:
    """Plot metallics composition for EAF (scrap, HBI, domestic reduction)."""
    
    scenarios = df['carbon_scenario'].unique()
    fig, axes = plt.subplots(1, len(scenarios), figsize=(6*len(scenarios), 6))
    
    if len(scenarios) == 1:
        axes = [axes]
    
    for i, scenario in enumerate(scenarios):
        scenario_data = df[df['carbon_scenario'] == scenario].sort_values('year')
        
        # Metallics components
        scrap = scenario_data['scrap_consumption_Mt']
        hbi = scenario_data['hbi_import_Mt']
        reduction = scenario_data['total_reduction_Mt']
        
        # Stack metallics
        axes[i].bar(scenario_data['year'], scrap, label='Scrap', 
                   color=TECHNOLOGY_COLORS['Scrap'], alpha=0.8)
        axes[i].bar(scenario_data['year'], hbi, bottom=scrap, label='HBI Import',
                   color=TECHNOLOGY_COLORS['HBI-import'], alpha=0.8)
        axes[i].bar(scenario_data['year'], reduction, bottom=scrap+hbi, label='Domestic Reduction',
                   color=TECHNOLOGY_COLORS['H2-DRI-dom'], alpha=0.8)
        
        axes[i].set_xlabel('Year')
        axes[i].set_ylabel('Metallics Consumption (Mt/year)')
        axes[i].set_title(f'Metallics Mix - {scenario}')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.suptitle('EAF Metallics Composition by Scenario', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/metallics_composition.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_capacity_utilization(df: pd.DataFrame, output_dir: str) -> None:
    """Plot capacity utilization rates over time."""
    
    scenarios = df['carbon_scenario'].unique()
    
    # Find utilization columns
    util_cols = [col for col in df.columns if 'utilization' in col.lower()]
    
    if not util_cols:
        # Calculate utilization from production and capacity data
        logger.warning("No utilization columns found, skipping capacity utilization plot")
        return
    
    fig, axes = plt.subplots(1, len(scenarios), figsize=(6*len(scenarios), 6))
    
    if len(scenarios) == 1:
        axes = [axes]
    
    for i, scenario in enumerate(scenarios):
        scenario_data = df[df['carbon_scenario'] == scenario].sort_values('year')
        
        # Plot available utilization data
        for col in util_cols:
            if col in scenario_data.columns:
                tech_name = col.replace('_utilization', '').replace('utilization_', '')
                axes[i].plot(scenario_data['year'], scenario_data[col] * 100, 
                            marker='o', linewidth=2, label=tech_name)
        
        axes[i].axhline(y=90, color='red', linestyle='--', alpha=0.7, label='90% Limit')
        axes[i].set_xlabel('Year')
        axes[i].set_ylabel('Capacity Utilization (%)')
        axes[i].set_title(f'Capacity Utilization - {scenario}')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
        axes[i].set_ylim(0, 100)
    
    plt.suptitle('Capacity Utilization Rates by Scenario', fontsize=16, y=1.02)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/capacity_utilization.png", dpi=300, bbox_inches='tight')
    plt.close()

def plot_scenario_comparison_summary(df: pd.DataFrame, output_dir: str) -> None:
    """Create summary comparison chart across key metrics."""
    
    scenarios = df['carbon_scenario'].unique()
    years = sorted(df['year'].unique())
    first_year, last_year = years[0], years[-1]
    
    # Calculate summary metrics
    summary_data = []
    
    for scenario in scenarios:
        scenario_data = df[df['carbon_scenario'] == scenario]
        
        # Emissions reduction
        emissions_first = scenario_data[scenario_data['year'] == first_year]['scope1_emissions_MtCO2'].iloc[0]
        emissions_last = scenario_data[scenario_data['year'] == last_year]['scope1_emissions_MtCO2'].iloc[0]
        emissions_reduction = (emissions_first - emissions_last) / emissions_first * 100
        
        # Final year EAF share
        total_final = scenario_data[scenario_data['year'] == last_year]['total_steel_Mt'].iloc[0]
        eaf_final = scenario_data[scenario_data['year'] == last_year]['eaf_production_Mt'].iloc[0]
        eaf_share = eaf_final / total_final * 100 if total_final > 0 else 0
        
        # Total ETS cost
        total_ets = scenario_data['ets_cost_USD'].sum() / 1e9  # Billion USD
        
        # Final carbon price
        final_carbon_price = scenario_data[scenario_data['year'] == last_year]['carbon_price_USD_per_tCO2'].iloc[0]
        
        summary_data.append({
            'Scenario': scenario,
            'Emissions Reduction (%)': emissions_reduction,
            f'EAF Share {last_year} (%)': eaf_share,
            'Total ETS Cost (B$)': total_ets,
            f'Carbon Price {last_year} ($/tCO2)': final_carbon_price
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create subplots for each metric
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()
    
    metrics = ['Emissions Reduction (%)', f'EAF Share {last_year} (%)', 
               'Total ETS Cost (B$)', f'Carbon Price {last_year} ($/tCO2)']
    
    for i, metric in enumerate(metrics):
        colors = [SCENARIO_COLORS.get(scenario, 'gray') for scenario in summary_df['Scenario']]
        
        bars = axes[i].bar(summary_df['Scenario'], summary_df[metric], color=colors, alpha=0.8)
        axes[i].set_title(metric)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            axes[i].text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}', ha='center', va='bottom')
    
    plt.suptitle('Scenario Comparison Summary', fontsize=16, y=0.98)
    plt.tight_layout()
    plt.savefig(f"{output_dir}/scenario_comparison_summary.png", dpi=300, bbox_inches='tight')
    plt.close()

# Legacy functions for backwards compatibility
def plot_scope1_by_scenario(csv_path: str, output_path: str) -> None:
    """Plot Scope 1 emissions by scenario (legacy function)."""
    df = pd.read_csv(csv_path)
    plot_emissions_pathways(df, str(Path(output_path).parent))

def plot_ets_cost_by_scenario(csv_path: str, output_path: str) -> None:
    """Plot ETS cost by scenario (legacy function)."""
    df = pd.read_csv(csv_path)
    plot_carbon_pricing_and_ets(df, str(Path(output_path).parent))

def plot_production_by_route(csv_path: str, output_path: str, scenario: str) -> None:
    """Plot production by route for a scenario (legacy function)."""
    df = pd.read_csv(csv_path)
    plot_production_mix_evolution(df, str(Path(output_path).parent))

def main():
    """CLI entry point for visualization module."""
    
    import argparse
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='POSCO v2.0 Visualization Generator')
    parser.add_argument('--output', type=str, required=True, 
                       help='Output directory containing results')
    
    args = parser.parse_args()
    
    try:
        create_scenario_plots(args.output)
        logger.info("Visualization generation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Visualization generation failed: {e}")
        return 1

if __name__ == '__main__':
    exit(main())