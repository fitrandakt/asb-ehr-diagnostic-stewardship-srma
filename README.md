# EHR-Based Diagnostic Stewardship for Asymptomatic Bacteriuria (SRMA)

Reproducible datasets, statistical synthesis scripts (Python & R `metafor`), protocol archive, and 300 dpi publication figures for:

> **Electronic Health Record-Based Diagnostic Stewardship to Reduce Antibiotic Use in Asymptomatic Bacteriuria: A Systematic Review and Meta-Analysis**  
> Fitranda Kusiyanto Taslim, Reinaldi Septiawan Azhar, Stefia Aisyah Amini — Faculty of Medicine, Universitas Jember, Indonesia.

## Key Summary (SSOT v2 — 43 Verified Studies)

- **Search & Selection (PRISMA 2020):** 876 raw records across 6 executed databases (Google Scholar 279, Scopus 266, PubMed/MEDLINE 140, EBSCOhost 133, ScienceDirect 52, Cochrane Library 6) + citation chaining → 68 full-text reports sought → 7 unretrievable paywalled excluded (PRISMA 16a) → 61 assessed → 18 excluded (PICOS) → **43 included studies** (34 corpus-level independent adult cohorts; 8 institutional lineages mapped including `L8_Duke` and per-stratum `L2_UNMC`).
- **Stratum A (Confirmed-ASB Prescribing, k = 4 primary 2×2):** RE-DL **RR 0.826 (95% CI 0.730–0.934; p = 0.0022; I² = 23.0%)**; small-sample HKSJ-DL **0.673–1.013 (p = 0.0587)**; sensitivity k = 5 (+S30) HKSJ-DL **RR 0.831 (0.705–0.979; p = 0.0348)**; LOO omitting S01 **RR 0.856 (0.713–1.028; p = 0.0955)**.
- **Stratum B (Diagnostic Stewardship / SWiM):** **22/30 (73.3%)** per-stratum independent adult cohorts favored intervention (two-sided exact binomial sign test **p = 0.0161**; strict corpus-level 21/29 [72.4%], p = 0.0241); median overall urine culture reduction **41.2% (IQR 32.0%–47.1%)**.
- **Stratum C (Safety & Compensatory Shifts):** 0/23 net clinical harm signals (explicit pyelonephritis monitoring in **2/23** cohorts; GRADE certainty **Low**); 6 recurring compensatory workaround patterns documented (**Moderate** certainty).
- **Risk of Bias & COVID-19 Overlap:** **21 Cochrane EPOC-ITS** (1 Low [`S13 Keintz 2026`], 11 Moderate, 9 High) and **22 ROBINS-I** (4 Moderate, 17 Serious, 1 Critical [`S09 Lewis 2023`]); COVID-19 temporal overlap **23/43 (53.5%)**.

## Repository Structure

```text
├── data/               # Locked consensus extraction manifests (Tabs 01–07 CSV)
├── scripts/            # Portable Python (SciPy/Matplotlib) & R (metafor) replication scripts
├── results/            # Machine-readable verified statistical outputs (ssot_v2_results.json)
├── figures/            # Publication-grade 300 dpi PNG figures (Figures 1–4)
├── docs/               # Study Protocol v1.0 archive
├── CITATION.cff        # Machine-readable citation metadata (GitHub / Zenodo)
└── LICENSE             # MIT (code) / CC BY 4.0 (curated data & figures)
```

*Note: Publisher-copyrighted primary study PDFs are intentionally excluded from this public repository; all 43 included studies are uniquely identified by PMID, PMCID, and DOI in `data/03_Study_Roster.csv`.*

## Reproducibility Instructions

### Python
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 scripts/run_ssot_v2.py
python3 scripts/generate_figures.py
```

### R (`metafor`)
```bash
Rscript scripts/replicate_metafor.R
```
