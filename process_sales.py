import csv
import os

input_folder = 'data'
output_file = 'cleaned_sales.csv'

# Get list of all CSV files in the input folder
csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

# Open the output CSV file for writing
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write header row
    writer.writerow(['Sales', 'Date', 'Region'])
    
    # Iterate over each CSV file
    for filename in csv_files:
        input_path = os.path.join(input_folder, filename)
        
        with open(input_path, 'r', newline='') as infile:
            reader = csv.DictReader(infile)
            
            for row in reader:
                # Use .get to safely access keys and default to empty string if missing
                product = row.get('product', '').strip().lower()
                
                if product == 'pink morsel':
                    try:
                        quantity = int(row.get('quantity', 0))
                        price = float(row.get('price', 0))
                        sales = quantity * price
                        date = row.get('date', '')
                        region = row.get('region', '')
                        
                        # Only write row if sales, date and region have valid values
                        if sales > 0 and date and region:
                            writer.writerow([sales, date, region])
                    except ValueError:
                        # Skip rows with invalid numeric conversion
                        continue
