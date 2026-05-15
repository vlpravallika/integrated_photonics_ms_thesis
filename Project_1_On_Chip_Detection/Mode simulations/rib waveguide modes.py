"""
Tidy3D script: LN rib waveguide on 10 µm SiO2 underclad, length 100 µm,
solve eigenmode (Ex, Ey) on an xy cross-section (at any z), and compute
mode overlap + power overlap with a cleaved SMF Gaussian mode (MFD=10.4 µm).

Geometry from your discussion:
- LN total film thickness = 0.300 µm
- Slab thickness = 0.100 µm  (=> partial etch depth 0.200 µm)
- Rib height above slab = 0.200 µm
- Rib (top) width = 0.800 µm
- "Bottom/slab region" width = 5.6 µm

Coordinates:
- x: horizontal
- y: vertical (up)
- z: propagation axis / waveguide length
We place the SiO2/LN interface at y=0.
"""

import numpy as np
import matplotlib.pyplot as plt
import tidy3d as td
from tidy3d.plugins.mode import ModeSolver

# ----------------------------
# 1) Wavelength / frequency
# ----------------------------
lambda0_um = 1.55
freq0 = td.C_0 / lambda0_um

# ----------------------------
# 2) Materials
# ----------------------------
# SiO2 from Tidy3D material library (as used in Flexcompute examples)
sio2 = td.material_library["SiO2"]["Horiba"]

# Lithium Niobate:
# For a quick rib-waveguide mode solve, many people start with an isotropic n~2.2 at 1550 nm
# (LN is actually anisotropic; for x-/z-cut and TE/TM you should switch to AnisotropicMedium).
n_ln = 2.20
ln = td.Medium(permittivity=n_ln**2)

# Background / top cladding (air)
air = td.Medium(permittivity=1.0)

# ----------------------------
# 3) Geometry dimensions (µm)
# ----------------------------
t_ln = 0.300          # LN total thickness
t_slab = 0.100        # remaining slab thickness
t_rib = t_ln - t_slab # rib height above slab = 0.200

w_rib = 0.800         # rib top width
w_slab = 5.600        # "bottom part" width you gave (7*0.8)

t_sio2 = 10.0         # SiO2 underclad thickness (below y=0)
Lz = 100.0            # straight waveguide length

# ----------------------------
# 4) Simulation domain sizes (µm)
# ----------------------------
# Give enough margin so fields decay at boundaries:
sx = 20.0             # x span
air_above = 6.0       # air above LN
sy = t_sio2 + air_above  # total y span (from bottom of SiO2 to top air)
# center y so that bottom is at -t_sio2 and top is +air_above
cy = (air_above - t_sio2) / 2.0

# ----------------------------
# 5) Build structures
# ----------------------------

# (a) SiO2 underclad: spans the whole x and z of the simulation
substrate = td.Structure(
    geometry=td.Box(
        center=(0.0, -t_sio2/2.0, 0.0),     # from y=-t_sio2 to y=0
        size=(sx, t_sio2, td.inf),
    ),
    medium=sio2,
)

# (b) LN slab "mesa" region: width = w_slab, thickness = t_slab (0 to 0.1 µm)
ln_slab = td.Structure(
    geometry=td.Box(
        center=(0.0, t_slab/2.0, 0.0),      # from y=0 to y=0.1
        size=(w_slab, t_slab, td.inf),
    ),
    medium=ln,
)

# (c) LN rib: width = w_rib, thickness = t_rib (0.1 to 0.3 µm)
ln_rib = td.Structure(
    geometry=td.Box(
        center=(0.0, t_slab + t_rib/2.0, 0.0),  # center at y=0.2
        size=(w_rib, t_rib, td.inf),
    ),
    medium=ln,
)

structures_mode = [substrate, ln_slab, ln_rib]

# ----------------------------
# 6) 3D "straight waveguide length 100 µm" geometry (for visualization / later FDTD)
# ----------------------------
# Note: Mode solving does NOT require the 100 µm length; the mode is invariant along z.
# But here's the 3D object set with finite z length if you want it.
substrate_3d = td.Structure(
    geometry=td.Box(center=(0.0, -t_sio2/2.0, 0.0), size=(sx, t_sio2, Lz)),
    medium=sio2,
)
ln_slab_3d = td.Structure(
    geometry=td.Box(center=(0.0, t_slab/2.0, 0.0), size=(w_slab, t_slab, Lz)),
    medium=ln,
)
ln_rib_3d = td.Structure(
    geometry=td.Box(center=(0.0, t_slab + t_rib/2.0, 0.0), size=(w_rib, t_rib, Lz)),
    medium=ln,
)

sim_3d_geom_only = td.Simulation(
    center=(0.0, cy, 0.0),
    size=(sx, sy, Lz),
    grid_spec=td.GridSpec.auto(min_steps_per_wvl=20, wavelength=lambda0_um),
    structures=[substrate_3d, ln_slab_3d, ln_rib_3d],
    run_time=1e-12,
    medium=air,
    boundary_spec=td.BoundarySpec.all_sides(td.PML()),
)

# Plot a y=const or z=const slice of the 3D geometry:
ax = sim_3d_geom_only.plot(z=0.0)
plt.title("3D geometry slice at z=0 µm (for visualization)")
plt.show()

# ----------------------------
# 7) Mode-solver simulation (2.5D): invariance along z, solve on xy plane
# ----------------------------
# We set z-size small; mode plane is xy with size=(sx, sy, 0).
sim_mode = td.Simulation(
    center=(0.0, cy, 0.0),
    size=(sx, sy, 1.0),
    grid_spec=td.GridSpec.auto(min_steps_per_wvl=25, wavelength=lambda0_um),
    structures=structures_mode,
    run_time=1e-12,
    medium=air,
)

# Mode solve plane: xy cross section at z=0
plane = td.Box(center=(0.0, cy, 0.0), size=(sx, sy, 0.0))

# Mode spec: fundamental mode
mode_spec = td.ModeSpec(
    num_modes=1,
    target_neff=2.1,  # reasonable starting guess for LN waveguides; adjust if needed
)

mode_solver = ModeSolver(
    simulation=sim_mode,
    plane=plane,
    mode_spec=mode_spec,
    freqs=[freq0],
)

# Solve locally (no cloud credits). For higher accuracy, use web.run() with subpixel averaging.
mode_data = mode_solver.solve()

# ----------------------------
# 8) Plot Ex and Ey in the cross-section (xy)
# ----------------------------
# mode_data has xarray-backed fields, so you can use .abs.plot()
mode_data.Ex.abs.plot(x="x", y="y", cmap="hot")
plt.title("Mode |Ex| in xy cross-section (z-invariant)")
plt.gca().set_aspect("equal")
plt.show()

mode_data.Ey.abs.plot(x="x", y="y", cmap="hot")
plt.title("Mode |Ey| in xy cross-section (z-invariant)")
plt.gca().set_aspect("equal")
plt.show()

# ----------------------------
# 9) Fiber mode (Gaussian) and overlap
# ----------------------------
# Fiber: MFD = 10.4 µm => waist radius (1/e^2 intensity radius) = MFD/2 = 5.2 µm
MFD_um = 10.4
w0_um = MFD_um / 2.0

# Make sure the Gaussian plane is large enough to capture tails
beam_plane_size = 6 * w0_um  # rule of thumb used in Flexcompute examples

# Polarization: set pol_angle to match your guided mode (TE/TM).
# pol_angle = pi/2 corresponds to Ey polarization for a z-propagating beam.
gaussian_beam = td.GaussianBeamProfile(
    waist_radius=w0_um,
    pol_angle=np.pi / 2,              # Ey-polarized (adjust if your mode is Ex-dominant)
    size=(beam_plane_size, beam_plane_size, 0.0),  # 0 means beam propagates along z
    resolution=250,
    freqs=[freq0],
)

# Optional: visualize the Gaussian Ey profile
gaussian_beam.field_data.Ey.abs.plot(x="x", y="y", cmap="hot")
plt.title("Fiber Gaussian |Ey| (MFD=10.4 µm @ 1550 nm)")
plt.gca().set_aspect("equal")
plt.show()

# Overlap integral using built-in outer_dot (modal decomposition)
# Returns complex amplitude overlap; power overlap / coupling efficiency is |overlap|^2
overlap_amp = mode_data.outer_dot(gaussian_beam.field_data).values.squeeze()
power_overlap = np.abs(overlap_amp) ** 2

print(f"Amplitude overlap = {overlap_amp}")
print(f"Power overlap (coupling efficiency) = {power_overlap:.6f}  ({10*np.log10(power_overlap):.2f} dB)")

# If you want to study misalignment (e.g., fiber offset by dx, dy):
dx_um, dy_um = 0.0, 0.0  # change these
mode_shifted = mode_data.translated_copy(vector=(dx_um, dy_um, 0.0))
overlap_amp_shifted = mode_shifted.outer_dot(gaussian_beam.field_data).values.squeeze()
power_overlap_shifted = np.abs(overlap_amp_shifted) ** 2
print(f"Shifted power overlap (dx={dx_um} µm, dy={dy_um} µm) = {power_overlap_shifted:.6f} "
      f"({10*np.log10(power_overlap_shifted):.2f} dB)")
