import pandas as pd

BASE = "clean/q3_poverty_filled.csv"
ENV = "environment.csv"
OUT = "clean/q4_env_merged.csv"

ENV_COL = "Carbon intensity of GDP (kg CO2e per 2021 PPP $ of GDP)"

base = pd.read_csv(BASE)
env = pd.read_csv(ENV)

env['iso3'] = env['country'].str.upper()

env = env[['iso3', 'year', ENV_COL]]

print(f"Base rows: {len(base)}, Env rows: {len(env)}")
print("Unique iso3 in base:", base['iso3'].nunique())
print("Unique iso3 in env :", env['iso3'].nunique())

merged = base.merge(env, on=['iso3', 'year'], how='left')

print("Rows after merge:", len(merged))
missing = merged[ENV_COL].isna().sum()
print(f"Missing carbon intensity values: {missing} / {len(merged)}")

merged.to_csv(OUT, index=False)
print(f"Saved merged file to {OUT}")
