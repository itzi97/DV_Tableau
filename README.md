# DV_Tableau

Tableau Data Visualization Assignment — *State-level household gun prevalence and ATF traced firearm patterns in the U.S.*

**Author:** Itziar Morales Rodríguez

---

## Project Structure

```
DV_Tableau/
├── data/               # Raw and processed CSV datasets
├── docs/               # LaTeX report source (report.tex + report.bib)
├── figures/            # Exported chart images referenced in the report
├── videolink.txt       # Link to the submission video
└── README.md
```

---

## Datasets

| Dataset | Source | Grain |
|---|---|---|
| State-Level Household Gun Ownership Proxy, 1949–2020 | [Harvard Dataverse](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/QVYDUD) | State × Year |
| ATF Gun Traces by State and Firearm Type, 2014–2023 | [The Trace / Gun Violence Data Hub](https://datahub.thetrace.org/dataset/atf-gun-traces-data/) | State × Year × Type |

Both datasets are joined in Tableau on `state` + `year`. The effective analysis window is **2014–2020**.

---

## Research Questions

1. How has estimated household gun prevalence varied by state over time?
2. What firearm types dominate ATF trace summaries by state?
3. Do states with higher estimated gun prevalence show different traced firearm type patterns?

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
