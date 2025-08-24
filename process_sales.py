import pandas as pd
from pathlib import Path

# Path to data folder
data_folder = Path("data")

# Get all CSV files
csv_files = list(data_folder.glob("*.csv"))
if not csv_files:
    print("❌ No CSV files found in the 'data' folder!")
    exit()

df_list = []

for file in csv_files:
    print(f"Processing {file}...")
    df = pd.read_csv(file)

    # Clean and normalize product names
    df["product"] = df["product"].str.strip().str.lower()

    # Filter only pink morsel
    filtered = df[df["product"] == "pink morsel"]

    # Clean price column: remove '$' and convert to float
    filtered["price"] = filtered["price"].replace("[\$,]", "", regex=True).astype(float)

    # Calculate Sales
    filtered["Sales"] = filtered["quantity"] * filtered["price"]

    # Select and rename columns
    filtered = filtered[["Sales", "date", "region"]]
    filtered.rename(columns={"date": "Date", "region": "Region"}, inplace=True)

    df_list.append(filtered)

# Combine everything
if df_list:
    final_df = pd.concat(df_list, ignore_index=True)
    final_df.sort_values(by="Date", inplace=True)
    final_df.to_csv("cleaned_sales.csv", index=False)
    print(f"✅ cleaned_sales.csv created with {len(final_df)} rows!")
else:
    print("❌ No data to save! Please check your CSV files.")
