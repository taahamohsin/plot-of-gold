import pandas as pd

gdp = pd.read_csv("clean/gdp_lifeexpectancy.csv")
edu = pd.read_csv("education.csv")

gdp['iso3'] = gdp['iso3'].str.upper()

col_iso     = "iso3"
col_country = "country_name"
col_year    = "year"
col_gdp     = "GDP per capita (current US$)"
col_life    = "Life expectancy at birth, total (years)"
col_group   = "income_group"
col_lit     = "Literacy rate, adult total (% of people ages 15 and above)"
iso_col_edu = "Country Code" if "Country Code" in edu.columns else "country"

edu_latest = (
    edu.dropna(subset=[col_lit])
       .sort_values(col_year)
       .groupby(iso_col_edu)
       .tail(1)
       .rename(columns={iso_col_edu: col_iso})
       [[col_iso, col_lit]]
)

gdp_latest = (
    gdp.dropna(subset=[col_gdp, col_life])
       .sort_values(col_year)
       .groupby(col_iso)
       .tail(1)
       [[col_iso, col_country, col_year, col_gdp, col_life, col_group]]
)

merged = pd.merge(gdp_latest, edu_latest, on=col_iso, how="inner")

merged[col_lit] = (
    merged[col_lit]
    .astype(str)
    .str.strip()
    .str.extract(r"([\d\.]+)", expand=False)
    .str.strip()
    .astype(float)
)

merged = merged.dropna(subset=[col_lit])

bucket_bins = [0, 60, 80, 90, 100]
bucket_labels = ["<60%", "60-80%", "80-90%", "90-100%"]

merged["literacy_bucket"] = pd.cut(
    merged[col_lit],
    bins=bucket_bins,
    labels=bucket_labels,
    include_lowest=True,
    right=True
)

merged["literacy_bucket"] = merged["literacy_bucket"].astype("category")
merged["literacy_bucket"] = merged["literacy_bucket"].cat.set_categories(
    bucket_labels, ordered=True
)

merged["gdp_tier"] = pd.qcut(
    merged["GDP per capita (current US$)"],
    q=4,
    labels=["Low GDP", "Lower-Mid GDP", "Upper-Mid GDP", "High GDP"]
)


out_path = "clean/q2_gdp_life_literacy.csv"
merged.to_csv(out_path, index=False)

print(f"Saved cleaned Q2 dataset to: {out_path}")
print(f"Countries included: {merged.shape[0]}")
