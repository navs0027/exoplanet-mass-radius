"""Step 5: fit a power law, radius = a * mass**b, separately in three mass ranges."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/clean.csv")
mass = df["pl_bmasse"].to_numpy()
radius = df["pl_rade"].to_numpy()

# Mass ranges (Earth masses) to fit separately. This is a starting guess.
# Published work uses edges near 2 and 130. Try both and compare.
RANGES = {
        "low mass (under 2)": (0.0, 2.0),
    "mid mass (2 to 130)": (2.0, 130.0),
    "high mass (over 130)": (130.0, 1e6),
}
MIN_PLANETS = 8     # do not fit a range with fewer planets than this
N_RESAMPLES = 5000  # number of bootstrap resamples

rng = np.random.default_rng(0)  # fixed seed, so you get the same answer every run


def fit_line(log_m, log_r):
    """Straight-line fit in log-log space. Returns (slope b, intercept log10 a)."""
    slope, intercept = np.polyfit(log_m, log_r, 1)
    return slope, intercept


def bootstrap_slope(log_m, log_r):
    """Refit on randomly resampled planets to see how much the slope moves."""
    slopes = []
    for _ in range(N_RESAMPLES):
        pick = rng.integers(0, len(log_m), len(log_m))  # random planets, with repeats
        slopes.append(fit_line(log_m[pick], log_r[pick])[0])
    return np.percentile(slopes, [16, 84])


fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(mass, radius, "o", ms=3.5, color="#9db9e0")

colours = ["#eb6834", "#1baf7a", "#4a3aa7"]
rows = []
for colour, (name, (lo, hi)) in zip(colours, RANGES.items()):
    keep = (mass >= lo) & (mass < hi)
    n = int(keep.sum())
    if n < MIN_PLANETS:
        print(f"{name}: only {n} planets, skipped")
        continue
    log_m, log_r = np.log10(mass[keep]), np.log10(radius[keep])
    slope, intercept = fit_line(log_m, log_r)
    low, high = bootstrap_slope(log_m, log_r)
    rows.append({"range": name, "n_planets": n, "slope": slope,
                 "slope_low_16": low, "slope_high_84": high,
                 "radius_at_1_earth_mass": 10**intercept})

    grid = np.logspace(np.log10(mass[keep].min()), np.log10(mass[keep].max()), 50)
    ax.plot(grid, 10**intercept * grid**slope, color=colour, lw=2.5,
            label=f"{name}: slope {slope:.2f} (n = {n})")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Mass (Earth masses)")
ax.set_ylabel("Radius (Earth radii)")
ax.set_title("Power-law fits in three mass ranges")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
Path("figures").mkdir(exist_ok=True)
fig.savefig("figures/fits.png", dpi=200, bbox_inches="tight")

results = pd.DataFrame(rows)
results.to_csv("results.csv", index=False)
print(results.round(3).to_string(index=False))
print()
print("Saved figures/fits.png and results.csv")