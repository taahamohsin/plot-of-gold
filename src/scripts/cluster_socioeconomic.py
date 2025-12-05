import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('../data/socioeconomic_profiles@1.csv')
country_meta = pd.read_csv('../data/country_meta.csv')

print("Socioeconomic columns:", df.columns.tolist()[:5])
print("Meta columns:", country_meta.columns.tolist())
df_latest = df.sort_values('year').groupby('country').tail(1)

features = [
    'gdp per capita (current us$)',
    'renewable energy consumption (% of total final energy consumption)',
    'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)',
    'individuals using the internet (% of population)',
    'electric power consumption (kwh per capita)'
]

df_clean = df_latest[['country'] + features].dropna()

print(f"Countries with complete data: {len(df_clean)}")
print(f"Countries dropped: {len(df_latest) - len(df_clean)}")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[features])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clean['cluster'] = kmeans.fit_predict(X_scaled)

print("\nCluster Summary:")
for i in range(4):
    cluster_data = df_clean[df_clean['cluster'] == i]
    print(f"\nCluster {i} ({len(cluster_data)} countries):")
    print(cluster_data[features].mean())
    print(f"Sample countries: {', '.join(cluster_data['country'].astype(str).head(5).values)}")

prosperity_df = pd.read_csv('../data/prosperity_sustainability.csv')

print("\nProsperity file sample:")
print(prosperity_df[['country', 'year']].head())

output = df_clean[['country', 'cluster']].copy()


print("\nCountry values in cleaned data:")
print(df_clean['country'].head(20))

output['country'] = output['country'].astype(str)
output['year'] = 2024

output.to_csv('../data/country_clusters.csv', index=False)

print(f"\nSaved {len(output)} countries to ../data/country_clusters.csv")
print("\nFirst few rows:")
print(output.head(10))
