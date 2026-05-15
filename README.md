# Supplementary materials: thesis experiments, layout, and analysis

This folder accompanies the MIT master’s thesis **“High-efficiency On-Chip detection in TFLN and On-chip Gain Integration on Si for Scalable Integrated Photonics”** by **Vemparala Lakshmi Pravallika** (Program in Media Arts and Sciences, Massachusetts Institute of Technology, May 2026; supervisor: Dirk Englund).

The thesis develops two complementary threads: **efficient telecom-band photodetection on thin-film lithium niobate (TFLN)** using a mechanically buckled, selectively underetched waveguide path to an absorber, and **optical gain on silicon** via micro-transfer printed GaAs quantum-dot nanobeams coupled to a silicon taper. The artifacts collected here are the **design files, finite-element models, raw instrument exports, and Python/Jupyter workflows** that support silicon photonics characterization—especially **edge-coupled loopback transmission** on a cleaved chip—rather than the full LaTeX thesis source tree.

If you cite or reuse this bundle, point readers to the official thesis document (MIT Libraries / program requirements) and, where appropriate, to this repository path.

---

## What is in this directory (high level)

| Subfolder | Role |
|-----------|------|
| **`GDS/`** | Layout generation for a **loopback test chip** (iteration 4) using **GDSFactory** and the generic PDK; encodes routing, etch-parameter sweeps, and layer definitions for tape-out or further editing. |
| **`COMSOL Sim/`** | **COMSOL Multiphysics** project material for a **strip waveguide** model (compressed `.mph` naming in the workspace). A `.mph.lock` file may appear while COMSOL has the model open—it is a local lock, not physics data. |
| **`Chip 2 measurements/`** | **Laboratory CSV sweeps**, aggregation scripts, and plotting code for **sixteen viable loopback waveguides** after cleaving, including comparison of two alignment geometries (see below). |

Together, these items document **how the measured transmission numbers and figures in the thesis were produced**, and how the **test structures** were generated in layout and simulation.

---

## Connection to the thesis narrative

The abstract emphasizes heterogeneous integration: attaching **III–V absorbers and gain media** to **passive hosts** (here, silicon and TFLN) and managing the **active–passive interface** (coupling, alignment, yield).

The contents of **`Chip 2 measurements/`** speak directly to that interface on a **cleaved silicon photonic chip**:

- **Forty loopbacks** were designed; **cleave quality and facet angle** reduced the set to **16 measurable structures**.
- Measurements were taken at **1595 nm** with **0 dBm** input on **straight waveguide + 180° Euler bend + straight** loopbacks, fiber-coupled chip-to-chip.
- Two experimental **cases** are distinguished in the write-up and in the plotting scripts:
  - **Case 1 — angled interfaces:** fiber array parallel to \(x\), chip facets not parallel because of cleave angle; per-structure re-optimization in multiple axes.
  - **Case 2 — parallel interfaces:** both facets parallel to the fiber array; waveguides slightly angled (\(\sim 1^\circ\)) but **repeatable alignment** without per-structure re-optimization.

The thesis section on **loopback transmission and edge-coupling characterisation** tabulates **transmission in dBm** for all sixteen structures in both cases, plots **transmission vs. structure index**, and marks:

- a **theoretical reference** at **−28 dBm** (ideal **−14 dB per edge** coupling budget for a rib waveguide, two edges), and  
- an **acceptable threshold** at **−65 dBm**, with **structures 3, 7, 8, 9, and 10** highlighted as meeting the criterion.

The Python sources in this folder encode those same thresholds, structure IDs, and case labels so that **figures can be regenerated** from the archived CSVs.

---

## `GDS/` — layout: `loopback chip iteration 4.ipynb`

This Jupyter notebook drives **GDSFactory** (`import gdsfactory as gf`) with the **generic PDK** activated.

**What the notebook is doing (conceptually):**

- Defines **strip waveguide** cross-section parameters (e.g. width **0.8 µm**), **127 µm** port pitch, and a **U-turn Euler radius** derived from that pitch.
- Sets **routing** constants (horizontal extent, vertical straights, per-unit vertical push) to tile or route many loopback units compatible with edge coupling.
- Declares an **etch sweep** over length, width, and gap to explore etch-defined features alongside the waveguide core.
- Assigns **GDS layers** for the waveguide and box/etch regions.

**Practical use:** open the notebook in Jupyter, ensure `gdsfactory` and the intended PDK are installed, run cells top-to-bottom, and export GDS/OASIS as needed for your flow. Exact cell order and outputs are preserved in the notebook metadata for traceability.

---

## `COMSOL Sim/` — electromagnetics / mode models

The strip-waveguide **COMSOL** model supports mode profiles, effective indices, or propagation assumptions used alongside—or to sanity-check—the measured coupling behavior. Because COMSOL files can be large and version-specific, this folder may contain the working **`.mph`** (and occasionally a **`.mph.lock`** while the GUI holds the file).

**Tip for Git hygiene:** add `*.mph.lock` to `.gitignore` if you version-control the project, so local GUI sessions do not create noisy commits.

---

## `Chip 2 measurements/` — sweeps, cleaning, summaries, plots

### Raw data: `sweep 16 waveguides transmission/`

This subdirectory holds **many `sweep_*.csv` files** exported from wavelength / power sweeps. Filenames encode:

- the **structure index** (1–16),
- optional suffix **`p_`** distinguishing the **parallel-interface (Case 2)** configuration from the **angled-interface (Case 1)** naming convention after cleanup,
- and **timestamp** (`YYYYMMDD_HHMMSS`) for run provenance.

The companion script **`transmission_calculation.py`** is effectively **two utilities in one file**:

1. **Renaming pass** — normalizes filenames with a regex so that angled runs read `sweep_<N>_<date>_<time>.csv` and parallel runs read `sweep_<N>_p_<date>_<time>.csv`, avoiding silent overwrites.
2. **Analysis pass** — filters to the thesis-highlighted structures **`{3, 7, 8, 9, 10}`**, reads CSV columns `wavelength_nm` and `power_dBm`, finds the **maximum transmitted power** per file, deduplicates multiple runs per (structure, orientation), and writes:

   - `summary_selected.csv` — per-structure, per-orientation maxima and wavelengths,  
   - `wavelength_vs_structure_selected.png` — peak wavelength vs structure for the selected set.

> **Dependency note:** the analysis section uses **`pandas`** and **`numpy`** in addition to **`matplotlib`**. Ensure they are installed in the interpreter you use.

### Top-level helper: `transmission variation in fiber x.py`

Standalone **`numpy` / `matplotlib`** script that plots **detector voltage vs. fiber alignment in \(x\)** (microns), including min–max scaling and **relative dB** with respect to the peak. This supports **fiber–facet alignment** studies complementary to the wavelength sweeps.

### Figures: `Plots/Transmisison values for all 16 loopbacks comparison.py`

*(Filename retains the original spelling “Transmisison”.)*

Generates the **thesis-style summary plot** of **transmission vs. structure number** for **all 16 loopbacks**, both cases, with:

- markers for Case 1 and Case 2,
- emphasis on acceptable structures **3, 7, 8, 9, 10**,
- horizontal guides at **−28 dBm** (theoretical best) and **−65 dBm** (acceptable threshold),
- export to **`transmission_vs_structure.png`** (the script currently uses an absolute save path on the author machine; adjust `out_path` when you clone this repo).

The numeric arrays in this script match the **LaTeX table** in the thesis excerpt for loopback transmission (Case 1 / Case 2 columns).

---

## Reproducing results (suggested order)

1. **Install** a recent Python (3.10+ recommended), then `pip install numpy matplotlib pandas jupyter gdsfactory` (and COMSOL locally for FEM work).
2. **`GDS/`** — run `loopback chip iteration 4.ipynb` to regenerate layout artifacts.
3. **`Chip 2 measurements/sweep 16 waveguides transmission/`** — optionally run the **rename** portion of `transmission_calculation.py` if you ingest new sweeps with legacy names; then run the **analysis** portion to refresh `summary_selected.csv` and the wavelength figure.
4. **`Chip 2 measurements/Plots/`** — run `Transmisison values for all 16 loopbacks comparison.py` after setting `out_path` to a location inside this repo if you want self-contained outputs.
5. **`COMSOL Sim/`** — open the `.mph` in COMSOL corresponding to your installed version; re-solve as needed.

---

## Relationship to other files on disk

The LaTeX snippet used in the thesis for the loopback section lives alongside related work under:

`MIT/QP/Inspired/Chip 2 measurements/Plots/loopback_transmission_thesis.tex`

That file’s **table, figure reference, and prose** are the publication-facing version of what the **`Plots/`** Python script visualizes. Keeping this **`Github uploads`** folder next to the thesis tree preserves **one-way traceability**: code and CSV → summary tables and figures → thesis PDF.

---

## License and credit

Thesis text and figures: © 2026 Vemparala Lakshmi Pravallika (subject to MIT thesis deposit terms). Third-party tools (**GDSFactory**, **COMSOL**, Python scientific stack) remain under their respective licenses.

**Committee (from thesis front matter):** Dirk Englund (supervisor), Joseph Paradiso, Jelena Notaros.

---

## Contact

For questions about this dataset bundle or the underlying experiments, use the correspondence channels established in the final thesis document.
