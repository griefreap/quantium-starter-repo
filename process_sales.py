from pathlib import Path
import pandas as pd


def load_and_clean_one(csv_path: Path) -> pd.DataFrame:
    """Load one raw CSV and return cleaned Pink Morsel rows."""
    df = pd.read_csv(csv_path)

    # normalize product & region
    df["product"] = df["product"].astype(str).str.strip().str.lower()
    df["region"] = df["region"].astype(str).str.strip().str.lower()

    # keep only Pink Morsel
    pink = df[df["product"] == "pink morsel"].copy()
    if pink.empty:
        return pink  # empty frame

    # clean price -> number
    pink["price"] = (
        pink["price"]
        .astype(str)
        .str.strip()
        .str.replace(r"[$,]", "", regex=True)
        .astype(float)
    )

    # compute Sales
    pink["Sales"] = pink["quantity"].astype(float) * pink["price"]

    # pick/rename columns
    out = pink[["Sales", "date", "region"]].rename(
        columns={"date": "Date", "region": "Region"}
    )

    # normalize date to datetime (kept as string when saving)
    out["Date"] = pd.to_datetime(out["Date"]).dt.date.astype(str)
    return out


def main() -> None:
    data_dir = Path("data")
    csvs = sorted(data_dir.glob("*.csv"))

    if not csvs:
        print("❌ No CSVs found in ./data")
        return

    frames = []
    for p in csvs:
        print(f"Processing {p.name} ...")
        frames.append(load_and_clean_one(p))

    if not frames:
        print("❌ No data loaded.")
        return

    final = pd.concat(frames, ignore_index=True)
    if final.empty:
        print("❌ No Pink Morsel rows found in any file.")
        final.to_csv("cleaned_sales.csv", index=False)
        return

    final = final.sort_values("Date")
    final.to_csv("cleaned_sales.csv", index=False)
    print(f"✅ cleaned_sales.csv written with {len(final)} rows.")


if __name__ == "__main__":
    main()
