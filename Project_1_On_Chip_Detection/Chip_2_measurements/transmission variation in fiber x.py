import numpy as np
import matplotlib.pyplot as plt

V = np.array([
    14.3, 14.3, 14.3, 14.3, 13.9, 14.3, 14.3, 13.7, 14.3, 14.1, 14.3, 14.1, 14.3,
    14.2, 13.5, 14.2, 14.3, 13.8, 14.3, 14.3, 14.3, 13.5, 14.3,
    14.2, 13.8, 14.2, 13.7, 14.3, 14.1, 14.2, 13.6, 13.5, 12.1,
    11.9, 11.3, 12.4, 12.6, 12.8, 12.7, 13.0, 12.7, 11.7, 11.5,
    11.1, 11.1, 10.7, 11.2, 11.0, 10.6, 11.2
], dtype=float)

# x positions: 0,1,2,... in microns (edit if you have a different x mapping)
x_um = np.arange(len(V))  # 0..46 µm here

# 1) Raw voltage plot
plt.figure()
plt.plot(x_um, V, marker='o', linewidth=1)
plt.xlabel("Fiber alignment x (µm)")
plt.ylabel("Detector output (V)")
plt.title("Detector output vs fiber alignment (raw)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 2) Min-max scaled to [0, 1]
V_scaled = (V - V.min()) / (V.max() - V.min())

plt.figure()
plt.plot(x_um, V_scaled, marker='o', linewidth=1)
plt.xlabel("Fiber alignment x (µm)")
plt.ylabel("Scaled detector output (0 to 1)")
plt.title("Detector output vs fiber alignment (min-max scaled)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 3) Relative dB w.r.t. maximum (voltage ratio)
V_db = 20 * np.log10(V / V.max())

plt.figure()
plt.plot(x_um, V_db, marker='o', linewidth=1)
plt.xlabel("Fiber alignment x (µm)")
plt.ylabel("Relative output (dB re. max)")
plt.title("Detector output vs fiber alignment (relative dB)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()