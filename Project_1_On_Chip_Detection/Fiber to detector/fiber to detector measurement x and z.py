"""
Output Power vs. Lateral Offset (x) and Vertical Distance (z)

Large-signal / small-signal decomposition of the detector output:

    V_total(d) = V_large(d) + V_small(d)
              ~ A * (d + d_p)^(-alpha)   +   B * exp(-d / d_e)

where d is z (vertical detector-to-chip gap) or x (lateral fibre-to-waveguide
offset). V_large is the parasitic free-space + scattering channel (slow
polynomial decay), V_small is the waveguide-launched evanescent / mode-overlap
channel (exponential decay). At d >> d_e the exponential term has died out,
so V_large can be fitted from the far-d tail and V_small recovered by
subtraction.

Outputs:
  - fitted parameters (A, d_p, alpha, B, d_e) for both x and z curves
  - small-signal values V_small(0) in V and dBm, compared between the two scans
  - one combined PNG ('output_power_with_fits.png') showing, for each panel,
    the raw data, the smoothed data, the V_large fit, the V_small fit,
    and their sum (V_total fit), all on the same axes.
"""

import os
import numpy as np
import matplotlib
if not os.environ.get("DISPLAY") and os.name != "posix":
    matplotlib.use("Agg")  # headless-safe; remove if you want interactive
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit

# ==========================================================================
# DATA
# ==========================================================================

V_out_x = np.array([
    14.3, 14.3, 14.3, 14.3, 13.9,
    14.3, 14.3, 13.7, 14.3, 14.1,
    14.3, 14.1, 14.3, 14.2, 13.5,
    14.2, 14.3, 13.8, 14.3, 14.3,
    14.3, 13.5, 14.3, 14.2, 13.8,
    14.2, 13.7, 14.3, 14.1, 14.2,
    13.6, 13.5, 12.1, 11.9, 11.3,
    12.4, 12.6, 12.8, 12.7, 13.0,
    12.7, 11.7, 11.5, 11.1, 11.1,
    10.7, 11.2, 11.0, 10.6, 11.2
])

V_out_z = np.array([
    13.0, 13.0, 12.8, 12.5, 12.6, 12.8, 12.5, 12.9, 12.7, 13.9,
    13.9, 13.8, 13.5, 13.7, 13.4, 12.5, 11.3, 11.4, 12.2, 12.8,
    12.1, 13.0, 12.4, 12.5, 13.3, 12.7, 12.4, 12.9, 12.3, 12.4,
    12.2, 12.3, 11.6, 11.8, 12.4, 11.6, 11.8, 12.5, 11.6, 12.2,
    11.7, 13.1, 12.8, 12.3, 11.2, 10.9, 11.0, 11.5, 10.6, 10.9,
    10.2, 10.3, 11.0, 10.4, 10.0, 10.3, 10.7, 9.9, 9.5, 9.1,
    10.1, 9.5, 10.1, 8.7, 8.9, 7.9, 7.4, 7.4, 7.9, 7.6,
    8.4, 7.7, 7.2, 8.2, 8.4, 7.7, 7.8, 7.2, 7.8, 7.6,
    7.2, 6.8, 6.7, 6.4, 6.1, 6.1, 5.9, 5.4, 5.7, 4.8,
    5.5, 5.6, 5.5, 5.2, 5.1, 4.8, 5.2, 4.8, 5.0, 4.7,
    4.8, 4.8, 4.9, 4.8, 4.5, 4.4, 5.1, 4.5, 4.9, 4.6,
    4.7, 4.7, 4.9, 4.5, 4.4, 4.5, 4.6, 4.5, 4.5, 3.8,
    4.3, 4.1, 3.8, 4.1, 3.7, 4.1, 4.3, 3.9, 3.9, 3.9,
    3.8, 4.0, 3.6, 3.8, 3.5, 3.4, 3.7, 3.8, 4.0, 3.6,
    3.8, 3.5, 3.4, 3.7, 3.8, 4.1, 3.4, 3.8, 4.0, 3.9,
    3.6, 3.5, 3.9, 4.1, 3.8, 3.6, 3.8, 3.7, 3.7, 3.4,
    3.2, 3.4, 3.5, 3.8, 3.6, 3.4, 3.6, 3.7, 3.2, 3.1,
    3.0, 3.2, 3.2, 3.2, 3.2, 3.1, 3.5, 3.3, 3.3, 3.4,
    3.6, 3.2, 3.2, 3.3, 3.4, 3.4, 3.4, 3.2, 3.4, 3.3,
    3.2, 3.1, 3.0, 2.9, 3.1, 2.8, 2.8, 2.8, 3.2, 2.9,
    3.1, 3.1, 2.9, 2.8, 2.9, 2.7, 2.7, 2.6, 2.5, 2.5,
    2.6, 2.7, 2.4, 2.8, 2.7, 2.7, 2.7, 2.6, 2.6, 2.6,
    2.4, 2.4, 2.7, 2.8, 2.8, 3.0, 3.1, 3.0, 2.8, 3.0,
    2.3, 3.0, 2.8, 2.8, 3.0, 2.8, 2.8, 2.9, 2.8, 2.6,
    2.6, 2.6, 2.8, 2.6, 2.7, 2.5, 2.6, 2.6, 2.7, 2.5,
    2.5
])

x_offset = np.arange(1, len(V_out_x) + 1).astype(float)   # micrometres
z_offset = np.arange(0, len(V_out_z)).astype(float)       # micrometres

V_x_smooth = savgol_filter(V_out_x, window_length=11, polyorder=3)
V_z_smooth = savgol_filter(V_out_z, window_length=15, polyorder=3)

# ==========================================================================
# UNITS
# ==========================================================================
Z_T = 1.5e5      # transimpedance (V/A)
R   = 1.0        # responsivity   (A/W)


def V_to_dBm(V):
    return 10.0 * np.log10(np.clip(V, 1e-9, None) / (Z_T * R) * 1e3)


def dBm_to_V(dBm):
    return Z_T * R * 10.0 ** (dBm / 10.0) * 1e-3


# ==========================================================================
# MODEL
#
# V_large is the parasitic free-space + scattering channel.  A plain
# A (d + dp)^(-alpha) cannot describe the measured data because the data has
# a clear *plateau* near d = 0 (V is roughly flat for z = 0..15 um and for
# x = 0..30 um) and only decays beyond a knee distance.  We therefore use a
# rounded power law (a Hill / soft-saturation form),
#
#     V_large(d) = V_inf + (V_0 - V_inf) / [1 + (d / L)^alpha],
#
# which plateaus at V_0 for d << L, transitions around the knee L, and
# decays as d^(-alpha) for d >> L (asymptotic floor V_inf).  This is the
# same functional shape as a Hill curve / generalised Lorentzian.
#
# V_small is still the waveguide-launched evanescent coupling:
#
#     V_small(d) = B * exp(-d / d_e),  B >= 0.
# ==========================================================================
def V_large(d, V0, Vinf, L, alpha):
    """Soft / rounded power law: plateau then tail."""
    return Vinf + (V0 - Vinf) / (1.0 + (d / L) ** alpha)


def V_small_fn(d, B, de):
    """Exponential evanescent / mode-overlap channel."""
    return B * np.exp(-d / de)


def V_total(d, V0, Vinf, L, alpha, B, de):
    return V_large(d, V0, Vinf, L, alpha) + V_small_fn(d, B, de)


# ==========================================================================
# JOINT FIT (V_large = rounded-power law + V_small = exponential)
#
# Strategy: do a Stage-1 fit on V_large alone (because the V_small fast
# evanescent term should sit on top of an already-good V_large), then a
# Stage-2 joint fit of V_large + V_small with B >= 0 and physical d_e.
#
# Bounds:
#   V_0 in [0, 30] V             : plateau height
#   V_inf in [0, V_0]            : asymptotic floor
#   L in [1, 500] um             : knee distance
#   alpha in [0.3, 5]            : tail steepness
#   B in [0, 30] V               : evanescent-channel amplitude
#   d_e in [physical range]      : evanescent decay length
# ==========================================================================
def fit_rounded(d, V_smoothed, ze_bounds, V0_init, Vinf_init, L_init,
                alpha_init, B_init=0.5, de_init=1.0):
    # Stage 1: V_large alone.
    p0_L = [V0_init, Vinf_init, L_init, alpha_init]
    bounds_L_lo = [0.5 * V0_init, 0.0, 1.0, 0.3]
    bounds_L_hi = [1.5 * V0_init, V0_init, 500.0, 6.0]
    popt_L, _ = curve_fit(
        V_large, d, V_smoothed,
        p0=p0_L,
        bounds=(bounds_L_lo, bounds_L_hi),
        maxfev=20000,
    )
    V0_0, Vinf_0, L_0, alpha_0 = popt_L

    # Stage 2: full joint fit.
    p0 = [V0_0, Vinf_0, L_0, alpha_0, B_init, de_init]
    bounds_lo = [0.5 * V0_0, 0.0,        max(1.0, L_0 - 100.0),
                 max(0.3, alpha_0 - 1.0), 0.0, ze_bounds[0]]
    bounds_hi = [1.5 * V0_0, V0_0,       L_0 + 200.0,
                 min(6.0, alpha_0 + 1.5), 30.0, ze_bounds[1]]
    popt, _ = curve_fit(
        V_total, d, V_smoothed,
        p0=p0,
        bounds=(bounds_lo, bounds_hi),
        maxfev=40000,
    )
    return popt


# ---------- Z scan ----------
V0_z, Vinf_z, L_z, alpha_z, B_z, ze = fit_rounded(
    z_offset, V_z_smooth,
    ze_bounds=(0.3, 5.0),
    V0_init=13.5, Vinf_init=1.5, L_init=80.0, alpha_init=2.0,
    B_init=0.3, de_init=1.0,
)
V_large_z_fit = V_large(z_offset, V0_z, Vinf_z, L_z, alpha_z)
V_small_z_fit = V_small_fn(z_offset, B_z, ze)
V_total_z_fit = V_large_z_fit + V_small_z_fit

# ---------- X scan ----------
V0_x, Vinf_x, L_x, alpha_x, B_x, xe = fit_rounded(
    x_offset, V_x_smooth,
    ze_bounds=(1.0, 15.0),
    V0_init=14.0, Vinf_init=11.0, L_init=32.0, alpha_init=4.0,
    B_init=0.3, de_init=5.0,
)
V_large_x_fit = V_large(x_offset, V0_x, Vinf_x, L_x, alpha_x)
V_small_x_fit = V_small_fn(x_offset, B_x, xe)
V_total_x_fit = V_large_x_fit + V_small_x_fit


# ==========================================================================
# REPORT
# ==========================================================================
def report(label, V0, Vinf, L, alpha, B, de):
    Vl0 = V_large(0.0, V0, Vinf, L, alpha)
    print(f"\n{label}")
    print(f"  V_large  : V0 = {V0:.3f} V   V_inf = {Vinf:.3f} V")
    print(f"             L  = {L:.2f} um   alpha = {alpha:.3f}")
    print(f"             V_large(0) = {Vl0:.3f} V")
    if B > 1e-6:
        print(f"  V_small  : B = {B:.3f} V  de = {de:.2f} um")
        print(f"             V_small(0) = {B:.3f} V   ({V_to_dBm(B):.2f} dBm)")
    else:
        print(f"  V_small  : B = {B:.3g} V (driven to zero)  de = {de:.2f} um")


print("=" * 70)
report("Z scan  (vertical detector offset)", V0_z, Vinf_z, L_z, alpha_z, B_z, ze)
report("X scan  (lateral fibre offset)",     V0_x, Vinf_x, L_x, alpha_x, B_x, xe)

print("\nSmall-signal cross-check (should match if model is consistent):")
print(f"  V_small_z(0) = {V_small_fn(0, B_z, ze):.3f} V "
      f"= {V_to_dBm(max(V_small_fn(0, B_z, ze), 1e-9)):.2f} dBm")
print(f"  V_small_x(0) = {V_small_fn(0, B_x, xe):.3f} V "
      f"= {V_to_dBm(max(V_small_fn(0, B_x, xe), 1e-9)):.2f} dBm")

# Coupling fraction relative to total at d=0.
V_total_z0 = V_z_smooth[0]
V_total_x0 = V_x_smooth[0]
print("\nCoupling fractions of V_small at the contact point (d -> 0):")
print(f"  Z scan: V_small(0)/V_total(0) = {B_z/V_total_z0*100:.2f}% "
      f"(small / total at z=0)")
print(f"  X scan: V_small(0)/V_total(0) = {B_x/V_total_x0*100:.2f}% "
      f"(small / total at x=0)")

# Goodness-of-fit (dB-domain RMS error of total fit vs smoothed data)
def rms_dB(meas, fit):
    return float(np.sqrt(np.mean((V_to_dBm(meas) - V_to_dBm(np.maximum(fit, 1e-9)))**2)))

print("\nFit residuals (dB-RMS, fit vs smoothed data):")
print(f"  Z scan: {rms_dB(V_z_smooth, V_total_z_fit):.3f} dB")
print(f"  X scan: {rms_dB(V_x_smooth, V_total_x_fit):.3f} dB")


# ==========================================================================
# PLOT  (1x2: data + V_large/V_total fits; no numerical annotations on plot)
#
# Numbers and quantification are intentionally kept out of the figure: the
# parasitic baseline V_large is dominated by reflections and small mechanical
# disturbances on the optical bench that shift the curve by several dB
# between scans, so any specific fit-extracted small-signal amplitude is
# not a robust observable and is not annotated here.
# ==========================================================================
plt.rcParams.update({"font.size": 10})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))


def safe_dBm(arr, floor=1e-9):
    return V_to_dBm(np.maximum(arr, floor))


# --- (a) X sweep, full fit ---
ax1.plot(x_offset, V_to_dBm(V_out_x),       'o', color='#7f8c8d',
         ms=4, alpha=0.4, label='Measured')
ax1.plot(x_offset, V_to_dBm(V_x_smooth),    '-', color='#3498db',
         lw=1.2, alpha=0.85, label='Smoothed')
ax1.plot(x_offset, safe_dBm(V_large_x_fit), '--', color='#e67e22',
         lw=1.8,
         label=r'$V_{\rm large}=V_\infty+(V_0-V_\infty)/[1+(x/L_x)^{\alpha_x}]$')
ax1.plot(x_offset, safe_dBm(V_total_x_fit), '-', color='#e74c3c',
         lw=2.2,
         label=r'$V_{\rm total}=V_{\rm large}+B_x\,e^{-x/x_e}$')
ax1.set_xlabel(r'Lateral offset  $x$  (µm)')
ax1.set_ylabel('Output power (dBm)')
ax1.set_title('(a) X scan', fontsize=11, weight='bold')
ax1.legend(loc='lower left', fontsize=9, framealpha=0.9)
ax1.grid(True, alpha=0.3)
ax1.set_xlim([0, 51])
ax1.set_ylim([-13, -8])

# --- (b) Z sweep, full fit ---
ax2.plot(z_offset, V_to_dBm(V_out_z),       '-', color='#7f8c8d',
         lw=0.5, alpha=0.35, label='Raw')
ax2.plot(z_offset, V_to_dBm(V_z_smooth),    '-', color='#3498db',
         lw=1.2, alpha=0.85, label='Smoothed')
ax2.plot(z_offset, safe_dBm(V_large_z_fit), '--', color='#e67e22',
         lw=1.8,
         label=r'$V_{\rm large}=V_\infty+(V_0-V_\infty)/[1+(z/L)^{\alpha}]$')
ax2.plot(z_offset, safe_dBm(V_total_z_fit), '-', color='#e74c3c',
         lw=2.2,
         label=r'$V_{\rm total}=V_{\rm large}+B\,e^{-z/z_e}$')
ax2.set_xlabel(r'Vertical distance  $z$  (µm)')
ax2.set_ylabel('Output power (dBm)')
ax2.set_title('(b) Z scan', fontsize=11, weight='bold')
ax2.legend(loc='lower left', fontsize=9, framealpha=0.9)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([-5, 255])
ax2.set_ylim([-19, -8])

plt.tight_layout()
plt.savefig('large_small_signal_fits.png', dpi=300, bbox_inches='tight')
print("\nSaved plot: large_small_signal_fits.png")
# plt.show()  # uncomment if you want an interactive window
