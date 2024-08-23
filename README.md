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









import os
import re

def process_file(file_path):
    try:
        # Open the file in binary mode to handle encoding issues manually
        with open(file_path, 'rb') as fpa:
            for line_no, line in enumerate(fpa):
                try:
                    # Try to decode the line using utf-8
                    line = line.decode('utf-8').strip()
                except UnicodeDecodeError:
                    # If decoding fails, replace problematic characters
                    line = line.decode('utf-8', errors='replace').strip()
                
                # Process the line if it contains the desired pattern
                if 'set (MODEL NAME' in line:
                    res = re.findall(r'"([^"]*)"', line)
                    if res:
                        load_name = res[0]
                        if load_name == "LOADNAME":
                            dummy_load = True
                            print(f"Found matching load name '{load_name}' at line {line_no}")

    except Exception as e:
        print(f"An error occurred while processing file {file_path}: {e}")

# Main function to handle the file processing
def main():
    cmakelists_file = 'path/to/your/file.txt'  # Update this with the correct file path
    
    if os.path.exists(cmakelists_file):
        process_file(cmakelists_file)
    else:
        print(f"File {cmakelists_file} does not exist.")

if __name__ == "__main__":
    main()




import pandas as pd

def process_csv(file_path):
    try:
        # Try reading the file with 'utf-8' encoding
        df = pd.read_csv(file_path, encoding='utf-8', error_bad_lines=False)
    except UnicodeDecodeError:
        # If that fails, try with 'ISO-8859-1' encoding
        df = pd.read_csv(file_path, encoding='ISO-8859-1', error_bad_lines=False)

    # Process your DataFrame here
    # Example: Filtering based on 'MODEL NAME' column
    filtered_df = df[df['MODEL NAME'].str.contains("LOADNAME", na=False)]
    print(filtered_df)

# Call the function
process_csv('path/to/your/file.csv')




import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as fpa:
        raw_data = fpa.read(10000)  # Read a sample of the file
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Detected encoding: {encoding}")
        return encoding

def process_file_with_detected_encoding(file_path):
    encoding = detect_encoding(file_path)
    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as fpa:
            for line_no, line in enumerate(fpa):
                line = line.strip()
                if 'set (MODEL NAME' in line:
                    res = re.findall(r'"([^"]*)"', line)
                    if res:
                        load_name = res[0]
                        if load_name == "LOADNAME":
                            print(f"Found matching load name '{load_name}' at line {line_no}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main logic
def main():
    file_path = 'path/to/your/file.txt'
    if os.path.exists(file_path):
        process_file_with_detected_encoding(file_path)

   
