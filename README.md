# DV_Tableau

Tableau Data Visualization Assignment — *The effect of gun laws on gun violence in the United States*

**Author:** Itziar Morales Rodríguez

---

## Project Structure

```
DV_Tableau/
├── data/               # Raw datasets (.tab and .xlsx)
├── docs/               # LaTeX report source (report.tex + report.bib)
├── figures/            # Exported chart images referenced in the report
├── videolink.txt       # Link to the submission video
└── README.md
```

---

## Datasets

| Dataset | Format | Source | Grain |
|---|---|---|---|
| Firearm Suicide Proxy for Household Gun Ownership, 1949–2023 | `.tab` | [Harvard Dataverse — doi:10.7910/DVN/QVYDUD](https://doi.org/10.7910/DVN/QVYDUD) | State × Year |
| State Firearm Law Database, 1976–2024 | `.xlsx` | [Tufts CTSI — statefirearmlaws.org](https://www.tuftsctsi.org/state-firearm-laws/) | State × Year |

Both datasets are joined in Tableau on `state` + `year`. The effective analysis window is **1976–2023**.

---

## Research Questions

1. Is the combination of high estimated gun ownership and few firearm laws associated with higher firearm homicide and suicide rates?
2. How has the gap in firearm violence rates between high-law and low-law states changed over time?
3. When states increase the number of firearm laws, do firearm homicide and suicide rates change in subsequent years?

---

## Report

The full written report is in `docs/report.tex`. Compile with:

```bash
pdflatex report.tex
biber report
pdflatex report.tex
pdflatex report.tex
```

---

## Video

See `videolink.txt` for the submission video link.
