# R (metafor) Replication Script for Stratum A Conditional Meta-Analysis & Stratum B Sign Test
# Package requirement: install.packages("metafor")

library(metafor)

# 1. Primary Stratum A (k = 4 independent adult cohorts)
dat_k4 <- data.frame(
  study = c("S01 Ammar 2026", "S06 Caveness 2024", "S07 Belk 2023", "S11 Osiemo 2021"),
  ai = c(139, 24, 38, 61),   # Post-intervention ASB antibiotic events
  n1i = c(331, 34, 100, 100),
  ci = c(307, 41, 57, 70),   # Pre-intervention ASB antibiotic events
  n2i = c(572, 58, 104, 100)
)
es_k4 <- escalc(measure = "RR", ai = ai, n1i = n1i, ci = ci, n2i = n2i, data = dat_k4)

res_fe       <- rma(yi, vi, data = es_k4, method = "FE")
res_dl       <- rma(yi, vi, data = es_k4, method = "DL")
res_dl_hksj  <- rma(yi, vi, data = es_k4, method = "DL", test = "knha")
res_reml     <- rma(yi, vi, data = es_k4, method = "REML")
res_reml_hk  <- rma(yi, vi, data = es_k4, method = "REML", test = "knha")

print(predict(res_dl, transf = exp, digits = 3))
print(predict(res_dl_hksj, transf = exp, digits = 3))
print(predict(res_reml_hk, transf = exp, digits = 3))
print(leave1out(res_dl, transf = exp, digits = 3))

# 2. Sensitivity Stratum A (k = 5 adding S30 Winkler 2023 CABG Pre-Op)
dat_k5 <- rbind(dat_k4, data.frame(study = "S30 Winkler 2023", ai = 3, n1i = 4, ci = 6, n2i = 9))
es_k5 <- escalc(measure = "RR", ai = ai, n1i = n1i, ci = ci, n2i = n2i, data = dat_k5)
print(predict(rma(yi, vi, data = es_k5, method = "DL", test = "knha"), transf = exp, digits = 3))

# 3. Stratum B Exact Two-Sided Binomial Sign Tests
print(binom.test(22, 30, p = 0.5, alternative = "two.sided")) # Per-stratum independent adult (incl. L2_UNMC S20)
print(binom.test(21, 29, p = 0.5, alternative = "two.sided")) # Strict corpus-level independent adult
