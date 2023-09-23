import sys
"""Takes two Command line arguments [puzzles.txt] and [file_with_unsolvable] and removes all entries in the second from the first"""
def extract_configuration(line):
    return " ".join(line.strip().split())

if len(sys.argv) != 3:
    print("Usage: python script_name.py file_path1 file_path2")
    sys.exit(1)

file_path1 = sys.argv[1]
file_path2 = sys.argv[2]

try:
    # Extract configurations from the second file and store them in a set
    configurations_set = set()
    
    with open(file_path2, 'r') as file2:
        for line in file2:
            configurations_set.add(extract_configuration(line))
                
    # Read all configurations from the first file
    with open(file_path1, 'r') as file1:
        lines = file1.readlines()

    # Write only the configurations that are not in the second file back to the first file
    with open(file_path1, 'w') as file1:
        for line in lines:
            config_str = extract_configuration(line)
            if config_str not in configurations_set:
                file1.write(line)
            else:
                print(f"Configuration {config_str} is present in both files and will be removed from the first file.")
except Exception as e:
    print(f"Error: {e}")
