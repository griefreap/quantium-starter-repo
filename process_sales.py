import csv
import os

# Folder containing the data files
input_folder = 'data'

# Output file name
output_file = 'cleaned_sales.csv'

# Automatically get all CSV files in the data folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Open the output file for writing
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Sales', 'Date', 'Region'])  # Write header

    # Loop through each input CSV file
    for filename in csv_files:
        with open(os.path.join(input_folder, filename), 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            
            # Process each row
            for row in reader:
                if row['product'].strip().lower() == 'pink morsel':
                    try:
                        quantity = int(row['quantity'])
                        price = float(row['price'])
                        sales = quantity * price
                        date = row['date']
                        region = row['region']
                        writer.writerow([sales, date, region])
                    except (ValueError, KeyError):
                        # Skip rows with missing or invalid data
                        continue
