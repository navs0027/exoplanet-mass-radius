"""Step 6: turn mass and radius into density, and see where planets stop being rocky."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

EARTH_DENSITY = 5.514  # g/cm^3

df = pd.read_csv("data/clean.csv")

# Density scales as mass / radius^3. In Earth units, Earth has mass 1 and radius 1,
# so the density in g/cm^3 is just Earth's density times mass / radius^3.
df["density"] = EARTH_DENSITY * df["pl_bmasse"] / df["pl_rade"] ** 3

# Sanity check against the density the archive lists. Most should agree closely.
ratio = (df["density"] / df["pl_dens"]).dropna()
print(f"Our density / archive density: median {ratio.median():.3f} (n = {len(ratio)})")
print()

# Group planets into radius bins and summarise the density in each bin.
edges = [0.5, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 6.0, 10.0, 16.0]
df["bin"] = pd.cut(df["pl_rade"], edges)
table = df.groupby("bin", observed=True)["density"].agg(
    n="count",
    median="median",
    low_16=lambda s: s.quantile(0.16),
    high_84=lambda s: s.quantile(0.84),
)
print(table.round(2).to_string())
print()

# One simple definition of the "rocky to gas-rich" transition. Change the number
# and see how the answer moves.
THRESHOLD = 3.5  # g/cm^3
below = table[(table["median"] < THRESHOLD) & (table["n"] >= 3)]
if len(below):
    print(f"First radius bin with median density below {THRESHOLD}: {below.index[0]}")

# Plot every planet, then the median in each bin.
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(df["pl_rade"], df["density"], "o", ms=3.5, color="#9db9e0")
mid = [b.mid for b in table.index]
ax.plot(mid, table["median"], "o-", color="#eb6834", lw=2, label="median in each bin")
ax.axhline(EARTH_DENSITY, color="#444444", ls="--", lw=1)
ax.text(0.55, EARTH_DENSITY * 1.07, "Earth (5.5)", fontsize=9)
ax.axhline(1.0, color="#444444", ls=":", lw=1)
ax.text(0.55, 1.07, "water (1.0)", fontsize=9)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Radius (Earth radii)")
ax.set_ylabel("Density (g/cm$^3$)")
ax.set_title("Planet density against radius")
ax.legend(loc="upper right")
ax.grid(alpha=0.3)
Path("figures").mkdir(exist_ok=True)
fig.savefig("figures/density.png", dpi=200, bbox_inches="tight")

table.to_csv("density_by_radius.csv")
print("Saved figures/density.png and density_by_radius.csv")