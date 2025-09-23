"""
Carbon budget calculation for Korea's steel sector.

Calculates sectoral carbon budget allocation based on:
1. Korea's national NDC (40% reduction by 2030, net-zero by 2050)
2. Steel sector's share of national emissions (~12%)
3. POSCO's share of steel sector emissions (~60%)
"""

import logging
import numpy as np
from typing import Dict, Tuple, List

logger = logging.getLogger(__name__)

def calculate_korea_steel_carbon_budget(
    base_year: int = 2018,
    base_emissions_national_MtCO2: float = 727.6,  # Korea's 2018 emissions
    steel_sector_share: float = 0.12,  # Steel sector ~12% of national emissions
    posco_share_of_steel: float = 0.60,  # POSCO ~60% of steel sector
    ndc_2030_reduction: float = 0.40,  # 40% reduction by 2030
    net_zero_year: int = 2050
) -> Dict[str, float]:
    """
    Calculate Korea's steel sector carbon budget and POSCO's allocation.

    Args:
        base_year: Reference year for emissions baseline
        base_emissions_national_MtCO2: National baseline emissions (MtCO2)
        steel_sector_share: Steel sector share of national emissions
        posco_share_of_steel: POSCO's share of steel sector emissions
        ndc_2030_reduction: NDC reduction target for 2030
        net_zero_year: Target year for net-zero emissions

    Returns:
        Dictionary with carbon budget allocations
    """

    # Calculate baseline emissions
    steel_sector_baseline = base_emissions_national_MtCO2 * steel_sector_share
    posco_baseline = steel_sector_baseline * posco_share_of_steel

    # Calculate 2030 target emissions
    national_2030 = base_emissions_national_MtCO2 * (1 - ndc_2030_reduction)
    steel_2030 = national_2030 * steel_sector_share  # Assume proportional reduction
    posco_2030 = steel_2030 * posco_share_of_steel

    # Linear interpolation/extrapolation for cumulative budget
    years = list(range(2025, 2051))  # Model period

    # Steel sector trajectory
    steel_trajectory = {}
    for year in years:
        if year <= 2030:
            # Linear decline to 2030 target
            progress = (year - base_year) / (2030 - base_year)
            steel_trajectory[year] = steel_sector_baseline * (1 - ndc_2030_reduction * progress)
        else:
            # Linear decline from 2030 to net-zero
            progress = (year - 2030) / (net_zero_year - 2030)
            steel_trajectory[year] = steel_2030 * (1 - progress)

    # POSCO trajectory (proportional to steel sector)
    posco_trajectory = {year: emissions * posco_share_of_steel
                       for year, emissions in steel_trajectory.items()}

    # Calculate cumulative budgets
    steel_cumulative_budget = sum(steel_trajectory.values())
    posco_cumulative_budget = sum(posco_trajectory.values())

    budget_allocation = {
        'steel_sector_baseline_2018_MtCO2': steel_sector_baseline,
        'posco_baseline_2018_MtCO2': posco_baseline,
        'steel_sector_2030_target_MtCO2': steel_2030,
        'posco_2030_target_MtCO2': posco_2030,
        'steel_sector_cumulative_budget_2025_2050_MtCO2': steel_cumulative_budget,
        'posco_cumulative_budget_2025_2050_MtCO2': posco_cumulative_budget,
        'annual_trajectory_steel': steel_trajectory,
        'annual_trajectory_posco': posco_trajectory
    }

    logger.info(f"Korea steel sector carbon budget calculated:")
    logger.info(f"  Baseline (2018): {steel_sector_baseline:.1f} MtCO2/y")
    logger.info(f"  2030 target: {steel_2030:.1f} MtCO2/y")
    logger.info(f"  Cumulative budget (2025-2050): {steel_cumulative_budget:.0f} MtCO2")
    logger.info(f"POSCO carbon budget allocation:")
    logger.info(f"  Baseline (2018): {posco_baseline:.1f} MtCO2/y")
    logger.info(f"  2030 target: {posco_2030:.1f} MtCO2/y")
    logger.info(f"  Cumulative budget (2025-2050): {posco_cumulative_budget:.0f} MtCO2")

    return budget_allocation


def compare_scenarios_to_budget(
    scenario_results: Dict[str, Dict[str, any]],
    carbon_budget: Dict[str, float]
) -> Dict[str, Dict[str, float]]:
    """
    Compare scenario emissions to carbon budget.

    Args:
        scenario_results: Results from optimization scenarios
        carbon_budget: Carbon budget allocation from calculate_korea_steel_carbon_budget

    Returns:
        Dictionary with budget compliance analysis
    """

    posco_budget = carbon_budget['posco_cumulative_budget_2025_2050_MtCO2']

    comparison = {}

    for scenario_name, results in scenario_results.items():
        if 'solution' in results and results['status'] == 'SUCCESS':
            solution = results['solution']

            # Calculate cumulative emissions
            cumulative_emissions = sum(solution['emissions'].values())

            # Budget compliance metrics
            overshoot_Mt = cumulative_emissions - posco_budget
            overshoot_percent = (overshoot_Mt / posco_budget) * 100
            compliance = overshoot_Mt <= 0

            comparison[scenario_name] = {
                'cumulative_emissions_MtCO2': cumulative_emissions,
                'carbon_budget_MtCO2': posco_budget,
                'overshoot_MtCO2': overshoot_Mt,
                'overshoot_percent': overshoot_percent,
                'budget_compliant': compliance,
                'budget_utilization_percent': (cumulative_emissions / posco_budget) * 100
            }

            logger.info(f"Scenario {scenario_name}:")
            logger.info(f"  Cumulative emissions: {cumulative_emissions:.0f} MtCO2")
            logger.info(f"  Budget allocation: {posco_budget:.0f} MtCO2")
            if compliance:
                logger.info(f"  COMPLIANT: {abs(overshoot_Mt):.0f} MtCO2 under budget ({abs(overshoot_percent):.1f}%)")
            else:
                logger.info(f"  OVERSHOOT: {overshoot_Mt:.0f} MtCO2 over budget (+{overshoot_percent:.1f}%)")

    return comparison


def create_budget_vs_emissions_data(
    scenario_results: Dict[str, Dict[str, any]],
    carbon_budget: Dict[str, float]
) -> Dict[str, List]:
    """
    Create data for budget vs emissions visualization.

    Args:
        scenario_results: Results from optimization scenarios
        carbon_budget: Carbon budget allocation

    Returns:
        Dictionary with data for plotting
    """

    scenarios = []
    emissions = []
    budget_line = []
    colors = []

    posco_budget = carbon_budget['posco_cumulative_budget_2025_2050_MtCO2']

    # Color mapping for scenarios
    color_map = {
        'NGFS_NetZero2050': '#2E8B57',  # Green
        'NGFS_Below2C': '#FF8C00',     # Orange
        'NGFS_NDCs': '#DC143C'         # Red
    }

    for scenario_name, results in scenario_results.items():
        if 'solution' in results and results['status'] == 'SUCCESS':
            solution = results['solution']
            cumulative_emissions = sum(solution['emissions'].values())

            scenarios.append(scenario_name.replace('NGFS_', '').replace('2050', ' 2050'))
            emissions.append(cumulative_emissions)
            budget_line.append(posco_budget)
            colors.append(color_map.get(scenario_name, '#808080'))

    return {
        'scenarios': scenarios,
        'emissions': emissions,
        'budget': budget_line,
        'colors': colors,
        'budget_value': posco_budget
    }