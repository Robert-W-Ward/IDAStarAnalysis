import sys
import json
"""Removes duplicate etries in the solutions JSON"""
if len(sys.argv) != 2:
    print("Usage: python script_name.py file_path")
    sys.exit(1)

file_path = sys.argv[1]

try:
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Use a dictionary to keep track of unique configurations
    unique_entries = {}
    for entry in data:
        config = entry.get('configuration', '')
        if config not in unique_entries:
            unique_entries[config] = entry
        else:
            print(f"Duplicate configuration {config} found. Removing duplicates.")
    
    # Write the unique entries back to the file
    with open(file_path, 'w') as file:
        json.dump(list(unique_entries.values()), file, indent=4)

except Exception as e:
    print(f"Error: {e}")
