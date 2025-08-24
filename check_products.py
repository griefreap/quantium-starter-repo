import os
import csv

input_folder = "data"

csv_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]

products_found = set()

for filename in csv_files:
    with open(os.path.join(input_folder, filename), "r", newline="") as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            product_name = row["product"].strip()
            products_found.add(product_name)

print("Products found in data files:")
for product in sorted(products_found):
    print(product)
