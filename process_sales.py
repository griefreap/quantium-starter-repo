import pandas as pd
from pathlib import Path

# Define the path to your data folder
data_folder = Path("data")

# Find all CSV files in the data folder
csv_files = list(data_folder.glob("*.csv"))

# List to store processed DataFrames
df_list = []

for file in csv_files:
    # Read the CSV
    df = pd.read_csv(file)
    
    # Keep only rows with "Pink Morsel"
    df = df[df["product"] == "Pink Morsel"]
    
    # Calculate Sales
    df["Sales"] = df["quantity"] * df["price"]
    
    # Keep only the required columns
    df = df[["Sales", "date", "region"]]
    df.rename(columns={"date": "Date", "region": "Region"}, inplace=True)
    
    # Add to list
    df_list.append(df)

# Combine all DataFrames
final_df = pd.concat(df_list, ignore_index=True)

# Optional: sort by Date for readability
final_df.sort_values(by="Date", inplace=True)

# Save final CSV
output_file = "formatted_sales.csv"
final_df.to_csv(output_file, index=False)

print(f"✅ Successfully created {output_file} with {len(final_df)} rows!")
