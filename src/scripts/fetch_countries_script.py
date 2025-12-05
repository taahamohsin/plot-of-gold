import requests
import pandas as pd
import os

url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
resp = requests.get(url)
resp.raise_for_status()
data = resp.json()

country_list = data[1]

records = []
for c in country_list:
    rec = {
        "iso3": c["id"],
        "country_name": c["name"],
        "region": c["region"]["value"],
        "income_group": c["incomeLevel"]["value"]
    }
    records.append(rec)

df_meta = pd.DataFrame(records)

df_meta = df_meta[~df_meta["region"].str.contains("aggregate", case=False)]
df_meta = df_meta[~df_meta["income_group"].str.contains("income only", case=False)]

df_meta["iso3"] = df_meta["iso3"].str.lower()

out_path = "country_meta.csv"
df_meta.to_csv(out_path, index=False)

print("Saved country metadata to:", out_path)
