"""
Calculate and plot the direct absorption of a Gaussian mode exiting an SMF‑28 fibre into a
horizontal detector placed beside the fibre in 2‑D.  This script computes the fraction of
power captured as a function of vertical offset from the fibre core and converts it to dBm
for a 0 dBm (1 mW) launch power.

Assumptions:

  • Mode field diameter (MFD) of SMF‑28 at 1550 nm: 10.4 µm → beam waist radius w0 = 5.2 µm.
    (Corning/Photon Engineering note that using a 5.2 µm waist and 1.55 µm wavelength
    yields a 1/e² divergence half‑angle of ≈5.42°:contentReference[oaicite:0]{index=0}.)
  • Launch power P_in = 1 mW (0 dBm).
  • Horizontal detector length d = 1 mm (1000 µm); multiple centre positions x are evaluated.
  • The fibre is modelled as emitting a 2‑D Gaussian far‑field intensity profile
    I(θ) ∝ exp[−2 (θ/θ0)^2], where θ0 = λ/(π w0) is the 1/e² divergence half‑angle in radians.
  • The detector intercepts rays subtended by angles θ2 ≤ θ ≤ θ1, where
      θ1 = atan(z / x_left),  θ2 = atan(z / x_right).
    Here x_left = max(0, x_center − d/2) and x_right = x_center + d/2.
  • The fraction of power captured is
        F(z) = erf(√2 θ1/θ0) − erf(√2 θ2/θ0)
    and the received power in dBm is 10·log10(F), provided F > 0; otherwise −∞.

For each x in [600, 700, 800, 900, 1000] µm the script writes a CSV file and plots the
received power vs. z with a legend.
"""

import numpy as np
import matplotlib.pyplot as plt
from math import atan, erf, sqrt, pi, log10

def gaussian_divergence_half_angle(lambda_um: float, w0_um: float) -> float:
    """Return the 1/e² divergence half‑angle (in radians) for a Gaussian beam."""
    return lambda_um / (pi * w0_um)

def fraction_captured(z_um: float, x_center_um: float, d_um: float, theta0: float) -> float:
    """Compute the fraction of power captured by the detector at height z (µm)."""
    x_left = x_center_um - d_um / 2.0
    x_right = x_center_um + d_um / 2.0
    # The fibre does not emit backwards; clamp x_left to zero if it is negative.
    if x_left < 0:
        theta1 = np.pi / 2  # 90°
    else:
        theta1 = atan(z_um / x_left) if x_left != 0 else np.pi / 2
    theta2 = atan(z_um / x_right) if x_right != 0 else 0.0
    # Ensure theta1 ≥ theta2
    if theta1 < theta2:
        theta1, theta2 = theta2, theta1
    # Convert to dimensionless u variables and use the error function
    u1 = sqrt(2) * theta1 / theta0
    u2 = sqrt(2) * theta2 / theta0
    return erf(u1) - erf(u2)

def compute_dataset(z_range: np.ndarray, x_center_um: float, d_um: float,
                    lambda_um: float, w0_um: float) -> tuple:
    """Compute the fraction and dBm power over a range of z values."""
    theta0 = gaussian_divergence_half_angle(lambda_um, w0_um)
    fractions = np.zeros_like(z_range, dtype=float)
    power_dbm = np.full_like(z_range, -np.inf, dtype=float)
    for i, z in enumerate(z_range):
        F = fraction_captured(z, x_center_um, d_um, theta0)
        fractions[i] = F
        if F > 0:
            power_dbm[i] = 10.0 * log10(F)  # 0 dBm launch; 10·log10(F·1 mW / 1 mW) = 10·log10(F)
    return z_range, fractions, power_dbm

def main():
    # Fibre parameters
    lambda_um = 1.55      # Wavelength (µm) for 1550 nm
    w0_um = 5.2           # Waist radius (µm) for 10.4 µm MFD
    d_um = 1000.0         # Detector length (1 mm in µm)

    # Range of vertical offsets from 0 to 100 µm (inclusive) in 1 µm steps
    z_values = np.arange(0.0, 101.0, 1.0)

    # Define a set of horizontal offsets for the detector centre
    x_centres = [600.0, 700.0, 800.0, 900.0, 1000.0]

    # Prepare a figure for plotting multiple curves
    plt.figure(figsize=(8, 5))

    import csv

    # Loop over each horizontal offset and compute the dataset
    for x_ctr in x_centres:
        # Compute fraction and power for this x
        z_vals, fractions, power_dbm = compute_dataset(z_values, x_ctr, d_um,
                                                      lambda_um, w0_um)
        # Replace −∞ values (log10(0)) with a floor for plotting
        finite_power = np.where(np.isfinite(power_dbm), power_dbm, -120.0)
        # Plot the received power vs height for this x
        plt.plot(z_vals, finite_power, label=f'x = {int(x_ctr)} µm')
        # Save CSV for this x
        csv_path = f'absorption_vs_z_x{int(x_ctr)}.csv'
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['z_um', 'fraction_captured', 'power_dbm'])
            for z, F, p in zip(z_vals, fractions, power_dbm):
                writer.writerow([z, F, p])
        print(f'Data for x = {int(x_ctr)} µm saved to {csv_path}')

    # Label and format the plot
    plt.xlabel('Vertical offset from fibre core z [µm]')
    plt.ylabel('Received power [dBm] (0 dBm launch)')
    plt.title('Direct absorption vs vertical offset (2‑D Gaussian model)')
    plt.grid(True)
    plt.legend(title='Detector centre offset')
    plt.tight_layout()
    # Save the plot.  Change this path to a valid location on your system as needed.
    plot_path = 'absorption_plot_multiple.png'  # e.g. r'C:\\Users\\prava\\MIT\\QP\\absorption_plot.png'
    plt.savefig(plot_path, dpi=300)
    print(f'Plot saved to {plot_path}')
    # plt.show()

if __name__ == '__main__':
    main()
