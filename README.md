# Device Exploration for On-Chip Detection on Lithium Niobate and Amplification on Silicon for Scalable Integrated Photonics

**Vemparala Lakshmi Pravallika**  
B.Tech., Indian Institute of Technology Bombay (2024)  

Program in Media Arts and Sciences, School of Architecture and Planning  
Massachusetts Institute of Technology  

Master of Science in Media Arts and Sciences · submitted **15 May 2026**  

**Thesis supervisor:** Dirk Englund — Professor of Electrical Engineering and AI + Decision-making, MIT EECS  
**Committee:** Dirk Englund, Joseph Paradiso, Jelena Notaros  

**Typeset thesis (author copy):** `C:\Users\prava\OneDrive\Desktop\Thesis.pdf` — section and figure references below refer to this document (86 pages, May 2026).

**Title variant on the committee certification page:** *Device Exploration for High-Efficiency On-Chip Detection in TFLN and Heterogeneous Gain Integration on Si for Scalable Integrated Photonics* — an extended formulation on the signature page; the **title page** uses the shorter title above.

---

## Abstract (as submitted)

Passive photonic integrated circuits excel at routing and modulating light, but generation and detection still rely on heterogeneous integration of foreign active materials. Bonding, epitaxy, flip-chip, and micro-transfer printing dominate how industry and research labs attach III–V detectors, amplifiers, and lasers to substrate hosts. An important bottleneck is the active–passive interface: coupling efficiency, alignment, and yield.

This thesis contributes two complementary demonstrations on leading passive platforms. Project 1 targets efficient telecom-band photodetection on thin-film lithium niobate. Lithographic adiabatic tapers to an absorber are the established route; here a doubly-clamped rib waveguide is selectively underetched and buckled so that a mechanical air gap drives the same adiabatic transition. Modeling predicts waveguide-to-absorber coupling near unity and total quantum efficiency near ninety-six percent for the coupled-mode design. A fiber-coupled test bench was built to characterize transmission and to separate the evanescent path from parasitic paths; a successor layout will suppress the dominant parasitic channel by geometry.

Project 2 targets optical gain on silicon using micro-transfer printing: a GaAs quantum-dot nanobeam with a 1D photonic-crystal cavity is placed on a silicon taper so that the signal transfers vertically to the III–V and is amplified by donor material. The workflow from donor release through stamp alignment and confocal pump delivery was implemented end-to-end, with several chiplets aligned within the taper tolerance for follow-on characterization.

Taken together, the work advances reusable recipes for high-efficiency detection on TFLN and compact gain on silicon spanning coherent links, switches, sensing, and integrated nonlinear and quantum photonics.

---

## How this repository folder ties to the thesis

The experiments behind **Chip 2** are documented in **Chapter 3 (Methods)** and **Chapter 4 (Results and Discussion)**, especially **§3.3.5** (waveguide-to-detector coupling measurements), **§4.1.2** (detector-signal contamination), **§4.1.3** (operating wavelength from the loopback wavelength sweep), and **§4.1.4** (two-dimensional free-space coupling model).

In the thesis text, **Chip 2 carried 25 loopback structures**. The chip was cleaved along crystallographic planes, but a **fabrication step error** meant the loopback waveguides were **not aligned** with those planes. Facets were not uniformly perpendicular to propagation; some structures cleaved obliquely or did not reach the edge. **Sixteen structures** had **viable facets** for fiber coupling.

To quantify how **facet parallelism** affects coupling, those sixteen structures were measured in two arrangements (**§3.3.5**):

- **Configuration 1 (angled interfaces):** the fiber array stays parallel to the chip \(x\)-direction; the two facets are not parallel to each other, and each structure required **independent 3D alignment** (including angular adjustment).
- **Configuration 2 (parallel interfaces):** the chip is rotated so **input and output facets are parallel**, while waveguides are tilted by **\(\sim 1^\circ\)** relative to the fiber array; a **single alignment** can optimize both interfaces and served as the **baseline** for the loopback transmission campaign.

The wavelength campaign scanned **1480–1600 nm** (1/3 nm steps, **0 dBm** input, dwell per wavelength) across all sixteen viable loopbacks, recording detector output versus wavelength (**§4.1.3**). Peak transmission clusters near **\(\lambda \approx 1595\) nm**, which the thesis adopts as the **operating wavelength** for subsequent fiber-to-detector and contamination studies (see **Fig. 4.2** and the narrative around **Fig. 4.5**).

The materials in **`Github uploads`** are the **layout, simulation, raw sweep exports, and Python/Jupyter tooling** used alongside that Chip 2 campaign—including **GDSFactory** loopback layout work related to **Fig. 3.11** (Chip 2 loopback GDS) and later layout iterations, **COMSOL** strip-waveguide modeling, and the **`sweep_*.csv`** archives plus scripts that normalize filenames and summarize spectra.

---

## What this folder is for

This directory is meant to make the **Chip 2 measurement pipeline** and **related layout/simulation artifacts** **inspectable and reproducible**: regenerate plots, re-parse CSVs, or revisit mask geometry without hunting through scattered paths. It is **not** a full export of the Overleaf thesis project; the canonical narrative and figures remain in **`Thesis.pdf`** (and the official MIT deposit when available).

---

## Contents (by subfolder)

| Subfolder | Role |
|-----------|------|
| **`GDS/`** | **GDSFactory** notebook **`loopback chip iteration 4.ipynb`**: parameters and routing for **loopback** test structures (etch sweeps, strip cross-section, layers). Aligns with the **Chip 2 loopback layout** thread in the thesis (see **Fig. 3.11** and related discussion). |
| **`COMSOL Sim/`** | **COMSOL Multiphysics** strip-waveguide model (working `.mph`). A **`.mph.lock`** file may appear while COMSOL has the model open; it is not part of the physics definition. |
| **`Chip 2 measurements/`** | **Raw wavelength–power CSV sweeps** for the sixteen viable loopbacks, plus scripts to **rename** files consistently, **aggregate** maxima, and **plot** summaries. |

---

## `GDS/` — layout notebook

Open **`GDS/loopback chip iteration 4.ipynb`** in Jupyter. It activates **`gdsfactory`** with the **generic PDK**, sets strip width and **127 µm** pitch, defines routing constants for tiled loopbacks, sweeps etch parameters (length, width, gap), and assigns waveguide / box layers. Run cells sequentially and export **GDS/OASIS** for your tape-out flow.

---

## `COMSOL Sim/` — FEM / mode work

Use the **`.mph`** model in COMSOL matching your installed version. This supports mode or propagation assumptions used to interpret coupling alongside measurements.

**Version control tip:** add `*.mph.lock` to `.gitignore` if you track the project in Git.

---

## `Chip 2 measurements/` — data and scripts

### `sweep 16 waveguides transmission/`

Contains many **`sweep_*.csv`** files from the wavelength sweeps. After cleanup, filenames follow:

- **Angled-interface / Configuration 1–style naming:** `sweep_<N>_<YYYYMMDD>_<HHMMSS>.csv`
- **Parallel-interface / Configuration 2–style naming:** `sweep_<N>_p_<YYYYMMDD>_<HHMMSS>.csv` (the **`p_`** token marks the “parallel facets” campaign in the local naming scheme)

The script **`transmission_calculation.py`** combines:

1. A **regex rename** utility that normalizes legacy sweep filenames without silent overwrites.
2. An **analysis** block that keeps structures **`{3, 7, 8, 9, 10}`** (a subset emphasized in local summaries), reads **`wavelength_nm`** and **`power_dBm`**, takes the **maximum** per file, collapses duplicate runs, and writes **`summary_selected.csv`** plus **`wavelength_vs_structure_selected.png`**.

> **Dependencies:** **`pandas`**, **`numpy`**, **`matplotlib`** for the analysis section (the rename block uses only the standard library plus **`pathlib`**).

**Terminology:** the thesis uses **Configuration 1** and **Configuration 2**; some Python files use the shorthand **Case 1 / Case 2** for the same two arrangements.

### `transmission variation in fiber x.py`

Plots **detector output vs. fiber alignment in \(x\)** (microns)—raw voltage, min–max scaling, and **relative dB**—supporting the **lateral fiber-to-detector** scans discussed with the **2D free-space model** in **§4.1.4** and **Appendix A.1**.

### `Plots/Transmisison values for all 16 loopbacks comparison.py`

*(Filename keeps the original spelling “Transmisison”.)*

Builds a **compact comparison figure** of **transmission vs. structure index** for all sixteen loopbacks for both configurations, with reference lines at **−28 dBm** (illustrative two-edge **−14 dB** budget) and **−65 dBm** (a local “acceptable band” threshold used in plotting). **Update figure captions** to match the **final thesis wording** if your published figures differ.

The script’s **`out_path`** is currently an **absolute path** on the author machine; change it when you clone or move the repo.

---

## Reproducing results (suggested order)

1. Install **Python 3.10+**, then `pip install numpy matplotlib pandas jupyter gdsfactory` (and **COMSOL** locally for FEM).
2. Run **`GDS/loopback chip iteration 4.ipynb`**.
3. In **`Chip 2 measurements/sweep 16 waveguides transmission/`**, run **`transmission_calculation.py`** (rename pass first if you are ingesting new sweeps with legacy names, then analysis).
4. Run **`Plots/Transmisison values for all 16 loopbacks comparison.py`** after fixing **`out_path`**.
5. Open the **`.mph`** model in **`COMSOL Sim/`** as needed.

---

## Related LaTeX on disk (draft / auxiliary)

`MIT/QP/Inspired/Chip 2 measurements/Plots/loopback_transmission_thesis.tex` contains a **self-contained LaTeX fragment** (table + figure stub) for loopback transmission. Treat it as **drafting material** unless the same numbers and captions appear verbatim in **`Thesis.pdf`**.

---

## Citing this work

For formal citation, use the **MIT thesis record** (Libraries / program deposit) once assigned. Until then, you may reference the **author-held PDF**: `C:\Users\prava\OneDrive\Desktop\Thesis.pdf`. For **datasets and code**, link to this **`Github uploads`** directory in addition to the thesis.

---

## License and credit

Thesis text and figures: © **2026** Vemparala Lakshmi Pravallika (subject to MIT thesis deposit terms). Third-party tools (**GDSFactory**, **COMSOL**, Python stack) remain under their respective licenses.

---

## Contact

Use the correspondence channels given in the submitted thesis (`Thesis.pdf`).
