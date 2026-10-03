"""Step 4: plot radius against mass for the cleaned planets, on log-log axes."""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("data/clean.csv")

mass = df["pl_bmasse"].to_numpy()
radius = df["pl_rade"].to_numpy()

# Matplotlib wants error bars as a positive number below and above each point.
# err2 is stored as a negative number, so we flip its sign.
mass_err = np.vstack([-df["pl_bmasseerr2"], df["pl_bmasseerr1"]])
radius_err = np.vstack([-df["pl_radeerr2"], df["pl_radeerr1"]])

fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(mass, radius, xerr=mass_err, yerr=radius_err, fmt="o", ms=3.5,
            color="#2a78d6", ecolor="#9db9e0", elinewidth=0.7, alpha=0.8)

# Solar system planets for reference: (mass, radius) in Earth units.
solar_system = {"Earth": (1.0, 1.0), "Neptune": (17.1, 3.88),
                "Saturn": (95.2, 9.45), "Jupiter": (317.8, 11.21)}
for name, (m, r) in solar_system.items():
    ax.plot(m, r, "o", color="#eb6834", ms=7)
    ax.annotate(name, (m, r), xytext=(6, -12), textcoords="offset points", fontsize=9)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Mass (Earth masses)")
ax.set_ylabel("Radius (Earth radii)")
ax.set_title(f"Exoplanet masses and radii ({len(df)} planets)")
ax.grid(alpha=0.3)

Path("figures").mkdir(exist_ok=True)
fig.savefig("figures/mass_radius.png", dpi=200, bbox_inches="tight")
print("Saved figures/mass_radius.png")