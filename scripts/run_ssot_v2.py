#!/usr/bin/env python3
"""
Reproducible statistical synthesis pipeline (SSOT v2) for:
Electronic Health Record-Based Diagnostic Stewardship to Reduce Antibiotic Use
in Asymptomatic Bacteriuria: A Systematic Review and Meta-Analysis.

Reads locked CSV manifests from data/ and writes results/ssot_v2_results.json.
"""
import csv
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_csv(filename: str):
    with open(DATA_DIR / filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def meta_2x2(studies):
    """Compute FE, RE-DL, RE-PM, RE-REML, and HKSJ (df = k - 1) on log-RR."""
    yi, vi = [], []
    for _sid, ep, np_, ec, nc in studies:
        rr = (ep / np_) / (ec / nc)
        yi.append(math.log(rr))
        vi.append((1.0 / ep - 1.0 / np_) + (1.0 / ec - 1.0 / nc))
    yi = np.array(yi, dtype=float)
    vi = np.array(vi, dtype=float)
    k = len(yi)
    df = k - 1

    wi_fe = 1.0 / vi
    theta_fe = float(np.sum(wi_fe * yi) / np.sum(wi_fe))
    se_fe = math.sqrt(1.0 / float(np.sum(wi_fe)))
    p_fe = float(2.0 * (1.0 - stats.norm.cdf(abs(theta_fe / se_fe))))

    Q = float(np.sum(wi_fe * (yi - theta_fe) ** 2))
    C = float(np.sum(wi_fe) - np.sum(wi_fe ** 2) / np.sum(wi_fe))
    tau2_dl = max(0.0, (Q - df) / C)
    I2 = max(0.0, (Q - df) / Q * 100.0) if Q > 0 else 0.0

    # Paule-Mandel iterative estimator
    tau2_pm = tau2_dl
    for _ in range(200):
        w = 1.0 / (vi + tau2_pm)
        th = float(np.sum(w * yi) / np.sum(w))
        q_pm = float(np.sum(w * (yi - th) ** 2))
        if abs(q_pm - df) < 1e-10:
            break
        dq = float(-np.sum((w ** 2) * (yi - th) ** 2))
        tau2_pm = max(0.0, tau2_pm - (q_pm - df) / dq)

    # REML estimator
    def neg_reml(t2):
        w = 1.0 / (vi + t2)
        th = np.sum(w * yi) / np.sum(w)
        return 0.5 * (np.sum(np.log(vi + t2)) + np.log(np.sum(w)) + np.sum(w * (yi - th) ** 2))

    tau2_reml = float(minimize_scalar(neg_reml, bounds=(0.0, 2.0), method="bounded").x)

    def summarize(tau2):
        w = 1.0 / (vi + tau2)
        theta = float(np.sum(w * yi) / np.sum(w))
        se = math.sqrt(1.0 / float(np.sum(w)))
        p_wald = float(2.0 * (1.0 - stats.norm.cdf(abs(theta / se))))
        q_star = float(np.sum(w * (yi - theta) ** 2) / df)
        se_hksj = math.sqrt(q_star / float(np.sum(w)))
        tcrit = float(stats.t.ppf(0.975, df))
        p_hksj = float(2.0 * (1.0 - stats.t.cdf(abs(theta / se_hksj), df)))
        return {
            "tau2": round(tau2, 5),
            "RR": round(math.exp(theta), 4),
            "ci_wald": [round(math.exp(theta - 1.96 * se), 4), round(math.exp(theta + 1.96 * se), 4)],
            "p_wald": round(p_wald, 5),
            "ci_hksj": [round(math.exp(theta - tcrit * se_hksj), 4), round(math.exp(theta + tcrit * se_hksj), 4)],
            "p_hksj": round(p_hksj, 5),
            "weights_pct": [round(float(x / np.sum(w) * 100.0), 1) for x in w],
        }

    return {
        "k": k,
        "Q": round(Q, 4),
        "I2": round(I2, 2),
        "FE": {
            "RR": round(math.exp(theta_fe), 4),
            "ci": [round(math.exp(theta_fe - 1.96 * se_fe), 4), round(math.exp(theta_fe + 1.96 * se_fe), 4)],
            "p": round(p_fe, 5),
        },
        "DL": summarize(tau2_dl),
        "PM": summarize(tau2_pm),
        "REML": summarize(tau2_reml),
    }


def main():
    roster = load_csv("03_Study_Roster.csv")
    sb = load_csv("05_StratumB_Diagnostic_ITS.csv")
    sc = load_csv("06_StratumC_Safety_Balancing.csv")
    rob = load_csv("07_Risk_of_Bias.csv")

    inc_ids = {r["Study_ID"] for r in roster if r["Study_ID"].startswith("S") and "Finalized" in r["Extraction_Status"]}
    assert len(inc_ids) == 43, f"Expected 43 included studies, got {len(inc_ids)}"
    roster_map = {r["Study_ID"]: r for r in roster}

    # Stratum A verified 2x2 counts (Pre vs Post confirmed ASB)
    k4 = [
        ("S01", 139, 331, 307, 572),
        ("S06", 24, 34, 41, 58),
        ("S07", 38, 100, 57, 104),
        ("S11", 61, 100, 70, 100),
    ]
    k5 = k4 + [("S30", 3, 4, 6, 9)]

    loo = {f"omit_{k4[i][0]}": meta_2x2([s for j, s in enumerate(k4) if j != i]) for i in range(4)}

    # Stratum B sign tests
    sb_inc = [r for r in sb if r["Study_ID"] in inc_ids]
    sb_strict29 = [r for r in sb_inc if roster_map[r["Study_ID"]]["Include_Primary_Counts"] == "Yes"]
    sb_perstratum30 = [r for r in sb_inc if roster_map[r["Study_ID"]]["Include_Primary_Counts"] == "Yes" or r["Study_ID"] == "S20"]

    def sign_test(rows):
        fav = sum(1 for r in rows if "Favors" in r["Effect_Direction"])
        n = len(rows)
        p2 = float(stats.binomtest(fav, n, 0.5, alternative="two-sided").pvalue)
        return {"favors": fav, "n": n, "pct": round(fav / n * 100.0, 1), "p_two_sided": round(p2, 5)}

    # Risk of Bias & COVID-19 overlap (from updated SSOT Tab 07)
    rob_inc = [r for r in rob if r["Study_ID"] in inc_ids]
    epoc_counts = Counter(r["Overall_RoB_Judgment"] for r in rob_inc if r["Assigned_RoB_Tool"] == "EPOC_ITS")
    robins_counts = Counter(r["Overall_RoB_Judgment"] for r in rob_inc if r["Assigned_RoB_Tool"] == "ROBINS-I")
    covid_epoc = sum(1 for r in rob_inc if r["Assigned_RoB_Tool"] == "EPOC_ITS" and r.get("COVID_Overlap_YN") == "Yes")
    covid_robins = sum(1 for r in rob_inc if r["Assigned_RoB_Tool"] == "ROBINS-I" and r.get("COVID_Overlap_YN") == "Yes")

    # Stratum C counts
    sc_inc = [r for r in sc if r["Study_ID"] in inc_ids]
    pyelo_monitored = sum(
        1 for r in sc_inc
        if r.get("Pyelonephritis_Outcome", "").strip()
        and not r["Pyelonephritis_Outcome"].strip().startswith("NR")
        and r["Pyelonephritis_Outcome"].strip() != "None Observed"
    )

    results = {
        "n_included": len(inc_ids),
        "stratum_a_k4": meta_2x2(k4),
        "stratum_a_k5": meta_2x2(k5),
        "stratum_a_loo": loo,
        "stratum_b_perstratum30": sign_test(sb_perstratum30),
        "stratum_b_strict29": sign_test(sb_strict29),
        "stratum_b_all38": sign_test(sb_inc),
        "stratum_c": {"total": len(sc_inc), "pyelonephritis_monitored": pyelo_monitored},
        "rob_epoc_its_n21": dict(epoc_counts),
        "rob_robins_i_n22": dict(robins_counts),
        "covid_overlap": {
            "epoc_its": covid_epoc,
            "robins_i": covid_robins,
            "total": covid_epoc + covid_robins,
            "pct": round((covid_epoc + covid_robins) / len(inc_ids) * 100.0, 1),
        },
    }

    out_path = RESULTS_DIR / "ssot_v2_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Verified SSOT v2 pipeline complete -> {out_path}")
    print(f"  Stratum A k=4 RE-DL: RR {results['stratum_a_k4']['DL']['RR']} ({results['stratum_a_k4']['DL']['ci_wald']}), HKSJ p={results['stratum_a_k4']['DL']['p_hksj']}")
    print(f"  Stratum B per-stratum: {results['stratum_b_perstratum30']['favors']}/{results['stratum_b_perstratum30']['n']} (p={results['stratum_b_perstratum30']['p_two_sided']})")
    print(f"  Stratum C pyelonephritis monitored: {pyelo_monitored}/{len(sc_inc)}")
    print(f"  RoB: EPOC-ITS={sum(epoc_counts.values())} {dict(epoc_counts)} | ROBINS-I={sum(robins_counts.values())} {dict(robins_counts)}")
    print(f"  COVID-19 overlap: {results['covid_overlap']['total']}/43 ({results['covid_overlap']['pct']}%)")


if __name__ == "__main__":
    main()
