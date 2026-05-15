"""Plot received power vs z for x = 600 µm and a linear fit."""

import numpy as np
import matplotlib.pyplot as plt
from math import atan, erf, sqrt, pi, log10

# Parameters
lambda_um = 1.55
w0_um = 5.2
d_um = 1000.0
x_um = 600.0

z = np.arange(0.0, 101.0, 1.0)
theta0 = lambda_um / (pi * w0_um)
x_left = max(0, x_um - d_um / 2)
x_right = x_um + d_um / 2

# Power (dBm) vs z
power_dbm = np.zeros_like(z)
for i, zi in enumerate(z):
    t1 = atan(zi / x_left) if x_left else np.pi / 2
    t2 = atan(zi / x_right) if x_right else 0.0
    if t1 < t2:
        t1, t2 = t2, t1
    u1 = sqrt(2) * t1 / theta0
    u2 = sqrt(2) * t2 / theta0
    F = erf(u1) - erf(u2)
    power_dbm[i] = 10.0 * log10(F) if F > 0 else -120.0

# Fit (use only finite points)
mask = np.isfinite(power_dbm) & (power_dbm > -100)
z_fit = z[mask]
y_fit = power_dbm[mask]
a, b = np.polyfit(z_fit, y_fit, 1)
fit_line = a * z + b

# Plot curve and fit
plt.figure(figsize=(8, 5))
plt.plot(z, power_dbm, 'b-', label='x = 600 µm')
plt.plot(z, fit_line, 'r--', label=f'Fit: P = {a:.4g}*z + {b:.4g}')
plt.xlabel('Vertical offset z [µm]')
plt.ylabel('Received power [dBm]')
plt.title('Direct absorption from fiber to detector curve fit')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(r'C:\Users\prava\MIT\QP\Models\absorption_plot_fit.png', dpi=300)
plt.show()
