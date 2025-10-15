#!/usr/bin/env python3
"""
Generate publication-ready figures for Energy Policy submission.

Requirements:
  - 6.5 x 4.0 inch canvas
  - White background, Arial font (9-10 pt)
  - Blue/grey colour palette, colour-blind friendly
  - PNG (600 dpi), PDF, EPS outputs
  - Stored under figures_pub/ with Figure_# naming
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
log = logging.getLogger(__name__)

OUTPUT_DIR = Path("figures_pub")

FIGURE_SPECS = {
    "Figure_1_Scope1_Emissions": "scope1_emissions",
    "Figure_2_Technology_Shares": "technology_transition",
    "Figure_3_Production_Mix": "production_mix",
    "Figure_4_Emissions_Pathways": "emissions_pathways",
    "Figure_5_ETS_Costs": "ets_costs",
    "Figure_6_ETS_Cost_Mechanics": "ets_cost_logic",
}

SCENARIO_FILES = {
    "NGFS_NetZero2050": Path("outputs/series_NGFS_NetZero2050.csv"),
    "NGFS_Below2C": Path("outputs/series_NGFS_Below2C.csv"),
    "NGFS_NDCs": Path("outputs/series_NGFS_NDCs.csv"),
    "NGFS_NetZero2050_NoCCUS": Path("outputs/no_ccus/series_NGFS_NetZero2050_NoCCUS.csv"),
}

SCENARIO_STYLES = {
    "NGFS_NetZero2050_NoCCUS": {"label": "Net Zero 2050 (No CCUS)", "color": "#1f77b4", "weight": 2.6},
    "NGFS_NetZero2050": {"label": "Net Zero 2050", "color": "#4c72b0", "weight": 2.0},
    "NGFS_Below2C": {"label": "Below 2°C", "color": "#708090", "weight": 2.0},
    "NGFS_NDCs": {"label": "NDCs", "color": "#a6a6a6", "weight": 1.8},
}

PRIMARY_SCENARIO = "NGFS_NetZero2050_NoCCUS"
TECH_ORDER = [
    "BF-BOF",
    "BF-BOF+CCUS",
    "FINEX-BOF",
    "Scrap-EAF",
    "NG-DRI-EAF",
    "H2-DRI-EAF",
    "HyREX",
]
TECH_LABELS = {
    "BF-BOF": "BF-BOF",
    "BF-BOF+CCUS": "BF-BOF + CCUS",
    "FINEX-BOF": "FINEX-BOF",
    "Scrap-EAF": "Scrap EAF",
    "NG-DRI-EAF": "NG-DRI EAF",
    "H2-DRI-EAF": "H₂-DRI EAF",
    "HyREX": "HyREX",
}

TECH_COLORS = {
    "BF-BOF": "#2C3E50",
    "BF-BOF+CCUS": "#2874A6",
    "FINEX-BOF": "#5499C7",
    "Scrap-EAF": "#85C1E9",
    "NG-DRI-EAF": "#566573",
    "H2-DRI-EAF": "#AEB6BF",
    "HyREX": "#D5DBDB",
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

FIGSIZE = (6.5, 4.0)
FONT_FAMILY = "Arial"


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def set_style() -> None:
    plt.style.use("default")
    plt.rcParams.update({
        "font.family": FONT_FAMILY,
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)


def load_scenario_data() -> Dict[str, pd.DataFrame]:
    data = {}
    for scenario, path in SCENARIO_FILES.items():
        if not path.exists():
            raise FileNotFoundError(f"Required scenario series not found: {path}")
        df = pd.read_csv(path)
        df = df.sort_values("year").reset_index(drop=True)
        numeric_cols = [c for c in df.columns if c not in {"year", "carbon_scenario", "demand_satisfied"}]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
        data[scenario] = df
    return data


def save_figure(fig: plt.Figure, name: str) -> None:
    base = OUTPUT_DIR / name
    fig.tight_layout()
    fig.canvas.draw_idle()
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".eps"), bbox_inches="tight")
    plt.close(fig)
    log.info("Saved %s.[png/pdf/eps]", base.name)


def compute_shares(df: pd.DataFrame) -> pd.DataFrame:
    shares = pd.DataFrame({"year": df["year"]})
    total = df["total_production_Mt"].replace(0, np.nan)
    for col, label in PRODUCTION_COLUMNS.items():
        if col in df.columns:
            shares[label] = (df[col] / total * 100).fillna(0.0)
    return shares


def compute_volumes(df: pd.DataFrame) -> pd.DataFrame:
    volumes = pd.DataFrame({"year": df["year"]})
    for col, label in PRODUCTION_COLUMNS.items():
        if col in df.columns:
            volumes[label] = df[col].fillna(0.0)
    return volumes


# ---------------------------------------------------------------------------
# Figure builders
# ---------------------------------------------------------------------------

def figure_scope1(scenario_data: Dict[str, pd.DataFrame]) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    for scenario, df in scenario_data.items():
        style = SCENARIO_STYLES.get(scenario, {})
        ax.plot(
            df["year"],
            df["scope1_emissions_MtCO2"],
            label=style.get("label", scenario),
            color=style.get("color", "#808080"),
            linewidth=style.get("weight", 2.0),
        )
    ax.set_xlabel("Year")
    ax.set_ylabel(r"MtCO$_2$ per year")
    ax.set_title("Scope 1 emissions by scenario")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    save_figure(fig, "Figure_1_Scope1_Emissions")


def figure_technology_shares(scenario_data: Dict[str, pd.DataFrame]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE, sharex=True)
    axes = axes.flatten()
    for ax, scenario in zip(axes, SCENARIO_STYLES.keys()):
        df = scenario_data.get(scenario)
        if df is None:
            ax.axis("off")
            continue
        shares = compute_shares(df)
        categories = [c for c in TECH_ORDER if c in shares.columns]
        stacks = [shares[c].values for c in categories]
        colors = [TECH_COLORS[c] for c in categories]
        ax.stackplot(shares["year"], stacks, labels=[TECH_LABELS[c] for c in categories], colors=colors)
        ax.set_title(SCENARIO_STYLES[scenario]["label"])
        ax.set_ylabel("Share of output (%)")
        ax.set_ylim(0, 100)
        ax.grid(True, alpha=0.3)
    axes[-1].set_xlabel("Year")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.02))
    save_figure(fig, "Figure_2_Technology_Shares")


def figure_production_mix(scenario_data: Dict[str, pd.DataFrame]) -> None:
    fig, axes = plt.subplots(2, 2, figsize=FIGSIZE, sharex=True)
    axes = axes.flatten()
    for ax, scenario in zip(axes, SCENARIO_STYLES.keys()):
        df = scenario_data.get(scenario)
        if df is None:
            ax.axis("off")
            continue
        volumes = compute_volumes(df)
        categories = [c for c in TECH_ORDER if c in volumes.columns]
        stacks = [volumes[c].values for c in categories]
        colors = [TECH_COLORS[c] for c in categories]
        ax.stackplot(volumes["year"], stacks, labels=[TECH_LABELS[c] for c in categories], colors=colors)
        ax.set_title(SCENARIO_STYLES[scenario]["label"])
        ax.set_ylabel("Production (Mt/year)")
        ax.grid(True, alpha=0.3)
    axes[-1].set_xlabel("Year")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=4, frameon=False, bbox_to_anchor=(0.5, 1.02))
    save_figure(fig, "Figure_3_Production_Mix")


def figure_emissions_pathways(scenario_data: Dict[str, pd.DataFrame]) -> None:
    fig, axes = plt.subplots(1, 2, figsize=FIGSIZE, sharex=True)
    for scenario, df in scenario_data.items():
        style = SCENARIO_STYLES.get(scenario, {})
        axes[0].plot(
            df["year"],
            df["scope1_emissions_MtCO2"],
            label=style.get("label", scenario),
            color=style.get("color", "#808080"),
            linewidth=style.get("weight", 2.0),
        )
        intensity = df["scope1_emissions_MtCO2"] / df["total_production_Mt"]
        axes[1].plot(
            df["year"],
            intensity,
            label=style.get("label", scenario),
            color=style.get("color", "#808080"),
            linewidth=style.get("weight", 2.0),
        )
    axes[0].set_title("Annual emissions")
    axes[0].set_ylabel(r"MtCO$_2$ per year")
    axes[1].set_title("Emissions intensity")
    axes[1].set_ylabel(r"tCO$_2$ per t steel")
    for ax in axes:
        ax.set_xlabel("Year")
        ax.grid(True, alpha=0.3)
    axes[1].legend(frameon=False, loc="upper right")
    save_figure(fig, "Figure_4_Emissions_Pathways")


def figure_ets_costs(scenario_data: Dict[str, pd.DataFrame]) -> None:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    for scenario, df in scenario_data.items():
        style = SCENARIO_STYLES.get(scenario, {})
        ax.plot(
            df["year"],
            df["ets_cost_USD"] / 1e9,
            label=style.get("label", scenario),
            color=style.get("color", "#808080"),
            linewidth=style.get("weight", 2.0),
        )
    ax.set_xlabel("Year")
    ax.set_ylabel("Billion USD per year")
    ax.set_title("Annual ETS payments by scenario")
    ax.grid(True, alpha=0.3)
    ax.legend(frameon=False, loc="upper right")
    save_figure(fig, "Figure_5_ETS_Costs")


def figure_ets_logic(scenario_data: Dict[str, pd.DataFrame]) -> None:
    df = scenario_data[PRIMARY_SCENARIO]
    years = df["year"]
    emissions = df["scope1_emissions_MtCO2"]
    free_alloc = df.get("free_allocation_MtCO2", pd.Series(np.nan, index=years.index))
    carbon_price = df.get("carbon_price_USD_per_tCO2")
    ets_liability = (emissions - free_alloc).clip(lower=0.0)
    ets_cost = df.get("ets_cost_USD", pd.Series(0.0, index=years.index))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=FIGSIZE, sharex=True)

    ax1.plot(years, emissions, label="Gross emissions", color="#1f77b4", linewidth=2.4)
    ax1.plot(years, free_alloc, label="Free allocation", color="#4c72b0", linestyle="--", linewidth=2.0)
    ax1.fill_between(years, free_alloc, emissions, where=emissions > free_alloc, color="#a6c8ff", alpha=0.4)
    ax1.set_ylabel(r"MtCO$_2$ per year")
    ax1.set_title("ETS mechanics – Net Zero 2050 (No CCUS)")
    ax1.grid(True, alpha=0.3)
    ax1.legend(frameon=False, loc="upper left")

    ax1b = ax1.twinx()
    ax1b.plot(years, carbon_price, color="#5d6d7e", linewidth=2.0, label="Carbon price")
    ax1b.set_ylabel(r"USD per tCO$_2$")
    ax1b.legend(frameon=False, loc="upper right")

    ax2.bar(years, ets_liability, color="#4c72b0", edgecolor="#1f4a78", label="ETS-liable emissions")
    ax2.set_ylabel(r"MtCO$_2$")
    ax2.set_xlabel("Year")
    ax2.grid(True, axis="y", alpha=0.3)

    ax2b = ax2.twinx()
    ax2b.plot(years, ets_cost / 1e9, color="#2c3e50", linewidth=2.0, label="ETS payments")
    ax2b.set_ylabel("Billion USD per year")

    ax2.legend(frameon=False, loc="upper left")
    ax2b.legend(frameon=False, loc="upper right")

    save_figure(fig, "Figure_6_ETS_Cost_Mechanics")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    set_style()
    ensure_output_dir()
    scenario_data = load_scenario_data()

    figure_scope1(scenario_data)
    figure_technology_shares(scenario_data)
    figure_production_mix(scenario_data)
    figure_emissions_pathways(scenario_data)
    figure_ets_costs(scenario_data)
    figure_ets_logic(scenario_data)

    log.info("All publication figures generated in %s", OUTPUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
