import pandas as pd

# Define file names
files = [
    'aid_effectiveness.csv', 'climate_change.csv', 'economy_growth.csv',
    'education.csv', 'environment.csv', 'external_debt.csv',
    'financial_sector.csv', 'infrastructure.csv', 'poverty.csv',
    'private_sector.csv'
]

# Cleaning data 
dfs = {}
print("--- Step 1: Loading and Cleaning Columns ---")
for f in files:
    try:
        df = pd.read_csv(f)
        df.columns = [col.strip().lower() for col in df.columns]
        dfs[f] = df
        print(f"[SUCCESS] Loaded {f}. Cleaned columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"[ERROR] Failed to load {f}: {e}")
print("\n--- Step 2: Checking for 'year' and 'country' columns ---")
base_cols = ['year', 'country']
for f_name in list(dfs.keys()):
    df = dfs[f_name]
    # Check for 'year' 
    if 'year' not in df.columns:
        print(f"[WARNING] {f_name} is missing 'year' column. Removing from merge.")
        del dfs[f_name]
        continue
    
    # Check for 'country'
    if 'country' not in df.columns:
        print(f"[WARNING] {f_name} is missing 'country' column. Removing from merge.")
        del dfs[f_name]
        continue 
        
    print(f"[INFO] {f_name} passed check.")
print(f"\n--- Step 3: Starting merge with remaining files ---")
print(f"Files to be merged: {list(dfs.keys())}")

# Processing data and merging
print("\n--- Step 4: Merging relevant indicators ---")
prosperity_sources = {
    'economy_growth.csv': [
        'gdp per capita (current us$)', 'gdp (current us$)'
    ],
    'financial_sector.csv': [
        'inflation, consumer prices (annual %)'
    ],
    'poverty.csv': [
        'poverty headcount ratio at $6.85 a day (2017 ppp) (% of population)'
    ]
}
sustainability_sources = {
    'environment.csv': [
        'renewable energy consumption (% of total final energy consumption)',
        'pm2.5 air pollution, mean annual exposure (micrograms per cubic meter)',
        'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)'
    ],
    'climate_change.csv': [
        'energy use (kg of oil equivalent) per $1,000 gdp (constant 2021 ppp)'
    ],
    'infrastructure.csv': [
        'access to electricity (% of population)'
    ]
}
all_sources = {**prosperity_sources, **sustainability_sources}

merged_df = None

# Iterate through each file 
for file_name, desired_cols in all_sources.items():
    if file_name in dfs:
        df = dfs[file_name]
        cols_to_select = base_cols.copy()
        found_cols = False
        for col in desired_cols:
            if col in df.columns:
                cols_to_select.append(col)
                found_cols = True
        
        if found_cols:
            print(f"Selecting columns from {file_name}: {cols_to_select}")
            subset_df = df[cols_to_select].drop_duplicates(subset=base_cols)
            
            if merged_df is None:
                merged_df = subset_df
            else:
                merged_df = pd.merge(merged_df, subset_df, on=base_cols, how='outer')
        else:
            print(f"[INFO] Could not find any of the desired indicators in {file_name}")
    else:
        print(f"[INFO] {file_name} was not in the list of files to merge. Skipping.")

# Save data
if merged_df is not None:
    print("\n--- Step 5: Cleaning and Finalizing Data ---")
    
    merged_df = merged_df[merged_df['year'] >= 2010].copy()
    print("Sorting by country and year...")
    merged_df = merged_df.sort_values(by=['country', 'year'])
    
    print("Setting index to ['country', 'year']...")
    merged_df = merged_df.set_index(['country', 'year'])
    
    print("Grouping by country and forward-filling...")
    merged_df = merged_df.groupby(level='country').ffill()
    
    print("Resetting index...")
    merged_df = merged_df.reset_index()

    print("Selecting most recent data for each country...")
    final_df = merged_df.drop_duplicates(subset=['country'], keep='last')
    
    print("Dropping rows with missing critical indicators...")
    
    gdp_col_found = None
    if 'gdp per capita (current us$)' in final_df.columns:
        gdp_col_found = 'gdp per capita (current us$)'
    elif 'gdp (current us$)' in final_df.columns:
        gdp_col_found = 'gdp (current us$)'

    critical_indicators = [
        gdp_col_found,
        'total greenhouse gas emissions excluding lulucf per capita (t co2e/capita)',
        'renewable energy consumption (% of total final energy consumption)'
    ]
    critical_indicators = [col for col in critical_indicators if col is not None and col in final_df.columns]

    if critical_indicators:
        print(f"Dropping rows missing critical indicators: {critical_indicators}")
        final_df = final_df.dropna(subset=critical_indicators)
    else:
        print("Warning: No critical indicators found. Dropping rows with any NaNs.")
        final_df = final_df.dropna()
        
    output_csv = 'prosperity_sustainability.csv'
    final_df.to_csv(output_csv, index=False)
    
    print(f"\n[FINAL SUCCESS] Successfully preprocessed and saved data to '{output_csv}'")
    print(f"Final DataFrame shape: {final_df.shape}")

else:
    print("\n--- FINAL ERROR ---")
    print("Failed to create merged DataFrame. This usually means no files passed the 'year' and 'country' check in Step 2.")