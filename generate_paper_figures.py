#!/usr/bin/env python3
"""
Generate publication-ready figures for the POSCO optimisation paper.

This script prefers previously exported scenario series (in ./outputs) so that we
can reuse the data that feeds the LaTeX tables. If any required CSV is missing it
falls back to running the optimisation model and then produces the figures.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

# Ensure src/ is importable
# Ensure the repository root is importable so we can use the src package
sys.path.append(str(Path(__file__).parent))

from src.scenarios import run_all_scenarios, run_single_scenario
from src.carbon_budget import calculate_korea_steel_carbon_budget

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

BASE_SCENARIOS = ["NGFS_NetZero2050", "NGFS_Below2C", "NGFS_NDCs"]
PRIMARY_SCENARIO = "NGFS_NetZero2050_NoCCUS"

SCENARIO_CONFIG = {
    "NGFS_NetZero2050_NoCCUS": {
        "label": "Net Zero 2050 (No CCUS)",
        "color": "#005f73",
        "path": Path("outputs/no_ccus/series_NGFS_NetZero2050_NoCCUS.csv"),
        "primary": True,
    },
    "NGFS_NetZero2050": {
        "label": "Net Zero 2050",
        "color": "#0a9396",
        "path": Path("outputs/series_NGFS_NetZero2050.csv"),
    },
    "NGFS_Below2C": {
        "label": "Below 2°C",
        "color": "#ee9b00",
        "path": Path("outputs/series_NGFS_Below2C.csv"),
    },
    "NGFS_NDCs": {
        "label": "NDCs",
        "color": "#ae2012",
        "path": Path("outputs/series_NGFS_NDCs.csv"),
    },
}

SCENARIO_ORDER = [
    "NGFS_NetZero2050_NoCCUS",
    "NGFS_NetZero2050",
    "NGFS_Below2C",
    "NGFS_NDCs",
]

TECH_ORDER = [
    "BF-BOF",
    "BF-BOF+CCUS",
    "FINEX-BOF",
    "Scrap-EAF",
    "NG-DRI-EAF",
    "H2-DRI-EAF",
    "HyREX",
]

TECH_COLORS = {
    "BF-BOF": "#8c510a",
    "BF-BOF+CCUS": "#bf812d",
    "FINEX-BOF": "#dfc27d",
    "Scrap-EAF": "#80cdc1",
    "NG-DRI-EAF": "#35978f",
    "H2-DRI-EAF": "#01665e",
    "HyREX": "#003c30",
}

PRODUCTION_COLUMNS = {
    "production_BF-BOF_Mt": "BF-BOF",
    "production_BF-BOF+CCUS_Mt": "BF-BOF+CCUS",
    "production_FINEX-BOF_Mt": "FINEX-BOF",
    "production_Scrap-EAF_Mt": "Scrap-EAF",
    "production_NG-DRI-EAF_Mt": "NG-DRI-EAF",
    "production_H2-DRI-EAF_Mt": "H2-DRI-EAF",
    "production_HyREX_Mt": "HyREX",
}

# Matplotlib defaults tuned for print-friendly figures
plt.style.use("seaborn-v0_8-whitegrid")
plt.rcParams.update(
    {
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.titlesize": 14,
        "axes.grid": True,
        "grid.alpha": 0.3,
    }
)


# --------------------------------------------------------------------------------------
# Data preparation helpers
# --------------------------------------------------------------------------------------

def _load_series_csv(path: Path) -> pd.DataFrame:
    """Load a scenario series CSV and ensure numeric typing."""
    df = pd.read_csv(path)
    if "year" not in df.columns:
        raise ValueError(f"{path} does not contain a 'year' column.")
    df = df.sort_values("year").reset_index(drop=True)
    numeric_cols = [
        c for c in df.columns if c not in {"year", "carbon_scenario", "demand_satisfied"}
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df


def ensure_no_ccus_scenario(data_path: str) -> None:
    """Run the Net Zero scenario with CCUS capture disabled and persist the CSV."""
    meta = SCENARIO_CONFIG[PRIMARY_SCENARIO]
    output_dir = meta["path"].parent
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Generating Net Zero 2050 scenario with CCUS disabled for figure focus.")
    result = run_single_scenario(
        data_path=data_path,
        carbon_scenario="NGFS_NetZero2050",
        h2_case="baseline",
        discount_rate=0.05,
        utilization=0.90,
        output_dir=str(output_dir),
        ccus_capture_rate=0.0,
    )

    if result.get("status") != "SUCCESS":
        raise RuntimeError(
            f"No-CCUS scenario optimisation failed: {result.get('status')} {result.get('error')}"
        )

    # Rename exports so they carry the _NoCCUS suffix and do not collide with main runs
    src_csv = output_dir / "series_NGFS_NetZero2050.csv"
    dest_csv = meta["path"]
    if src_csv.exists():
        dest_csv.unlink(missing_ok=True)
        src_csv.rename(dest_csv)

    src_summary = output_dir / "summary_NGFS_NetZero2050.json"
    dest_summary = output_dir / "summary_NGFS_NetZero2050_NoCCUS.json"
    if src_summary.exists():
        dest_summary.unlink(missing_ok=True)
        src_summary.rename(dest_summary)


def collect_scenario_data(data_path: str) -> Dict[str, pd.DataFrame]:
    """Ensure required CSVs exist and return prepared data frames."""
    scenario_data: Dict[str, pd.DataFrame] = {}

    missing = [s for s in BASE_SCENARIOS if not SCENARIO_CONFIG[s]["path"].exists()]
    if missing:
        logger.info(
            "Scenario CSVs missing for %s. Running optimisation to regenerate.",
            ", ".join(missing),
        )
        results = run_all_scenarios(
            data_path=data_path,
            h2_case="baseline",
            discount_rate=0.05,
            utilization=0.90,
            output_dir="outputs",
        )
        if results["run_summary"]["successful_scenarios"] == 0:
            raise RuntimeError("Optimisation runs failed; cannot build figures.")

    for scenario in BASE_SCENARIOS:
        path = SCENARIO_CONFIG[scenario]["path"]
        if not path.exists():
            raise FileNotFoundError(f"Expected series output missing: {path}")
        scenario_data[scenario] = _load_series_csv(path)

    # Ensure the highlighted no-CCUS run exists
    if not SCENARIO_CONFIG[PRIMARY_SCENARIO]["path"].exists():
        ensure_no_ccus_scenario(data_path)

    no_ccus_path = SCENARIO_CONFIG[PRIMARY_SCENARIO]["path"]
    if no_ccus_path.exists():
        scenario_data[PRIMARY_SCENARIO] = _load_series_csv(no_ccus_path)
    else:
        logger.warning("No-CCUS scenario CSV still missing; figures will omit it.")

    return scenario_data


def compute_share_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe of technology shares (% of total production)."""
    shares = pd.DataFrame({"year": df["year"]})
    denominator = df["total_production_Mt"].replace(0, np.nan)
    for col, label in PRODUCTION_COLUMNS.items():
        if col in df.columns:
            shares[label] = (df[col] / denominator * 100.0).fillna(0.0)
    return shares


def compute_volume_df(df: pd.DataFrame) -> pd.DataFrame:
    """Return a dataframe of technology production volumes (Mt)."""
    volumes = pd.DataFrame({"year": df["year"]})
    for col, label in PRODUCTION_COLUMNS.items():
        if col in df.columns:
            volumes[label] = df[col].fillna(0.0)
    return volumes


def _plot_stack(
    ax: plt.Axes,
    df: pd.DataFrame,
    scenario_key: str,
    value_df_func,
    ylabel: str,
    legend: bool,
) -> None:
    """Generic stacked area helper used by both share and volume plots."""
    value_df = value_df_func(df)
    categories = [c for c in TECH_ORDER if c in value_df.columns]
    if not categories:
        return

    years = value_df["year"].values
    stacks = [value_df[c].values for c in categories]
    colors = [TECH_COLORS[c] for c in categories]

    ax.stackplot(years, stacks, labels=categories, colors=colors, alpha=0.9)
    ax.set_title(SCENARIO_CONFIG[scenario_key]["label"])
    ax.set_ylabel(ylabel)
    ax.set_xlim(years[0], years[-1])
    ax.set_xlabel("Year")
    if ylabel.endswith("(%)"):
        ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.25)
    if legend:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.25))


# --------------------------------------------------------------------------------------
# Figure builders
# --------------------------------------------------------------------------------------

def generate_scope1_emissions_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering scope 1 emissions trajectories.")
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    for scenario in SCENARIO_ORDER:
        if scenario not in scenario_data:
            continue
        df = scenario_data[scenario]
        meta = SCENARIO_CONFIG[scenario]
        lw = 3.0 if meta.get("primary") else 2.0
        alpha = 1.0 if meta.get("primary") else 0.65
        ax.plot(
            df["year"],
            df["scope1_emissions_MtCO2"],
            label=meta["label"],
            color=meta["color"],
            linewidth=lw,
            alpha=alpha,
        )

    ax.set_title("Scope 1 emissions by scenario (2025–2050)")
    ax.set_xlabel("Year")
    ax.set_ylabel("MtCO$_2$ per year")
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.35)
    plt.tight_layout()
    plt.savefig(figures_dir / "scope1_by_scenario.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_emissions_pathways_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering emissions level and intensity figure.")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), sharex=True)

    for ax in axes:
        ax.grid(True, alpha=0.25)

    for scenario in SCENARIO_ORDER:
        if scenario not in scenario_data:
            continue
        df = scenario_data[scenario]
        meta = SCENARIO_CONFIG[scenario]
        lw = 2.8 if meta.get("primary") else 1.9
        alpha = 1.0 if meta.get("primary") else 0.7

        axes[0].plot(
            df["year"],
            df["scope1_emissions_MtCO2"],
            label=meta["label"],
            color=meta["color"],
            linewidth=lw,
            alpha=alpha,
        )
        intensity = df["scope1_emissions_MtCO2"] / df["total_production_Mt"]
        axes[1].plot(
            df["year"],
            intensity,
            label=meta["label"],
            color=meta["color"],
            linewidth=lw,
            alpha=alpha,
        )

    axes[0].set_title("Annual Scope 1 emissions")
    axes[0].set_ylabel("MtCO$_2$/year")
    axes[1].set_title("Emissions intensity")
    axes[1].set_ylabel("tCO$_2$ per t steel")
    for ax in axes:
        ax.set_xlabel("Year")

    axes[0].legend(frameon=False)
    plt.tight_layout()
    plt.savefig(figures_dir / "emissions_pathways.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_technology_transition_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering technology share transition panels.")
    if PRIMARY_SCENARIO not in scenario_data:
        logger.warning("Primary scenario missing – skipping technology transition figure.")
        return

    fig = plt.figure(figsize=(12, 7.8))
    gs = GridSpec(2, 3, height_ratios=[1.25, 1], figure=fig)

    # Main panel: non-CCUS scenario
    ax_main = fig.add_subplot(gs[0, :])
    _plot_stack(
        ax_main,
        scenario_data[PRIMARY_SCENARIO],
        PRIMARY_SCENARIO,
        compute_share_df,
        "Share of total output (%)",
        legend=True,
    )
    ax_main.set_xlabel("")

    bottom_scenarios = [s for s in SCENARIO_ORDER if s != PRIMARY_SCENARIO]
    for idx, scenario in enumerate(bottom_scenarios):
        if scenario not in scenario_data:
            continue
        ax = fig.add_subplot(gs[1, idx])
        _plot_stack(
            ax,
            scenario_data[scenario],
            scenario,
            compute_share_df,
            "Share of total output (%)",
            legend=False,
        )

    fig.suptitle("Technology shares of production (model output vs. time)", y=0.98)
    plt.tight_layout()
    plt.savefig(figures_dir / "technology_transition.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_production_mix_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering production mix (absolute volumes).")
    if PRIMARY_SCENARIO not in scenario_data:
        logger.warning("Primary scenario missing – skipping production mix figure.")
        return

    fig = plt.figure(figsize=(12, 7.8))
    gs = GridSpec(2, 3, height_ratios=[1.25, 1], figure=fig)

    ax_main = fig.add_subplot(gs[0, :])
    _plot_stack(
        ax_main,
        scenario_data[PRIMARY_SCENARIO],
        PRIMARY_SCENARIO,
        compute_volume_df,
        "Production (Mt/year)",
        legend=True,
    )
    ax_main.set_xlabel("")

    bottom_scenarios = [s for s in SCENARIO_ORDER if s != PRIMARY_SCENARIO]
    for idx, scenario in enumerate(bottom_scenarios):
        if scenario not in scenario_data:
            continue
        ax = fig.add_subplot(gs[1, idx])
        _plot_stack(
            ax,
            scenario_data[scenario],
            scenario,
            compute_volume_df,
            "Production (Mt/year)",
            legend=False,
        )

    fig.suptitle("Production mix by technology route", y=0.98)
    plt.tight_layout()
    plt.savefig(figures_dir / "production_mix_evolution.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_ets_costs_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering ETS cost comparison.")
    fig, ax = plt.subplots(figsize=(8.5, 5.2))

    for scenario in SCENARIO_ORDER:
        if scenario not in scenario_data:
            continue
        df = scenario_data[scenario]
        meta = SCENARIO_CONFIG[scenario]
        lw = 3.0 if meta.get("primary") else 2.0
        alpha = 1.0 if meta.get("primary") else 0.65
        ax.plot(
            df["year"],
            df["ets_cost_USD"] / 1e9,
            label=meta["label"],
            color=meta["color"],
            linewidth=lw,
            alpha=alpha,
        )

    ax.set_title("Annual ETS payments")
    ax.set_xlabel("Year")
    ax.set_ylabel("Billion USD (real 2024)")
    ax.legend(frameon=False)
    plt.tight_layout()
    plt.savefig(figures_dir / "ets_cost_by_scenario.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_ets_cost_logic_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering ETS cost logic decomposition.")
    primary = PRIMARY_SCENARIO if PRIMARY_SCENARIO in scenario_data else BASE_SCENARIOS[0]
    if primary not in scenario_data:
        logger.warning("No scenario data available for ETS logic visual.")
        return

    df = scenario_data[primary].copy()
    years = df["year"]
    emissions = df["scope1_emissions_MtCO2"]
    free_alloc = df.get(
        "free_allocation_MtCO2", pd.Series([np.nan] * len(df), index=df.index)
    )
    carbon_price = df.get("carbon_price_USD_per_tCO2")
    ets_liability = df.get(
        "ets_positive_MtCO2", (emissions - free_alloc).clip(lower=0.0)
    )
    ets_cost = df.get("ets_cost_USD", pd.Series([0.0] * len(df), index=df.index))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

    ax1.plot(years, emissions, color="#1b4332", linewidth=2.5, label="Gross emissions")
    ax1.plot(
        years,
        free_alloc,
        color="#74c69d",
        linewidth=2.5,
        linestyle="--",
        label="Free allocation",
    )
    ax1.fill_between(
        years,
        free_alloc,
        emissions,
        where=emissions > free_alloc,
        color="#d8f3dc",
        alpha=0.6,
        label="Liability window",
    )
    ax1.set_ylabel("MtCO$_2$/year")
    ax1.set_title(
        f"ETS mechanics: {SCENARIO_CONFIG.get(primary, {}).get('label', primary)}"
    )
    ax1.grid(True, alpha=0.25)

    if carbon_price is not None:
        ax1b = ax1.twinx()
        ax1b.plot(
            years,
            carbon_price,
            color="#1d3557",
            linewidth=2.2,
            label="Carbon price",
        )
        ax1b.set_ylabel("USD per tCO$_2$")
        handles1, labels1 = ax1.get_legend_handles_labels()
        handles2, labels2 = ax1b.get_legend_handles_labels()
        ax1.legend(
            handles1 + handles2,
            labels1 + labels2,
            frameon=False,
            loc="upper left",
        )
    else:
        ax1.legend(frameon=False, loc="upper left")

    ax2.bar(
        years,
        ets_liability,
        color="#ffbe0b",
        edgecolor="#d18a00",
        alpha=0.85,
        label="Net ETS liability",
    )
    ax2.set_ylabel("MtCO$_2$")
    ax2.set_xlabel("Year")
    ax2.grid(True, axis="y", alpha=0.25)

    if ets_cost is not None:
        ax2b = ax2.twinx()
        ax2b.plot(
            years,
            ets_cost / 1e9,
            color="#fb5607",
            linewidth=2.4,
            label="ETS payment",
        )
        ax2b.set_ylabel("Billion USD")
        handles1, labels1 = ax2.get_legend_handles_labels()
        handles2, labels2 = ax2b.get_legend_handles_labels()
        ax2.legend(
            handles1 + handles2,
            labels1 + labels2,
            frameon=False,
            loc="upper left",
        )
    else:
        ax2.legend(frameon=False, loc="upper left")

    plt.tight_layout()
    plt.savefig(figures_dir / "ets_cost_logic.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def generate_carbon_budget_figure(
    scenario_data: Dict[str, pd.DataFrame], figures_dir: Path
) -> None:
    logger.info("Rendering carbon budget compliance summary.")
    carbon_budget = calculate_korea_steel_carbon_budget()
    limit = carbon_budget["posco_cumulative_budget_2025_2050_MtCO2"]

    records = []
    for scenario, df in scenario_data.items():
        cumulative = df["scope1_emissions_MtCO2"].sum()
        overshoot = cumulative - limit
        records.append(
            {
                "key": scenario,
                "scenario": SCENARIO_CONFIG.get(scenario, {}).get("label", scenario),
                "cumulative": cumulative,
                "overshoot_pct": overshoot / limit * 100.0,
                "compliant": overshoot <= 0,
            }
        )

    if not records:
        logger.warning("No data available for carbon budget figure.")
        return

    def _order(record):
        key = record.get("key")
        return SCENARIO_ORDER.index(key) if key in SCENARIO_ORDER else len(SCENARIO_ORDER)

    records.sort(key=_order)

    scenarios = [r["scenario"] for r in records]
    cumulative = [r["cumulative"] for r in records]
    compliant = [r["compliant"] for r in records]
    overshoot_pct = [r["overshoot_pct"] for r in records]
    colors = ["#2e7d32" if c else "#c62828" for c in compliant]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))

    bars = axes[0].bar(scenarios, cumulative, color=colors)
    axes[0].axhline(limit, color="#444444", linestyle="--", linewidth=1.8)
    axes[0].set_ylabel("Cumulative Scope 1 (MtCO$_2$)")
    axes[0].set_title("Cumulative emissions vs. budget (2025–2050)")
    axes[0].set_ylim(0, max(max(cumulative) * 1.1, limit * 1.05))
    axes[0].tick_params(axis="x", rotation=15)

    for bar, pct in zip(bars, overshoot_pct):
        axes[0].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 15,
            f"{pct:+.1f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    utilization = [c / limit * 100.0 for c in cumulative]
    bars2 = axes[1].bar(scenarios, utilization, color=colors)
    axes[1].axhline(100, color="#444444", linestyle="--", linewidth=1.8)
    axes[1].set_ylabel("Budget utilisation (%)")
    axes[1].set_title("Budget utilisation index")
    axes[1].set_ylim(0, max(max(utilization) * 1.1, 110))
    axes[1].tick_params(axis="x", rotation=15)

    for bar, util in zip(bars2, utilization):
        axes[1].text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 2,
            f"{util:.1f}%",
            ha="center",
            va="bottom",
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig(figures_dir / "carbon_budget_compliance.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


# --------------------------------------------------------------------------------------
# Orchestrator
# --------------------------------------------------------------------------------------

def generate_all_paper_figures(
    data_path: str = "data/posco_parameters_enhanced_academic.xlsx",
) -> bool:
    """Main orchestration routine."""
    figures_dir = Path("figures")
    figures_dir.mkdir(exist_ok=True)
    Path("outputs").mkdir(exist_ok=True)

    scenario_data = collect_scenario_data(data_path)

    generate_scope1_emissions_figure(scenario_data, figures_dir)
    generate_emissions_pathways_figure(scenario_data, figures_dir)
    generate_technology_transition_figure(scenario_data, figures_dir)
    generate_production_mix_figure(scenario_data, figures_dir)
    generate_ets_costs_figure(scenario_data, figures_dir)
    generate_ets_cost_logic_figure(scenario_data, figures_dir)
    generate_carbon_budget_figure(scenario_data, figures_dir)

    logger.info("All figure routines completed.")
    return True


def main() -> int:
    """CLI entry point."""
    print("=" * 80)
    print("POSCO OPTIMISATION MODEL – PAPER FIGURE GENERATION")
    print("=" * 80)

    data_files = [
        "data/posco_parameters_enhanced_academic.xlsx",
        "data/posco_parameters_consolidated_v2_0.xlsx",
        "data/posco_parameters_consolidated.xlsx",
    ]

    data_path = next((f for f in data_files if Path(f).exists()), None)
    if not data_path:
        logger.error("No data workbook found. Checked: %s", ", ".join(data_files))
        return 1

    logger.info("Using data workbook: %s", data_path)
    success = generate_all_paper_figures(data_path)

    if success:
        print("\n" + "=" * 80)
        print("FIGURE GENERATION COMPLETE")
        print("=" * 80)
        print("Updated assets:")
        print("  - figures/scope1_by_scenario.png")
        print("  - figures/emissions_pathways.png")
        print("  - figures/technology_transition.png")
        print("  - figures/production_mix_evolution.png")
        print("  - figures/ets_cost_by_scenario.png")
        print("  - figures/ets_cost_logic.png")
        print("  - figures/carbon_budget_compliance.png")
        print("=" * 80)
        return 0

    print("Figure generation failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
