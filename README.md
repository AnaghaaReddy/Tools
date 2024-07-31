# Tools

import yaml
import csv
import os

# Function to read and parse YAML file content correctly
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split records on empty lines between entries
    entries = content.split('\n\n')

    records = []
    for entry in entries:
        if entry.strip():  # ignore empty sections
            record_data = yaml.safe_load(entry)
            records.append(record_data)

    return records

# Function to read existing CSV file content
def read_csv(csv_file_path):
    data = []
    if os.path.exists(csv_file_path):
        with open(csv_file_path, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    return data

# Function to write data to CSV file
def write_to_csv(data, csv_file_path):
    if not data:
        return

    # Extract column names from the keys of the first dictionary
    columns = data[0].keys()
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=columns)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Path to the YAML file
yaml_file_path = 'output.yaml'

# Read YAML file
yaml_data = read_yaml(yaml_file_path)

# Path to the CSV file
csv_file_path = 'output1.csv'

# Read existing CSV data
csv_data = read_csv(csv_file_path)

# Append new YAML data to existing CSV data
csv_data.extend(yaml_data)

# Write combined data to CSV file
write_to_csv(csv_data, csv_file_path)

print(f"CSV file updated: {csv_file_path}")
