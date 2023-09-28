import sys
"""Takes two Command line arguments: [solutions file] and [puzzles.txt] removes entries in the second that are present in the first"""
def extract_configuration(line):
    line = line.replace("Solving puzzle", "").split(":")[1].strip()
    return " ".join(line.split())

def check_configuration_exists(config_set, config_line):
    config_str = " ".join(config_line.strip().split())
    return config_str in config_set

if len(sys.argv) != 3:
    print("Usage: python script_name.py file_path1 file_path2")
    sys.exit(1)

file_path1 = sys.argv[1]
file_path2 = sys.argv[2]

# Extract configurations from the first file and store them in a set
configurations_set = set()

try:
    with open(file_path1, 'r') as file1:
        for line in file1:
            if "Solving puzzle" in line:
                configurations_set.add(extract_configuration(line))
                
    # Read all configurations from the second file
    with open(file_path2, 'r') as file2:
        lines = file2.readlines()

    # Write only the configurations that have not been solved to the second file
    with open(file_path2, 'w') as file2:
        for line in lines:
            if not check_configuration_exists(configurations_set, line):
                file2.write(line)
            else:
                print(f"Configuration {line.strip()} has already been solved and will be removed.")

except Exception as e:
    print(f"Error: {e}")
