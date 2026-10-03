"""Step 2: look at the raw data before doing anything to it."""
import pandas as pd

df = pd.read_csv("data/pscomppars.csv")

print("Rows and columns:", df.shape)
print()
print("Column names:")
print(df.columns.tolist())
print()
print("First five rows:")
print(df.head())
print()
print("Missing values in each column:")
print(df.isna().sum())
print()
print("Where does each planet's mass come from?")
print(df["pl_bmassprov"].value_counts(dropna=False))
print()
both = df.dropna(subset=["pl_rade", "pl_bmasse"])
print("Planets with both a radius and a mass:", len(both))