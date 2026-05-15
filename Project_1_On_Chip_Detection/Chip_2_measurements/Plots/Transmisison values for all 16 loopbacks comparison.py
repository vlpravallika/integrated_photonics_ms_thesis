"""
Transmission vs structure number for 16 loopback structures @ 1595 nm, 0 dBm input.
Case 1: Angled interfaces (fiber array || x, interfaces not parallel).
Case 2: Parallel interfaces (structures slightly angled, both edges parallel).
Theoretical best: -14 dBm per edge → -28 dBm total (perfect alignment, perfect edges, rib).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Structure numbers 1–16
structures = np.arange(1, 17)

# Case 1: Angled interfaces (dBm)
case1 = np.array([-77, -75, -53, -68, -74, -69, -61, -54, -56, -57, -68, -67, -64, -67, -67, -64])

# Case 2: Parallel interfaces (dBm) — structure 8 corrected to -53 dBm
case2 = np.array([-72, -71, -51, -67, -69, -67, -65, -53, -54, -55, -65, -66, -67, -66, -66, -66])

THRESHOLD_DBM = -65       # Acceptable transmission threshold
THEORETICAL_BEST_DBM = -28  # Best case: -14 dB/edge × 2 edges

# Acceptable structures (by structure number)
ACCEPTABLE_STRUCTURES = (3, 7, 8, 9, 10)
acceptable_mask = np.isin(structures, ACCEPTABLE_STRUCTURES)

# --- Single plot: transmission vs structure number ---
# Two lines (Case 1, Case 2) so transmission vs structure is clear; Case 2 above Case 1 → better coupling evident.
# Good structures highlighted; -28 dBm and -60 dBm reference lines.
fig, ax = plt.subplots(figsize=(12, 6))

x = structures
# ax.plot(x, case1, "o-", color="#2E86AB", linewidth=2, markersize=8, label="Case 1 (angled interfaces)", zorder=2)
# ax.plot(x, case2, "s-", color="#A23B72", linewidth=2, markersize=8, label="Case 2 (parallel interfaces)", zorder=2)
ax.plot(x, case1, "o", linestyle="None",
        color="#2E86AB", markersize=8,
        label="Case 1 (angled interfaces)", zorder=2)

ax.plot(x, case2, "s", linestyle="None",
        color="#A23B72", markersize=8,
        label="Case 2 (parallel interfaces)", zorder=2)


# Highlight acceptable structures (3, 7, 8, 9, 10)
for i in range(len(structures)):
    if acceptable_mask[i]:
        ax.plot(structures[i], case1[i], "o", color="#06D6A0", markersize=12, markeredgecolor="black", markeredgewidth=1, zorder=3)
        ax.plot(structures[i], case2[i], "s", color="#FFD166", markersize=12, markeredgecolor="black", markeredgewidth=1, zorder=3)

# Theoretical best (-28 dBm) — dotted, labeled (y-axis extended so this line is visible)
ax.axhline(THEORETICAL_BEST_DBM, color="darkgreen", linestyle=":", linewidth=2.5, label=f"Theoretical best ({THEORETICAL_BEST_DBM} dBm, -14 dB/edge)", zorder=1)
ax.axhline(THRESHOLD_DBM, color="gray", linestyle="--", linewidth=1.5, label=f"Acceptable threshold ({THRESHOLD_DBM} dBm)", zorder=1)

ax.set_xlabel("Structure number")
ax.set_ylabel("Transmission (dBm)")
ax.set_title("Loopback transmission @ 1595 nm, 0 dBm input (16 structures)")
ax.set_xticks(structures)
ax.set_xlim(0.5, 16.5)
ax.set_ylim(-80, -25)  # extend top to show theoretical best at -28 dBm
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right", fontsize=9)

# Text box: acceptable structures (3, 7, 8, 9, 10) and their transmission values
good_ix = np.where(acceptable_mask)[0]
lines = ["Acceptable structures: 3, 7, 8, 9, 10", ""]
struct_list_1 = ", ".join(f"{structures[i]} ({case1[i]:.0f})" for i in good_ix)
struct_list_2 = ", ".join(f"{structures[i]} ({case2[i]:.0f})" for i in good_ix)
lines.append("Case 1 (angled):  " + struct_list_1 + " dBm")
lines.append("Case 2 (parallel): " + struct_list_2 + " dBm")
ax.text(0.02, 0.98, "\n".join(lines), transform=ax.transAxes, fontsize=8, verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))

plt.tight_layout()
out_path = r"c:\Users\prava\MIT\QP\Chip 2 measurements\Plots\transmission_vs_structure.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print("Saved:", out_path)
plt.close()

# Console summary
print("Acceptable structures: 3, 7, 8, 9, 10")
print("  Case 1 (angled):", [f"{structures[i]} ({case1[i]:.0f} dBm)" for i in good_ix])
print("  Case 2 (parallel):", [f"{structures[i]} ({case2[i]:.0f} dBm)" for i in good_ix])
