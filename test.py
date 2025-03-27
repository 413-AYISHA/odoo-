import json
import csv
import glob

# Get all JSON files in the directory
json_files = glob.glob("*.json")

# Initialize list to store bank data
bank_data_list = []

# Load data from each JSON file
for json_file in json_files:
    with open(json_file, 'r') as file:
        bank_data = json.load(file)
        for key in bank_data.keys():
            bank_data_list.append({
                "BANK": bank_data[key]['BANK'],
                "BRANCH": bank_data[key]['BRANCH'],
                "IFSC": bank_data[key]['IFSC']
            })

# Writing to a CSV file
with open('bank_data.csv', 'w', newline='') as csvfile:
    fieldnames = ["BANK", "BRANCH", "IFSC"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data
    writer.writerows(bank_data_list)

print("CSV file 'bank_data.csv' created successfully from multiple JSON files.")
