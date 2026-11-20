import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["axes.linewidth"] = 0.8

from pathlib import Path
OUT_DIR = str(Path(__file__).resolve().parent.parent / "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ==========================================
# FIGURE 1: PRISMA 2020 FLOW DIAGRAM
# ==========================================
fig, ax = plt.subplots(figsize=(10.5, 8.2), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

def box(x, y, w, h, text, fc="#F8FAFC", ec="#1E3A5F", lw=1.2, fs=8.5, bold_first=False, ha="center"):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.3,rounding_size=1.0",
                                  facecolor=fc, edgecolor=ec, linewidth=lw)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha=ha, va="center", fontsize=fs, color="#111827",
            linespacing=1.35, fontweight="bold" if bold_first else "normal")

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#1E3A5F", lw=1.3, mutation_scale=12))

# Title
ax.text(50, 97.5, "Figure 1. PRISMA 2020 Flow Diagram — EHR Diagnostic Stewardship for Asymptomatic Bacteriuria",
        ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")

# Phase labels on left
for y0, h0, lbl in [(76, 17, "Identification"), (36, 37, "Screening"), (6, 27, "Included")]:
    rect = patches.FancyBboxPatch((1.5, y0), 4.5, h0, boxstyle="round,pad=0.2,rounding_size=0.8",
                                  facecolor="#1E3A5F", edgecolor="#1E3A5F")
    ax.add_patch(rect)
    ax.text(3.75, y0 + h0/2, lbl, ha="center", va="center", rotation=90, color="white", fontsize=9, fontweight="bold")

# Identification
box(9, 77, 43, 15.5,
    "Records identified from 6 electronic databases (n = 876):\n"
    "• Google Scholar (n = 279)   • Scopus (n = 266)\n"
    "• PubMed/MEDLINE (n = 140)   • EBSCOhost (n = 133)\n"
    "• ScienceDirect (n = 52)     • Cochrane Library (n = 6)",
    fc="#EFF6FF")
box(56, 77, 41, 15.5,
    "Records identified via other methods:\n"
    "• Backward & forward citation chaining of\n"
    "  included studies and prior SRs (Hojat 2023;\n"
    "  Humphrey 2023) & PMC grey-lit abstracts",
    fc="#EFF6FF")

arrow(30.5, 77, 30.5, 72.5)
arrow(76.5, 77, 76.5, 72.5)

# Screening - Candidate Pool
box(9, 61.5, 43, 10.5,
    "Records deduplicated, title/abstract screened,\n"
    "and merged with citation-chaining candidates\n"
    "→ Reports sought for full-text retrieval (n = 68)",
    fc="#F8FAFC")
box(56, 61.5, 41, 10.5,
    "Reports not retrieved (PRISMA 16a; n = 7):\n"
    "• Subscription/paywalled full texts unavailable\n"
    "  (S12 Rico, S22 Smith, S23 Sansom, S28 Pham,\n"
    "  S31 Penney, S45 Khachatryan, S49 Caroff)",
    fc="#FEF2F2", ec="#991B1B")

arrow(52, 66.7, 56, 66.7)
arrow(30.5, 61.5, 30.5, 55)

# Eligibility
box(9, 41, 43, 13.5,
    "Reports assessed for full-text eligibility\n"
    "(n = 61)\n"
    "Dual-reviewer PICOS verification & PDF audit\n"
    "(misfiled PDFs quarantined; Appendix 8)",
    fc="#F8FAFC")
box(56, 39, 41, 16.5,
    "Reports excluded after full-text review (n = 18):\n"
    "• Non-electronic / manual intervention only (n = 8)\n"
    "• Single-arm uncontrolled audit / no comparator (n = 5)\n"
    "• Pediatric-only or wrong clinical target (n = 3)\n"
    "• Theoretical simulation / non-isolated bundle (n = 2)",
    fc="#FEF2F2", ec="#991B1B")

arrow(52, 47.5, 56, 47.5)
arrow(30.5, 41, 30.5, 33)

# Included
box(9, 7, 88, 25.5,
    "Studies included in finalized systematic review (n = 43)\n"
    "• Corpus-level deduplication: 34 independent adult cohorts | 5 linked institutional duplicates | 3 mixed-age sensitivity | 1 grey-lit abstract\n"
    "• Per-stratum independent adult cohorts (including L2_UNMC S20 in Strata B & C; L8_Duke mapped):\n"
    "    – Stratum A (Confirmed-ASB prescribing): n = 12 total (11 independent adult; k = 4 primary 2×2 meta-analysis; k = 5 sensitivity)\n"
    "    – Stratum B (Diagnostic urine-culture stewardship / ITS): n = 38 total (30 per-stratum independent adult; 29 strict corpus-level)\n"
    "    – Stratum C (Safety & compensatory workarounds): n = 23 total (20 per-stratum independent adult; 2/23 monitored pyelonephritis)\n"
    "• Design-routed Risk of Bias: 21 EPOC-ITS (1 Low, 11 Moderate, 9 High) | 22 ROBINS-I (4 Moderate, 17 Serious, 1 Critical)",
    fc="#ECFDF5", ec="#065F46", fs=8.3)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Figure1_PRISMA2020.png"), dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

# ==========================================
# FIGURE 2: FOREST PLOT STRATUM A (k=4 + SENSITIVITIES)
# ==========================================
fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)

labels = [
    "S01 Ammar et al. (2026)\n[BPA + BPAN; Pre 307/572 vs Post 139/331]",
    "S06 Caveness et al. (2024)\n[Reflex >50K; Pre 41/58 vs Post 24/34]",
    "S07 Belk et al. (2023)*\n[<100K CFU, >72h; Pre 57/104 vs Post 38/100]",
    "S11 Osiemo et al. (2021)\n[UNMC Order/Edu; Pre 70/100 vs Post 61/100]",
    "Primary Pooled RE-DL (k = 4; I² = 23.0%)",
    "Primary Pooled RE-REML (Wald, k = 4)",
    "Primary Pooled HKSJ-DL (df = 3; small-sample)",
    "Primary Pooled HKSJ-REML (df = 3; small-sample)",
    "Sensitivity k = 5 (+S30 CABG) RE-DL / HKSJ-DL",
    "Leave-One-Out: Omit S01 (k = 3, RE-DL)",
    "Leave-One-Out: Omit S07 (<100K; k = 3, RE-DL)"
]
rrs  = [0.782, 0.999, 0.693, 0.871, 0.826, 0.823, 0.826, 0.823, 0.831, 0.856, 0.848]
los  = [0.677, 0.761, 0.509, 0.708, 0.730, 0.739, 0.673, 0.677, 0.705, 0.713, 0.746]
his  = [0.905, 1.310, 0.944, 1.072, 0.934, 0.916, 1.013, 0.999, 0.979, 1.028, 0.964]
wts  = ["41.7%", "17.4%", "14.0%", "26.9%", "100%", "100%", "100%", "100%", "k=5", "k=3", "k=3"]
pvals= ["0.001", "0.99", "0.020", "0.19", "0.0022", "0.0004", "0.0587", "0.0496", "0.0348*", "0.0955", "0.0116"]

y_pos = np.arange(len(labels))[::-1]

ax.axvline(1.0, color="#6B7280", linestyle="--", linewidth=1.1, zorder=1)
ax.axhline(6.5, color="#CBD5E1", linestyle="-", linewidth=0.9)
ax.axhline(2.5, color="#CBD5E1", linestyle=":", linewidth=0.9)

for i, (y, rr, lo, hi, wt, pv) in enumerate(zip(y_pos, rrs, los, his, wts, pvals)):
    is_study = i < 4
    is_hksj_ns = i in (6, 9)
    col = "#1D4ED8" if is_study else ("#B91C1C" if is_hksj_ns else "#047857")
    if is_study:
        ax.errorbar(rr, y, xerr=[[rr-lo], [hi-rr]], fmt="s", color=col, markersize=6.5, capsize=3, lw=1.6, zorder=3)
    else:
        # diamond-like marker + CI bar
        ax.errorbar(rr, y, xerr=[[rr-lo], [hi-rr]], fmt="D", color=col, markersize=6.5, capsize=3, lw=1.8, zorder=3)
    ci_str = f"{rr:.3f} ({lo:.3f}–{hi:.3f})   p={pv}"
    ax.text(1.37, y, ci_str, va="center", ha="left", fontsize=8.2,
            fontweight="bold" if i in (4, 6) else "normal", color=col if not is_study else "#111827")

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8.3)
ax.set_xscale("log")
ax.set_xlim(0.45, 1.35)
ax.set_xticks([0.5, 0.7, 0.85, 1.0, 1.25])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xlabel("Risk Ratio (RR, log scale) — Favors EHR Stewardship (< 1.0) vs. Favors Control (> 1.0)", fontsize=9, fontweight="bold")
ax.set_title("Figure 2. Conditional Meta-Analysis & Small-Sample Sensitivity (Stratum A: Confirmed-ASB Antibiotic Prescribing)",
             fontsize=10, fontweight="bold", pad=12, loc="left")
ax.text(1.37, 10.65, "RR (95% CI)   Two-sided p", fontsize=8.5, fontweight="bold", color="#0F172A")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.text(0.01, -0.02, "*S07 Belk (2023) evaluated low-burden bacteriuria (<100,000 CFU/mL) with >72h continuation; Sensitivity k=5 displays HKSJ-DL CI (RE-DL: 0.831 [0.741–0.932], p=0.0016).",
         fontsize=7.5, color="#4B5563", style="italic")

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Figure2_ForestPlot_StratumA.png"), dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

# ==========================================
# FIGURE 3: STRATUM B EFFECT DIRECTION & % REDUCTIONS
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.2), dpi=300, gridspec_kw={"width_ratios": [1.0, 1.35]})

# Panel A: Effect direction breakdown (Per-stratum n=30 vs Strict n=29 vs All n=38)
cats = ["Per-Stratum Indep.\nAdult (n = 30)\np = 0.0161", "Strict Corpus-Level\nIndep. (n = 29)\np = 0.0241", "All Finalized\nStratum B (n = 38)\np = 0.0005*"]
fav = np.array([22, 21, 30])
mix = np.array([4, 4, 4])
nul = np.array([4, 4, 4])
x = np.arange(len(cats))
w = 0.52

p1 = ax1.bar(x, fav, w, label="Favors EHR Stewardship", color="#059669")
p2 = ax1.bar(x, mix, w, bottom=fav, label="Mixed Across Settings", color="#D97706")
p3 = ax1.bar(x, nul, w, bottom=fav+mix, label="Null / NS", color="#9CA3AF")

for i in range(len(cats)):
    ax1.text(x[i], fav[i]/2, f"{fav[i]} ({fav[i]/(fav[i]+mix[i]+nul[i])*100:.1f}%)", ha="center", va="center", color="white", fontweight="bold", fontsize=8.5)
    ax1.text(x[i], fav[i]+mix[i]/2, f"{mix[i]}", ha="center", va="center", color="white", fontweight="bold", fontsize=8)
    ax1.text(x[i], fav[i]+mix[i]+nul[i]/2, f"{nul[i]}", ha="center", va="center", color="#111827", fontweight="bold", fontsize=8)

ax1.set_xticks(x)
ax1.set_xticklabels(cats, fontsize=8.3)
ax1.set_ylabel("Number of Studies / Cohorts", fontsize=9, fontweight="bold")
ax1.set_title("A. Effect Direction (Exact Binomial Sign Test)", fontsize=9.5, fontweight="bold")
ax1.legend(loc="upper left", fontsize=7.8, frameon=True)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Panel B: Relative % Urine Culture Reductions (Per-stratum independent cohorts reporting %, sorted)
studies_pct = [
    ("S19 Yogo 2025 (Reflex)", 85.4, "Favors"),
    ("S30 Winkler 2023 (Order Set)", 76.5, "Favors"),
    ("S35 Howard-Anderson 2020 (Reflex)", 75.6, "Favors"),
    ("S18 Suleyman 2026 (Hard-Stop)", 59.0, "Favors"),
    ("S32 Kalorin 2022 (BPA+Reflex)", 57.0, "Favors"),
    ("S20 Torres 2025 (UNMC ITS)", 55.0, "Favors"),
    ("S37 Shimoni 2020 (Hard-Stop)", 53.5, "Favors"),
    ("S02 Qin 2026 (Triage Calc)", 51.0, "Favors"),
    ("S14 Luu 2026 (Remove Standing)", 46.3, "Favors"),
    ("S41 Munigala 2018 (Order Set)", 45.3, "Favors"),
    ("S06 Caveness 2024 (Reflex)", 43.5, "Favors"),
    ("S21 Berger 2025 (Remove Reflex)", 42.0, "Favors"),
    ("S34 Watson 2020 (BPA+Order)", 40.4, "Favors"),
    ("S17 Claeys 2026 (Hybrid CDS)", 39.5, "Mixed"),
    ("S38 Coughlin 2020 (Reflex)", 39.1, "Favors"),
    ("S36 Lynch 2020 (Reflex)", 39.0, "Mixed"),
    ("S43 Shirley 2017 (BPA)", 34.0, "Favors"),
    ("S27 Nix 2024 (Order Set)", 33.0, "Mixed"),
    ("S16 Ostrowski 2026 (Null ITS)", 31.6, "Null"),
    ("S26 Stensgard 2024 (Reflex)", 26.0, "Mixed"),
    ("S29 Krouss 2023 (BPA)", 20.9, "Favors"),
    ("S05 Strebe 2025 (Reflex)", 20.3, "Favors"),
    ("S03 Alghamdi 2025 (CDS)", 12.5, "Favors"),
    ("S42 Keller 2018 (BPA)", 10.2, "Favors"),
]
vals = [v for _, v, _ in studies_pct]
med_all = np.median(vals)
q25, q75 = np.percentile(vals, [25, 75])

y2 = np.arange(len(studies_pct))[::-1]
colors2 = ["#059669" if s == "Favors" else ("#D97706" if s == "Mixed" else "#9CA3AF") for _, _, s in studies_pct]
ax2.barh(y2, vals, color=colors2, height=0.72, alpha=0.9)
ax2.axvline(med_all, color="#1E3A5F", linestyle="--", lw=1.3, label=f"Median: {med_all:.1f}% (IQR {q25:.1f}%–{q75:.1f}%)")
ax2.axvspan(q25, q75, color="#1E3A5F", alpha=0.08)
ax2.set_yticks(y2)
ax2.set_yticklabels([n for n, _, _ in studies_pct], fontsize=7.0)
ax2.set_xlabel("Relative Reduction in Urine Culture Volume / Rate (%)", fontsize=8.8, fontweight="bold")
ax2.set_title("B. Reported Relative Reductions (n = 24 Per-Stratum Indep. Cohorts)", fontsize=9.5, fontweight="bold")
ax2.legend(loc="lower right", fontsize=7.8, frameon=True)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.suptitle("Figure 3. Stratum B Diagnostic Stewardship Outcomes (SWiM Synthesis)", fontsize=10.5, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Figure3_EffectDirection_StratumB.png"), dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

# ==========================================
# FIGURE 4: DESIGN-ROUTED RISK OF BIAS (EPOC-ITS n=21 & ROBINS-I n=22)
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.6), dpi=300)

# EPOC-ITS (n=21)
epoc_lbls = ["Low\n(S13 Keintz)", "Moderate", "High"]
epoc_vals = [1, 11, 9]
epoc_cols = ["#10B981", "#F59E0B", "#EF4444"]
bars1 = ax1.bar(epoc_lbls, epoc_vals, color=epoc_cols, width=0.55, edgecolor="#1F2937", lw=0.7)
for b, v in zip(bars1, epoc_vals):
    ax1.text(b.get_x() + b.get_width()/2, v + 0.35, f"{v} ({v/21*100:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax1.set_ylim(0, 14)
ax1.set_ylabel("Number of Studies", fontsize=9, fontweight="bold")
ax1.set_title("A. Cochrane EPOC-ITS (n = 21 ITS Studies)\nCOVID-19 Overlap: 7/21 (33.3%)", fontsize=9.5, fontweight="bold")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# ROBINS-I (n=22)
rob_lbls = ["Low", "Moderate", "Serious", "Critical\n(S09 Lewis)"]
rob_vals = [0, 4, 17, 1]
rob_cols = ["#10B981", "#F59E0B", "#EA580C", "#991B1B"]
bars2 = ax2.bar(rob_lbls, rob_vals, color=rob_cols, width=0.55, edgecolor="#1F2937", lw=0.7)
for b, v in zip(bars2, rob_vals):
    ax2.text(b.get_x() + b.get_width()/2, v + 0.4, f"{v} ({v/22*100:.1f}%)", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax2.set_ylim(0, 21)
ax2.set_ylabel("Number of Studies", fontsize=9, fontweight="bold")
ax2.set_title("B. ROBINS-I (n = 22 Non-ITS Studies)\nCOVID-19 Overlap: 16/22 (72.7%)", fontsize=9.5, fontweight="bold")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.suptitle("Figure 4. Design-Routed Risk of Bias Summary Across All 43 Included Studies (Total COVID-19 Overlap: 23/43 [53.5%])",
             fontsize=10.2, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "Figure4_RoB_Summary.png"), dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print("Generated all 4 publication-grade 300 dpi figures in", OUT_DIR)
