# from datetime import datetime

# def convert_timestamp_to_date(timestamp):
#     """
#     Convert a Linux timestamp to a date string.

#     Args:
#     timestamp (int): Linux timestamp.

#     Returns:
#     str: Date in the format YYYY-MM-DD.
#     """
#     date = datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
#     return date

# # Example usage
# linux_timestamp = 1690838400  # Corresponds to 2023-07-31
# date_string = convert_timestamp_to_date(linux_timestamp)
# print(date_string)  # Output: 2023-07-31


import yaml
import csv
import os

# Function to read and parse YAML file content correctly
def read_yaml(file_path):
    records = []
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        # Split records on double newlines between entries
        entries = content.strip().split('\n\n')
        for entry in entries:
            try:
                record_data = yaml.safe_load(entry)
                if isinstance(record_data, dict):
                    records.append(record_data)
            except yaml.YAMLError as exc:
                print(f"Error parsing YAML entry: {exc}")
                continue
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return records

# Function to read existing CSV file content
def read_csv(csv_file_path):
    data = []
    if os.path.exists(csv_file_path):
        try:
            with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
    return data

# Function to write data to CSV file
def write_to_csv(data, csv_file_path):
    if not data:
        return

    # Extract column names from the keys of all dictionaries
    columns = set()
    for record in data:
        if isinstance(record, dict):
            columns.update(record.keys())
    columns = list(columns)

    try:
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in data:
                if isinstance(row, dict):
                    # Ensure each cell is properly escaped
                    escaped_row = {k: (v if v is not None else '') for k, v in row.items()}
                    writer.writerow(escaped_row)
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# Path to the YAML file
yaml_file_path = 'output.yaml'

# Read YAML file
yaml_data = read_yaml(yaml_file_path)

# Path to the CSV file
csv_file_path = 'output1.csv'

# Clear the CSV file before writing new data
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)

# Write new data to CSV file
write_to_csv(yaml_data, csv_file_path)

print(f"CSV file updated: {csv_file_path}")
