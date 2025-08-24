import pandas as pd
from pathlib import Path

def clean_file(file_path: Path) -> pd.DataFrame:
    """Clean one daily sales CSV file and return only Pink Morsel rows."""
    df = pd.read_csv(file_path)
    # Standardize product and region
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df["region"] = df["region"].astype(str).str.strip().str.capitalize()

    # Filter for pink morsel
    pink_df = df[df["product"] == "pink morsel"].copy()

    # Clean price (remove $ and commas)
    pink_df["price"] = (
        pink_df["price"]
        .astype(str)
        .str.replace(r"[$,]", "", regex=True)
        .astype(float)
    )

    # Calculate sales
    pink_df["Sales"] = pink_df["quantity"].astype(float) * pink_df["price"]

    # Keep only Sales, Date, Region
    cleaned = pink_df.rename(columns={"date": "Date", "region": "Region"})
    cleaned = cleaned[["Sales", "Date", "Region"]]
    cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")
    return cleaned


def main():
    data_dir = Path("data")
    files = list(data_dir.glob("*.csv"))
    if not files:
        print("❌ No CSV files found in the 'data' folder.")
        return

    all_data = []
    print("🔍 Processing files:")
    for file in files:
        print(f" - {file.name}")
        all_data.append(clean_file(file))

    final_df = pd.concat(all_data, ignore_index=True).dropna()
    final_df = final_df.sort_values("Date")
    print(f"✅ Processed {len(final_df)} rows total.")

    final_df.to_csv("cleaned_sales.csv", index=False)
    print("💾 Saved cleaned_sales.csv")


if __name__ == "__main__":
    main()
