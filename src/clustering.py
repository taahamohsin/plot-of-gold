import pandas as pd
import os

# All the csvs and indicators to merge
indicators_to_merge = {
    'economy_growth.csv': [
        'gdp per capita (current us$)'
    ],
    'financial_sector.csv': [
        'inflation, consumer prices (annual %)',
        'domestic credit to private sector (% of gdp)'
    ],
    'poverty.csv': [
        'poverty headcount ratio at $6.85 a day (2017 ppp) (% of population)'
    ],
    'education.csv': [
        'literacy rate, adult total (% of people ages 15 and above)',
        'school enrollment, secondary (% gross)'
    ],
    'infrastructure.csv': [
        'individuals using the internet (% of population)',
        'mobile cellular subscriptions (per 100 people)',
        'electric power consumption (kwh per capita)'
    ],
    'agriculture_rural_development.csv': [
        'rural population (% of total population)'
    ],
    'climate_change.csv': [
        'population growth (annual %)'
    ],
    'environment.csv': [
        'renewable energy consumption (% of total final energy consumption)',
        'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)'
    ]
}

base_cols = ['year', 'country']
merged_df = None

print("--- Starting Merge for Socio-Economic Profile Data (Q3) ---")

# Merging files

for file_name, indicators in indicators_to_merge.items():
    if not os.path.exists(file_name):
        print(f"[Warning] File not found: {file_name}. Skipping.")
        continue
        
    try:
        print(f"[Processing] Loading file: {file_name}")
        df = pd.read_csv(file_name)
        df.columns = [col.strip().lower() for col in df.columns]
        if 'year' not in df.columns or 'country' not in df.columns:
            print(f"[Warning] Skipping {file_name}: 'year' or 'country' column not found.")
            continue
        cols_to_select = base_cols.copy()
        for ind in indicators:
            if ind in df.columns:
                cols_to_select.append(ind)
            else:
                print(f"[Warning] Indicator not found in {file_name}: {ind}")
        
        subset_df = df[cols_to_select].drop_duplicates(subset=base_cols)
        
        if merged_df is None:
            merged_df = subset_df
            print(f"    ...Initialized merge with {file_name}")
        else:
            merged_df = pd.merge(merged_df, subset_df, on=base_cols, how='outer')
            print(f"    ...Merged data from {file_name}")
            
    except Exception as e:
        print(f"[ERROR] Failed to process {file_name}: {e}")

# Cleaning data
if merged_df is not None:
    print("\n--- Finalizing Data (Creating Most Recent Snapshot) ---")
    
    merged_df = merged_df[merged_df['year'] >= 2010].copy()
    
    merged_df = merged_df.sort_values(by=['country', 'year'])

    print("Forward-filling missing data within each country...")
    merged_df = merged_df.groupby('country').ffill()
    
    print("Resetting index...")
    merged_df = merged_df.reset_index()
    
    # renaming country column
    if 'country' not in merged_df.columns:
        print("[INFO] 'country' column not found, renaming 'index' column.")
        if 'index' in merged_df.columns:
            merged_df = merged_df.rename(columns={'index': 'country'})
        else:
            print("[ERROR] Catastrophic error: Neither 'country' nor 'index' found after reset.")
            

    print("Selecting most recent snapshot for each country...")
    final_df = merged_df.drop_duplicates(subset=['country'], keep='last')
    
    print("Dropping rows with any remaining missing data...")
    original_count = final_df.shape[0]
    final_df = final_df.dropna()
    new_count = final_df.shape[0]
    print(f"    ...Dropped {original_count - new_count} countries with incomplete profiles.")

    # Save into CSV
    output_file = "socioeconomic_profiles.csv"
    final_df.to_csv(output_file, index=False)
    
    print(f"\n[SUCCESS] Successfully created '{output_file}'")
    print(f"Final data shape: {final_df.shape}")
    print("Final columns:", final_df.columns.tolist())
    
else:
    print("\n[FAILED] No data was merged. Check if files exist and have correct columns.")


