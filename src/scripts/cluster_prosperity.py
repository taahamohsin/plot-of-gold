#!/usr/bin/env python3
"""
K-Means Clustering using prosperity_sustainability.csv
This file already has ISO3 country codes which the map needs
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

print("="*60)
print("K-Means Clustering for Country Socioeconomic Profiles")
print("="*60)

print("\n[1/5] Loading data...")
df = pd.read_csv('../data/prosperity_sustainability.csv')

df_latest = df[df['year'] == 2024].copy()

print(f"Total countries in 2024: {len(df_latest)}")
print(f"Sample countries: {', '.join(df_latest['country'].head(10).values)}")

print("\n[2/5] Preparing features...")
features = [
    'gdp per capita (current us$)',
    'renewable energy consumption (% of total final energy consumption)',
    'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)',
    'inflation, consumer prices (annual %)'
]

df_clean = df_latest[['country'] + features].dropna()

print(f"Countries with complete data: {len(df_clean)}")
print(f"Countries dropped due to missing data: {len(df_latest) - len(df_clean)}")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[features])
print("\n[4/5] Performing K-Means clustering (k=4)...")
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df_clean['cluster'] = kmeans.fit_predict(X_scaled)

print(f"Clustering complete. Inertia: {kmeans.inertia_:.2f}")

for i in range(4):
    cluster_data = df_clean[df_clean['cluster'] == i]
    print(f"\n{'='*60}")
    print(f"Cluster {i}: {len(cluster_data)} countries")
    print(f"{'='*60}")
    print("\nMean values:")
    for feat in features:
        print(f"  {feat}: {cluster_data[feat].mean():.2f}")
    print(f"\nSample countries: {', '.join(cluster_data['country'].head(10).values)}")

output = df_clean[['country', 'cluster'] + features].copy()
output['year'] = 2024

output = output.rename(columns={
    'gdp per capita (current us$)': 'gdp',
    'renewable energy consumption (% of total final energy consumption)': 'renewable',
    'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)': 'ghg',
    'inflation, consumer prices (annual %)': 'inflation'
})

output.to_csv('../data/country_clusters.csv', index=False)

print(f"\n{'='*60}")
print(f"✓ Saved {len(output)} countries to ../data/country_clusters.csv")
print(f"{'='*60}")
print("\nCluster distribution:")
print(output['cluster'].value_counts().sort_index())
print("\nFirst 10 countries:")
print(output.head(10))
