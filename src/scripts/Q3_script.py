import pandas as pd

BASE_FILE = "clean/q2_gdp_life_literacy.csv"
POVERTY_FILE = "poverty.csv"
OUTPUT_FILE = "clean/q3_poverty_filled.csv"

POV_COL = "Poverty headcount ratio at $6.85 a day (2017 PPP) (% of population)"

df = pd.read_csv(BASE_FILE)
poverty = pd.read_csv(POVERTY_FILE)

poverty = poverty[["country", "year", POV_COL]].copy()
poverty["country"] = poverty["country"].str.upper()
df["iso3"] = df["iso3"].str.upper()

# Acknowledgment: we used external sources to help with this data wrangling

#  Pivot poverty data into wide format (country to year columns)
poverty_wide = poverty.pivot(index="country", columns="year", values=POV_COL)

# Perform backward fill (use most recent prior value)
poverty_filled = poverty_wide.sort_index(axis=1, ascending=False).bfill(axis=1)

# Melt back to long format
poverty_long = poverty_filled.reset_index().melt(
    id_vars="country",
    var_name="year",
    value_name="poverty_rate_6_85"
)

poverty_long["year"] = poverty_long["year"].astype(int)

merged = df.merge(
    poverty_long,
    left_on=["iso3", "year"],
    right_on=["country", "year"],
    how="left"
).drop(columns=["country"])

merged.to_csv(OUTPUT_FILE, index=False)

print(f"Merge complete with time-fill. Saved as {OUTPUT_FILE}")
print("Missing poverty values:", merged['poverty_rate_6_85'].isna().sum())
