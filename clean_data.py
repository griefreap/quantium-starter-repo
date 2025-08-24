import csv
import os

input_folder = "data"
output_file = "cleaned_sales.csv"

csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

with open(output_file, "w", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Sales", "Date", "Region"])

    for filename in csv_files:
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", newline="") as infile:
            reader = csv.DictReader(infile)

            for row in reader:
                if row["product"].strip().lower() == "pink mors":
                    try:
                        quantity = int(row["quantity"])
                        price = float(row["price"].replace("$", ""))
                        sales = quantity * price
                        date = row["date"]
                        region = row["region"]
                        writer.writerow([sales, date, region])
                    except Exception as e:
                        print(f"Skipping row due to error: {e}")
