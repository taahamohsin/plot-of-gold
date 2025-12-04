import requests
import pandas as pd
import os

# 1) Fetch JSON for all countries
url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
resp = requests.get(url)
resp.raise_for_status()
data = resp.json()

# Format: data[0] = metadata, data[1] = list of country objects
country_list = data[1]

# 2) Extract relevant fields
records = []
for c in country_list:
    # skip if “aggregate” based on region.id or incomeLevel.id perhaps
    rec = {
        "iso3": c["id"],                     # e.g. "USA"
        "country_name": c["name"],           # e.g. "United States"
        "region": c["region"]["value"],      # e.g. "North America"
        "income_group": c["incomeLevel"]["value"]  # e.g. "High income"
    }
    records.append(rec)

# 3) Create DataFrame
df_meta = pd.DataFrame(records)

# 4) (Optional) Filter out aggregates: e.g., rows where region or income_group = "Aggregates" or empty
df_meta = df_meta[~df_meta["region"].str.contains("aggregate", case=False)]
df_meta = df_meta[~df_meta["income_group"].str.contains("income only", case=False)]

# 5) Lowercase iso3 codes so they match your dataset
df_meta["iso3"] = df_meta["iso3"].str.lower()

out_path = "country_meta.csv"
df_meta.to_csv(out_path, index=False)

print("Saved country metadata to:", out_path)
