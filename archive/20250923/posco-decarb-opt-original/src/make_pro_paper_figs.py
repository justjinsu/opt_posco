#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_pro_paper_figs.py

Generate publication-grade (PDF + PNG) figures from detailed scenario outputs.

Inputs (defaults can be overridden via CLI):
  - detailed_results_NGFS_NetZero2050.csv
  - detailed_results_NGFS_Below2C.csv
  - detailed_results_NGFS_NDCs.csv
  - summary_*.json   (optional; used for ΔNPV in MAC proxy)
  - any additional detailed_results_*_*.csv (optional; used for robustness bars)

Outputs (default: ./figs_pro/):
  - fig_scope1_by_scenario.(pdf|png)
  - fig_prodmix_{NetZero2050|Below2C|NDCs}.(pdf|png)
  - fig_ets_cost_by_scenario.(pdf|png)
  - fig_cum_scope1_bar.(pdf|png)
  - fig_cum_ets_bar.(pdf|png)  [if ETS column present]
  - fig_mac_proxy.(pdf|png)
  - fig_timeline_{NetZero2050|Below2C|NDCs}.(pdf|png)
  - fig_cum_vs_budget_{NetZero2050|Below2C|NDCs}.(pdf|png)
  - fig_h2_{scenario}.(pdf|png)     [if hydrogen column present]
  - fig_elec_{scenario}.(pdf|png)   [if electricity column present]
  - fig_robust_2050_scope1.(pdf|png)  [if extra cases found]
  - fig_robust_cumETS.(pdf|png)       [if extra cases found]

Design rules:
  - matplotlib only (no seaborn)
  - one chart per figure (no subplots)
  - do not set custom colors or styles
"""

import argparse
import os
import glob
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------- Helpers ----------

def ensure_outdir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    return df

def safe_json(path: str) -> dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def pick_col(df: pd.DataFrame, names) -> str | None:
    """Pick the first matching column name (case-insensitive fallback)."""
    for n in names:
        if n in df.columns:
            return n
    lowmap = {c.lower(): c for c in df.columns}
    for n in names:
        if n.lower() in lowmap:
            return lowmap[n.lower()]
    return None

def first_positive_year(series: pd.Series, years: pd.Series, tol=1e-9) -> int | None:
    idx = np.where(series.fillna(0.0).values > tol)[0]
    return int(years.iloc[idx[0]]) if len(idx) else None

def savefig_base(pathbase: str) -> None:
    plt.tight_layout()
    plt.savefig(pathbase + ".pdf")
    plt.savefig(pathbase + ".png")
    plt.show()


# ---------- Core plotting functions (matplotlib only) ----------

def fig_scope1_by_scenario(dfs, labels, outdir):
    plt.figure(figsize=(5.2, 3.4))
    for key, label in labels.items():
        df = dfs[key]
        s1 = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
        if not s1:
            continue
        plt.plot(df["year"], df[s1], label=label)
    plt.xlabel("Year")
    plt.ylabel("Scope 1 emissions (MtCO₂)")
    plt.title("Scope 1 emissions by scenario (2025–2050)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(frameon=False, ncol=1)
    savefig_base(os.path.join(outdir, "fig_scope1_by_scenario"))

def fig_production_mix_per_scenario(df, label, outpath_base):
    # Attempt to infer category series from common column name patterns
    hot_cols   = [c for c in df.columns if c.startswith("hotmetal_") and c.endswith("_Mt")]
    red_cols   = [c for c in df.columns if c.startswith("reduction_") and c.endswith("_Mt")]
    hbi_cols   = [c for c in df.columns if "hbi"   in c.lower() and c.endswith("_Mt")]
    scrap_cols = [c for c in df.columns if "scrap" in c.lower() and c.endswith("_Mt")]
    ts = pd.DataFrame({"year": df["year"]})
    ts["Hot metal"]               = df[hot_cols].sum(axis=1) if hot_cols else 0.0
    ts["Domestic DRI (NG/H₂)"]    = df[red_cols].sum(axis=1) if red_cols else 0.0
    ts["Imported HBI"]            = df[hbi_cols].sum(axis=1) if hbi_cols else 0.0
    if scrap_cols:
        ts["Scrap to EAF"]       = df[scrap_cols].sum(axis=1)
    # drop zero-only series
    for c in list(ts.columns):
        if c != "year" and np.allclose(ts[c].fillna(0.0), 0.0):
            ts.drop(columns=[c], inplace=True)

    if ts.shape[1] <= 1:
        return  # nothing to draw

    plt.figure(figsize=(5.2, 3.4))
    x = ts["year"].values
    ycols = [c for c in ts.columns if c != "year"]
    y = [ts[c].values for c in ycols]
    plt.stackplot(x, y, labels=ycols)
    plt.xlabel("Year")
    plt.ylabel("Production inputs (Mt)")
    plt.title(f"Production mix over time — {label}")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(frameon=False, ncol=1, loc="upper left")
    savefig_base(outpath_base)

def fig_ets_cost_by_scenario(dfs, labels, outdir):
    plt.figure(figsize=(5.2, 3.4))
    has_any = False
    for key, label in labels.items():
        df = dfs[key]
        ets_col = next((c for c in df.columns
                        if c.lower().startswith("ets") and c.lower().endswith("_usd")), None)
        if ets_col is None:
            continue
        plt.plot(df["year"], df[ets_col], label=label)
        has_any = True
    if not has_any:
        plt.close()
        return
    plt.xlabel("Year")
    plt.ylabel("ETS cost (USD)")
    plt.title("ETS cost by scenario (annual)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(frameon=False, ncol=1)
    savefig_base(os.path.join(outdir, "fig_ets_cost_by_scenario"))

def fig_cumulative_bars(dfs, labels, outdir):
    # Build aggregate table
    rows = []
    for key, label in labels.items():
        df = dfs[key]
        s1 = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
        ets_col = next((c for c in df.columns
                        if c.lower().startswith("ets") and c.lower().endswith("_usd")), None)
        if not s1:
            continue
        cum_s1 = float(df[s1].sum())
        cum_ets_busd = float(df[ets_col].sum()/1e9) if ets_col else np.nan
        rows.append((label, cum_s1, cum_ets_busd))
    if not rows:
        return
    labels_list, cum_s1_list, cum_ets_list = zip(*rows)

    # Cumulative Scope 1 bar
    plt.figure(figsize=(5.2, 3.4))
    plt.bar(labels_list, cum_s1_list)
    plt.ylabel("Cumulative Scope 1 (MtCO₂)")
    plt.title("Cumulative Scope 1 emissions by scenario (2025–2050)")
    plt.xticks(rotation=15, ha="right")
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)
    savefig_base(os.path.join(outdir, "fig_cum_scope1_bar"))

    # Cumulative ETS bar (if any)
    if any(np.isfinite(c) for c in cum_ets_list):
        plt.figure(figsize=(5.2, 3.4))
        plt.bar(labels_list, cum_ets_list)
        plt.ylabel("Cumulative ETS (B USD)")
        plt.title("Cumulative ETS cost by scenario (2025–2050)")
        plt.xticks(rotation=15, ha="right")
        plt.grid(True, axis="y", linestyle="--", alpha=0.5)
        savefig_base(os.path.join(outdir, "fig_cum_ets_bar"))

def fig_mac_proxy(dfs, summaries, labels, outdir, ndcs_key="NDCs"):
    """MAC proxy via scenario ladder: ΔNPV vs cumulative abatement relative to NDCs."""
    if ndcs_key not in dfs:
        return
    ref_df = dfs[ndcs_key]
    s1 = pick_col(ref_df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
    if not s1:
        return
    ref_cum = ref_df[s1].sum()
    ref_obj = summaries.get(ndcs_key, {}).get("objective_USD", np.nan)

    rows = []
    for key, label in labels.items():
        df = dfs[key]
        s1k = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
        if not s1k:
            continue
        cum = df[s1k].sum()
        obj = summaries.get(key, {}).get("objective_USD", np.nan)
        abate = ref_cum - cum
        dcost = obj - ref_obj if (np.isfinite(obj) and np.isfinite(ref_obj)) else np.nan
        rows.append((label, abate, (dcost/1e9) if np.isfinite(dcost) else np.nan))
    if not rows:
        return
    labels_list, x, y = zip(*rows)

    plt.figure(figsize=(5.2, 3.4))
    plt.plot(x, y, marker="o")
    for xi, yi, lab in zip(x, y, labels_list):
        plt.annotate(lab, (xi, yi), xytext=(4, 4), textcoords="offset points")
    plt.xlabel("Cumulative abatement vs NDCs (MtCO₂, 2025–2050)")
    plt.ylabel("ΔNPV vs NDCs (B USD)")
    plt.title("Policy ladder MAC proxy (lower-right is better)")
    plt.grid(True, linestyle="--", alpha=0.5)
    savefig_base(os.path.join(outdir, "fig_mac_proxy"))

def fig_timeline_markers(df, label, outpath_base):
    years = df["year"]
    zeros = pd.Series(0.0, index=df.index)

    # Identify flows for timing
    red_cols = [c for c in df.columns if "reduction" in c.lower() and c.endswith("_Mt")]
    h2_cols  = [c for c in red_cols if "h2" in c.lower()]
    ng_cols  = [c for c in red_cols if ("ng" in c.lower()) or ("gas" in c.lower())]
    hbi_col  = next((c for c in df.columns if "hbi" in c.lower() and c.endswith("_Mt")), None)
    ets_col  = next((c for c in df.columns if c.lower().startswith("ets") and c.lower().endswith("_usd")), None)
    s1       = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])

    first_h2  = first_positive_year(df[h2_cols].sum(axis=1) if h2_cols else zeros, years)
    first_ng  = first_positive_year(df[ng_cols].sum(axis=1) if ng_cols else zeros, years)
    first_hbi = first_positive_year(df[hbi_col] if hbi_col is not None else zeros, years)

    half_emis = None
    if s1:
        base = float(df[s1].iloc[0]); target = 0.5*base
        hits = df[df[s1] <= target]
        if len(hits):
            half_emis = int(hits["year"].iloc[0])

    ets_peak_year = None
    if ets_col:
        idx = df[ets_col].idxmax()
        ets_peak_year = int(df.loc[idx, "year"])

    # Draw markers on a minimal baseline
    plt.figure(figsize=(5.6, 1.6))
    plt.plot(years, zeros, alpha=0)
    for y, val, text in [
        (first_ng, 1.00, "First NG-DRI"),
        (first_h2, 1.20, "First H₂-DRI"),
        (first_hbi, 0.80, "First HBI import"),
        (half_emis, 0.60, "Half-emissions"),
        (ets_peak_year, 1.40, "ETS peak"),
    ]:
        if y:
            plt.vlines(y, 0, val, linestyles="--")
            plt.text(y, val + 0.05, text, rotation=90, va="bottom", ha="center")
    plt.yticks([])
    plt.xlabel("Year")
    plt.title(f"Investment timeline markers — {label}")
    savefig_base(outpath_base)

def fig_cum_vs_budget(df, label, outpath_base):
    s1 = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
    if not s1:
        return
    years = df["year"]
    y0 = float(df[s1].iloc[0])
    y_end = 0.0
    T = len(years)  # Use actual number of data points
    budget_series = np.linspace(y0, y_end, T)
    budget_cum = budget_series.cumsum()
    actual_cum = df[s1].cumsum().values

    plt.figure(figsize=(5.2, 3.4))
    plt.plot(years, actual_cum, label="Cumulative actual Scope 1")
    plt.plot(years, budget_cum, label="Cumulative budget (linear-to-zero)")
    plt.xlabel("Year")
    plt.ylabel("Cumulative MtCO₂")
    plt.title(f"Cumulative emissions vs budget — {label}")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(frameon=False)
    savefig_base(outpath_base)

def maybe_h2_elec(df, label, outdir_base):
    years = df["year"]
    h2_col = next((c for c in df.columns
                   if "hydrogen" in c.lower() and c.lower().endswith(("_t", "_tonnes", "_kt"))), None)
    elec_col = next((c for c in df.columns
                     if ("electricity" in c.lower() or "power_mwh" in c.lower()) and
                        ("demand" in c.lower() or c.lower().endswith("_mwh"))), None)
    if h2_col:
        plt.figure(figsize=(5.2, 3.4))
        plt.plot(years, df[h2_col])
        plt.xlabel("Year")
        plt.ylabel("Hydrogen demand (tonnes)")
        plt.title(f"Hydrogen demand — {label}")
        plt.grid(True, linestyle="--", alpha=0.5)
        savefig_base(os.path.join(outdir_base, f"fig_h2_{label.replace(' ','')}"))
    if elec_col:
        plt.figure(figsize=(5.2, 3.4))
        plt.plot(years, df[elec_col])
        plt.xlabel("Year")
        plt.ylabel("Electricity demand (MWh)")
        plt.title(f"Electricity demand — {label}")
        plt.grid(True, linestyle="--", alpha=0.5)
        savefig_base(os.path.join(outdir_base, f"fig_elec_{label.replace(' ','')}"))


# ---------- Main ----------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nz_csv",   default="detailed_results_NGFS_NetZero2050.csv")
    ap.add_argument("--b2c_csv",  default="detailed_results_NGFS_Below2C.csv")
    ap.add_argument("--ndc_csv",  default="detailed_results_NGFS_NDCs.csv")
    ap.add_argument("--nz_json",  default="summary_NGFS_NetZero2050.json")
    ap.add_argument("--b2c_json", default="summary_NGFS_Below2C.json")
    ap.add_argument("--ndc_json", default="summary_NGFS_NDCs.json")
    ap.add_argument("--outdir",   default="figs_pro")
    args = ap.parse_args()

    outdir = ensure_outdir(args.outdir)

    # Matplotlib defaults for publication look (no custom colors/styles)
    plt.rcParams.update({
        "figure.dpi": 200, "savefig.dpi": 300,
        "font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
        "legend.fontsize": 9, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "figure.autolayout": True, "pdf.fonttype": 42, "ps.fonttype": 42
    })

    scenarios = {
        "NetZero2050": {"label": "NGFS NetZero2050", "csv": args.nz_csv, "json": args.nz_json},
        "Below2C":     {"label": "NGFS Below 2°C",   "csv": args.b2c_csv, "json": args.b2c_json},
        "NDCs":        {"label": "NGFS NDCs",        "csv": args.ndc_csv, "json": args.ndc_json},
    }

    # Load
    dfs = {k: load_df(meta["csv"]) for k, meta in scenarios.items()}
    summaries = {k: safe_json(meta["json"]) for k, meta in scenarios.items()}
    labels = {k: meta["label"] for k, meta in scenarios.items()}

    # 1) Scope 1 by scenario
    fig_scope1_by_scenario(dfs, labels, outdir)

    # 2) Production mix (per scenario)
    for key, meta in scenarios.items():
        fig_production_mix_per_scenario(
            dfs[key], meta["label"], os.path.join(outdir, f"fig_prodmix_{key}")
        )

    # 3) ETS cost by scenario
    fig_ets_cost_by_scenario(dfs, labels, outdir)

    # 4) Cumulative bars (Scope1 & ETS)
    fig_cumulative_bars(dfs, labels, outdir)

    # 5) MAC proxy (ΔNPV vs abatement vs NDCs)
    fig_mac_proxy(dfs, summaries, labels, outdir, ndcs_key="NDCs")

    # 6) Investment timeline markers (per scenario)
    for key, meta in scenarios.items():
        fig_timeline_markers(
            dfs[key], meta["label"], os.path.join(outdir, f"fig_timeline_{key}")
        )

    # 7) Carbon budget vs cumulative emissions (linear-to-zero)
    for key, meta in scenarios.items():
        fig_cum_vs_budget(
            dfs[key], meta["label"], os.path.join(outdir, f"fig_cum_vs_budget_{key}")
        )

    # 8) Hydrogen/Electricity demand (if present)
    for key, meta in scenarios.items():
        maybe_h2_elec(dfs[key], meta["label"], outdir)

    # 9) Robustness: auto-detect extra scenario CSVs (beyond the 3 base)
    extras = sorted(glob.glob("detailed_results_*_*.csv"))
    extras = [p for p in extras if all(tag not in p for tag in ["NetZero2050", "Below2C", "NDCs"])]
    rows = []
    for path in extras:
        df = load_df(path)
        s1 = pick_col(df, ["scope1_emissions_MtCO2", "scope1_MtCO2"])
        ets_col = next((c for c in df.columns if c.lower().startswith("ets") and c.lower().endswith("_usd")), None)
        if not s1:
            continue
        label = os.path.basename(path).replace("detailed_results_", "").replace(".csv", "")
        kpi2050 = float(df.loc[df["year"] == df["year"].max(), s1])
        cumets = float(df[ets_col].sum()/1e9) if ets_col else np.nan
        rows.append((label, kpi2050, cumets))

    if rows:
        lab, v2050, cumets = zip(*rows)
        plt.figure(figsize=(5.2, 3.4))
        plt.bar(lab, v2050)
        plt.xticks(rotation=20, ha="right")
        plt.ylabel("2050 Scope 1 (MtCO₂)")
        plt.title("Robustness: 2050 emissions across extra cases")
        plt.grid(True, axis="y", linestyle="--", alpha=0.5)
        savefig_base(os.path.join(outdir, "fig_robust_2050_scope1"))

        if any(np.isfinite(c) for c in cumets):
            plt.figure(figsize=(5.2, 3.4))
            plt.bar(lab, cumets)
            plt.xticks(rotation=20, ha="right")
            plt.ylabel("Cumulative ETS (B USD)")
            plt.title("Robustness: cumulative ETS across extra cases")
            plt.grid(True, axis="y", linestyle="--", alpha=0.5)
            savefig_base(os.path.join(outdir, "fig_robust_cumETS"))

    print(f"[OK] Figures written to: {os.path.abspath(outdir)}")


if __name__ == "__main__":
    main()