import pandas as pd
from pathlib import Path

# Path to data folder
data_folder = Path("data")

# Get all CSV files
csv_files = list(data_folder.glob("*.csv"))

# Create an empty list to store DataFrames
df_list = []

# Process each file
for file in csv_files:
    df = pd.read_csv(file)
    
    # Filter for Pink Morsel
    df = df[df["product"] == "Pink Morsel"]
    
    # Create Sales column
    df["Sales"] = df["quantity"] * df["price"]
    
    # Keep only required columns
    df = df[["Sales", "date", "region"]]
    
    # Rename columns to match desired output
    df.rename(columns={"date": "Date", "region": "Region"}, inplace=True)
    
    # Append to list
    df_list.append(df)

# Combine all into one DataFrame
final_df = pd.concat(df_list)

# Save to CSV
final_df.to_csv("formatted_sales.csv", index=False)

print("✅ formatted_sales.csv created successfully!")
