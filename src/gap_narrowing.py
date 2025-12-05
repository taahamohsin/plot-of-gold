import pandas as pd
import os

# Cleaning colum names
indicators_to_merge = {
    'education.csv': [
        'literacy rate, adult total (% of people ages 15 and above)',
        'primary completion rate, total (% of relevant age group)',
        'school enrollment, secondary (% gross)'
    ],
    'economy_growth.csv': [
        'gdp per capita (current us$)' 
    ],
    'agriculture_rural_development.csv': [
        'access to electricity, rural (% of rural population)' 
    ],
    'poverty.csv': [
        'poverty headcount ratio at $6.85 a day (2017 ppp) (% of population)' 
    ],
    'infrastructure.csv': [
        'individuals using the internet (% of population)' 
    ]
}

base_cols = ['year', 'country']
merged_df = None

print("--- Starting Time-Series Merge for Education/Health Gap Analysis ---")

for file_name, indicators in indicators_to_merge.items():
    
    if not os.path.exists(file_name):
        print(f"[Warning] File not found: {file_name}. Skipping.")
        continue
        
    try:
        print(f"[Processing] Loading file: {file_name}")
        df = pd.read_csv(file_name)
        
        # Clean and standardize column names 
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Check if the file has the base columns
        if 'year' not in df.columns or 'country' not in df.columns:
            print(f"[Warning] Skipping {file_name}: 'year' or 'country' column not found.")
            continue
            
        # Build list of indicators
        cols_to_select = base_cols.copy()
        for ind in indicators:
            if ind in df.columns:
                cols_to_select.append(ind)
            else:
                print(f"[Warning] Indicator not found in {file_name}: {ind}")
        
        # Create a subset with only needed columns
        subset_df = df[cols_to_select].drop_duplicates(subset=base_cols)
        
        # Merge subset with the main dataframe
        if merged_df is None:
            merged_df = subset_df
            print(f"    ...Initialized merge with {file_name}")
        else:
            merged_df = pd.merge(merged_df, subset_df, on=base_cols, how='outer')
            print(f"    ...Merged data from {file_name}")
            
    except Exception as e:
        print(f"[ERROR] Failed to process {file_name}: {e}")

# Clean & save
if merged_df is not None:
    print("\n--- Finalizing Data ---")
    
    # Sort by country and year 
    merged_df = merged_df.sort_values(by=['country', 'year'])
    
    merged_df = merged_df[merged_df['year'] >= 1990].copy()

    # Save the final cohesive CSV
    output_file = "education_health_gap_data.csv"
    merged_df.to_csv(output_file, index=False)
    
    print(f"\n[SUCCESS] Successfully created '{output_file}'")
    print(f"Final data shape: {merged_df.shape}")
    print("Final columns:", merged_df.columns.tolist())
    
else:
    print("\n[FAILED] No data was merged. Check if files exist and have correct columns.")
