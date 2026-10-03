"""Step 3: keep only planets whose mass and radius we can trust, and save them."""
import pandas as pd

# Thresholds you can change later to see what happens to the result.
MAX_MASS_ERR = 0.25    # drop planets whose mass is uncertain by more than 25 %
MAX_RADIUS_ERR = 0.10  # drop planets whose radius is uncertain by more than 10 %

df = pd.read_csv("data/pscomppars.csv")
print(f"Start:                                   {len(df)} planets")

# Cut 1: we need both a mass and a radius.
df = df.dropna(subset=["pl_rade", "pl_bmasse"])
print(f"After requiring a mass and a radius:     {len(df)}")

# Cut 2: keep only real, measured masses. Some masses in the archive were
# estimated FROM the radius using a mass-radius relation. Using those would be
# circular, because we are trying to find that relation.
df = df[df["pl_bmassprov"] == "Mass"].copy()
print(f"After keeping only measured masses:      {len(df)}")

# Cut 3: keep planets with small uncertainties. The archive gives the upper
# error (err1, positive) and the lower error (err2, negative), so the average
# size of the error is (err1 - err2) / 2. A planet with a missing error becomes
# NaN here, fails the comparison below, and is dropped.
df["mass_frac_err"] = (df["pl_bmasseerr1"] - df["pl_bmasseerr2"]) / 2 / df["pl_bmasse"]
df["radius_frac_err"] = (df["pl_radeerr1"] - df["pl_radeerr2"]) / 2 / df["pl_rade"]
good = (df["mass_frac_err"] < MAX_MASS_ERR) & (df["radius_frac_err"] < MAX_RADIUS_ERR)
df = df[good]
print(f"After the uncertainty cuts:              {len(df)}")

print()
print("Mass range (Earth masses):  ", df["pl_bmasse"].min(), "to",
      df["pl_bmasse"].max())
print("Radius range (Earth radii): ", df["pl_rade"].min(), "to", df["pl_rade"].max())

df.to_csv("data/clean.csv", index=False)
print()
print("Saved", len(df), "planets to data/clean.csv")