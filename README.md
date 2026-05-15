# Device Exploration for On-Chip Detection on Lithium Niobate and Amplification on Silicon for Scalable Integrated Photonics

**Vemparala Lakshmi Pravallika**  
B.Tech., Indian Institute of Technology Bombay (2024)  

Program in Media Arts and Sciences, School of Architecture and Planning  
Massachusetts Institute of Technology  

Master of Science in Media Arts and Sciences · submitted **15 May 2026**  

**Thesis supervisor:** Dirk Englund — Professor of Electrical Engineering and AI + Decision-making, MIT EECS  
**Committee:** Dirk Englund, Joseph Paradiso, Jelena Notaros  

**Committee certification page title (longer variant):** *Device Exploration for High-Efficiency On-Chip Detection in TFLN and Heterogeneous Gain Integration on Si for Scalable Integrated Photonics*  

The **citation copy** of the thesis is the **MIT-submitted document** (Libraries / program deposit). This Git directory holds **artifacts only** (CAD interchange, notebooks, code, CSV measurements).

---

## Abstract (as submitted)

Passive photonic integrated circuits excel at routing and modulating light, but generation and detection still rely on heterogeneous integration of foreign active materials. Bonding, epitaxy, flip-chip, and micro-transfer printing dominate how industry and research labs attach III–V detectors, amplifiers, and lasers to substrate hosts. An important bottleneck is the active–passive interface: coupling efficiency, alignment, and yield.

This thesis contributes two complementary demonstrations on leading passive platforms. Project 1 targets efficient telecom-band photodetection on thin-film lithium niobate. Lithographic adiabatic tapers to an absorber are the established route; here a doubly-clamped rib waveguide is selectively underetched and buckled so that a mechanical air gap drives the same adiabatic transition. Modeling predicts waveguide-to-absorber coupling near unity and total quantum efficiency near ninety-six percent for the coupled-mode design. A fiber-coupled test bench was built to characterize transmission and to separate the evanescent path from parasitic paths; a successor layout will suppress the dominant parasitic channel by geometry.

Project 2 targets optical gain on silicon using micro-transfer printing: a GaAs quantum-dot nanobeam with a 1D photonic-crystal cavity is placed on a silicon taper so that the signal transfers vertically to the III–V and is amplified by donor material. The workflow from donor release through stamp alignment and confocal pump delivery was implemented end-to-end, with several chiplets aligned within the taper tolerance for follow-on characterization.

Taken together, the work advances reusable recipes for high-efficiency detection on TFLN and compact gain on silicon spanning coherent links, switches, sensing, and integrated nonlinear and quantum photonics.

---

## What this repository contains

This tree is the **working artifact bundle** for the thesis hardware chapters: **SolidWorks / STEP digital twins** for both benches, **GDSFactory** mask notebooks, **COMSOL** project locks (models may be kept locally), **Tidy3D** mode notebooks and scripts, **Chip 1** detector-linearity checks, and **Chip 2** loopback **wavelength–power CSV archives** plus Python reduction and plotting.

There is **no separate folder named `transmission results`**: the **transmission sweep results** are the **`sweep_*.csv`** files (and derived **`summary_*.csv`**) under **`Chip 2 measurements/sweep 16 waveguides transmission/`**.

---

## Indexed layout (files that exist in this directory)

### `on chip detection setup solidworks model/`

**Project 1** mechanical **digital twin** geometry in neutral **STEP/STP** interchange (import into SolidWorks or any MCAD viewer). This is the same class of assembly the thesis documents in **§3.2.1** and **Fig. 3.4** (fiber-coupled detector bench with horizontal side-view imaging, clearance checks before 3D-printed fixtures).

| File | Role |
|------|------|
| `fiber array holder 15_01.STEP` | Custom **fiber-array holder** solid exported from SolidWorks (15 Jan revision in filename). |
| `Newport-TSX-1D.stp` | Newport **TSX-1D** linear stage vendor solid. |
| `B1818F-Step.step` | Thorlabs **B1818F** breadboard / plate geometry. |
| `MAX313D-Step.step` | Thorlabs **MAX313D** mount solid. |
| `TTR001-Step.step` | Thorlabs **TTR001** rotation mount solid. |
| `GPXL1-Step.step` | Thorlabs **GPXL1** goniometric stage solid. |
| `PR01-Step.step` | Thorlabs **PR01** cage plate solid. |
| `HFV002-Step.step` | Thorlabs **HFV002** vertical translation stage solid. |
| `CS165MU-Step.step` | Thorlabs **CS165MU** post / pedestal solid. |
| `step_63744.step` | Additional interchange solid from the same export set (SolidWorks default `step_*.step` naming). |

### `Topchip gain integration setup digital twin/`

| File | Role |
|------|------|
| `step_88206.step` | **Project 2** bench **STEP** export: silicon host with **dual edge-coupled fiber stacks** and **vertical confocal microscope** access as laid out in **§3.4.4–3.4.5** of the thesis (stamp alignment and pump delivery geometry). |

### `GDS/`

| File | Role |
|------|------|
| `loopback chip iteration 4.ipynb` | **Primary** **GDSFactory** notebook (generic PDK): **0.8 µm** strip waveguide, **127 µm** facet pitch, Euler **U-turn** radius `(PITCH/2)−5.8` µm, long routing straights, **`ETCH_LENGTHS` × `ETCH_WIDTHS` × `ETCH_GAPS`** etch-window sweep, layer pair `(1,0)` waveguide / `(2,0)` box. This is the **Chip 2** loopback mask lineage behind **Fig. 3.11** in the thesis. |
| `loopback chip iteration 3.ipynb` | **Earlier** loopback notebook (`repeats = 7`, **5000 µm** straight sections, etch lengths up to **2500 µm**, boolean / `LayerStack` tooling) retained for iteration history. |
| `bend_radius_analysis.ipynb` | **Tidy3D**-invoking bend / propagation study notebook (see notebook for exact solver calls and warnings). Informs Euler bend radius choices in the loopback notebooks. |

### `COMSOL Sim/`

| File | Role |
|------|------|
| `strip waveguide compressed.mph.lock` | Lock file for the **strip waveguide** COMSOL model (`strip waveguide compressed.mph` when saved locally). |
| `taper waveguide edge.mph.lock` | Lock file for the **taper / facet-edge** waveguide model (`taper waveguide edge.mph` when saved locally). |

Only **`.mph.lock`** files are present in this snapshot; the binary **`.mph`** models are usually excluded from Git for size. Re-open the corresponding `.mph` in COMSOL on a machine that has the full file.

### `Mode simulations/`

Eigenmode and overlap work for the **LNOI rib** cross section at **1550 nm** scale (thesis **Fig. 3.2** class: Tidy3D FDE rib mode).

| Path | Role |
|------|------|
| `ln_rib_mode_overlap.ipynb` | Notebook pipeline for **rib eigenmodes** and **overlap integrals** with a cleaved **SMF-28** Gaussian (**MFD = 10.4 µm**). |
| `edge_coupler.ipynb` | Notebook for **edge-coupler** field / coupling studies. |
| `rib waveguide modes.py` | Standalone **Tidy3D** `ModeSolver` script: **10 µm** SiO₂ underclad, **0.30 µm** LN film, **0.10 µm** slab, **0.20 µm** rib height, **0.80 µm** rib top width, **5.6 µm** bottom width; computes mode fields and **power overlap** with fiber mode. |
| `.vscode/settings.json` | Workspace editor settings used while developing these notebooks. |
| `build/log/.wsport.log` | Tool-generated log from a local solve / IDE session. |

### `Chip 1/`

| File | Role |
|------|------|
| `characterisation of detector comparison.py` | **Capped vs. uncapped** photoreceiver comparison: hard-coded **`power_dbm_*`** vs **`voltage_v_*`** arrays, plots **dBm** and **µW** vs voltage and inferred **photocurrent**; writes **`compare_dBm_vs_voltage.png`**, **`compare_uW_vs_voltage.png`**, **`compare_current_vs_voltage.png`** in the current working directory when run. Supports the **TIA / saturation** discussion around **Fig. 3.14** bench checkout. |

### `Chip 2 measurements/`

**Thesis linkage:** **§3.3.5** (measurement protocol), **§4.1.2–4.1.4** (contamination, operating wavelength, 2D free-space model). **Chip 2** has **25** designed loopbacks; **16** cleaved to viable facets (**§3.3.5** text). **Configuration 1** = angled facets; **Configuration 2** = parallel facets (**§3.3.5**). Sweeps run **1480–1600 nm**, **0 dBm** input; **~1595 nm** adopted as common operating point (**§4.1.3**, **Fig. 4.2**).

| Path | Role |
|------|------|
| `sweep 16 waveguides transmission/sweep_*.csv` | Raw **wavelength sweep** logs: columns include **`wavelength_nm`** and **`power_dBm`** (after instrument export). Filename grammar after cleanup: `sweep_<structure>_<YYYYMMDD>_<HHMMSS>.csv` for **Configuration 1** runs and `sweep_<structure>_p_<YYYYMMDD>_<HHMMSS>.csv` when `_p_` marks **Configuration 2** (“parallel facets”) reruns. |
| `sweep 16 waveguides transmission/summary_selected.csv` | Per-structure, per-orientation **max power** table produced by **`transmission_calculation.py`**. |
| `sweep 16 waveguides transmission/summary_maxima_selected.csv` | Alternate / intermediate maxima summary from the same script family. |
| `sweep 16 waveguides transmission/summary_maxima.csv` | Broader maxima table prior to orientation filtering (same analysis lineage). |
| `sweep 16 waveguides transmission/transmission_calculation.py` | **(1)** Regex-based batch **rename** of `sweep_*.csv` to the canonical patterns above (collision-safe). **(2)** **pandas**/**numpy** pass: filters structures **`{3,7,8,9,10}`**, finds **argmax** of `power_dBm`, deduplicates by structure+orientation, writes **`summary_selected.csv`** and **`wavelength_vs_structure_selected.png`**. |
| `transmission variation in fiber x.py` | Standalone **matplotlib** plots of **detector voltage vs. fiber \(x\)** (µm) from embedded arrays: raw trace, min–max scaled, and **20·log₁₀(V/Vmax)** dB scale—used for **lateral alignment** sweeps in the same measurement campaign as **§4.1.4**. |
| `Plots/Transmisison values for all 16 loopbacks comparison.py` | **Agg** backend: plots **all 16** structures’ **dBm** values at **1595 nm**, **0 dBm** input for **Case 1** vs **Case 2** arrays (same physical content as **Configuration 1** vs **2** in the thesis), highlights structures **3,7,8,9,10**, draws **−28 dBm** and **−65 dBm** reference lines. **You must edit `out_path`** inside the script before saving figures on a new machine. |

### `README.md`

This file.

---

## How measurements map to thesis language

- **Thesis:** **Configuration 1** (angled interfaces) vs **Configuration 2** (parallel interfaces).  
- **Python in this repo:** often labeled **Case 1** / **Case 2** in comments and plot legends.

---

## Dependencies (by component)

| Component | Typical stack |
|-----------|----------------|
| `GDS/*.ipynb` | **Python 3.10+**, **`gdsfactory`**, Jupyter |
| `Mode simulations/*` | **`tidy3d`**, **`numpy`**, **`matplotlib`**, Jupyter |
| `COMSOL Sim` | **COMSOL Multiphysics** (version matched to your `.mph`) |
| `Chip 2 measurements/*.py` | **`numpy`**, **`matplotlib`**; **`transmission_calculation.py`** analysis cell needs **`pandas`** |
| CAD | Any STEP/STP-capable viewer (SolidWorks, Onshape, FreeCAD) |

---

## Suggested reproduction order

1. Open STEP files in **`on chip detection setup solidworks model/`** and **`Topchip gain integration setup digital twin/`** to recover full 3D clearance context (**Fig. 3.4** and Project 2 bench figures).  
2. Run **`GDS/loopback chip iteration 4.ipynb`**, then compare against **`loopback chip iteration 3.ipynb`** for design deltas.  
3. Run **`bend_radius_analysis.ipynb`** if updating bend radii before a mask rerun.  
4. Execute **`Mode simulations/rib waveguide modes.py`** or the notebooks after configuring **Tidy3D** credentials.  
5. Open COMSOL **`.mph`** files that pair with the two **`.mph.lock`** names (local machine).  
6. From **`Chip 2 measurements/sweep 16 waveguides transmission/`**, run **`transmission_calculation.py`** (rename pass only when ingesting new raw sweeps), then run the **`Plots/`** script after fixing paths.

---

## Version control hygiene (recommended)

Add to **`.gitignore`** if you expand commits: `*.mph.lock`, `**/.vscode/`, `**/build/`, large `*.mph`, and any regenerated **`compare_*.png`** / **`transmission_vs_structure.png`** outputs if you do not want binaries in history.

---

## License

Thesis text and figures: © **2026** Vemparala Lakshmi Pravallika (subject to MIT thesis deposit terms). **Vendor STEP** models remain property of their respective suppliers. **Tidy3D**, **COMSOL**, **gdsfactory**, and Python packages follow their own licenses.

---

## Contact

Use the correspondence channels listed in the submitted thesis front matter.
