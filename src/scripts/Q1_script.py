import pandas as pd
import os

master = pd.read_csv("world_bank_indicators.csv")

country_meta = pd.read_csv("country_meta.csv")

country_meta["iso3"] = country_meta["iso3"].str.lower()

col_country = "country"
col_year    = "year"
col_gdp_pc  = "GDP per capita (current US$)"
col_life    = "Life expectancy at birth, total (years)"

q1 = master[[col_country, col_year, col_gdp_pc, col_life]].copy()

q1 = q1[q1[col_year] >= 1990].dropna(subset=[col_gdp_pc, col_life], how="all")

q1 = q1.merge(country_meta, left_on="country", right_on="iso3", how="inner")

q1 = q1.sort_values(["country", "year"]).reset_index(drop=True)

os.makedirs("clean", exist_ok=True)
out_path = "clean/gdp_lifeexpectancy.csv"
q1.to_csv(out_path, index=False)

print(f"Saved cleaned file to: {out_path}")
