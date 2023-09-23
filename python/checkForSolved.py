import sys
"""Takes two Command line arguments: [puzzles.txt] and [solutions file] checks if entries in the second are present in the first"""
def extract_configuration(line):
    line = line.replace("Solving puzzle", "").split(":")[1].strip()
    return " ".join(line.split())

def check_configuration_exists(config_set, config_line):
    config_str = " ".join(config_line.strip().split())
    return config_str in config_set


if len(sys.argv) != 3:
    print("Usage: python checkForSolved.py [path to puzzles file] [path to solutions file]")
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
                
    # Check configurations in the second file
    with open(file_path2, 'r') as file2:
        for line in file2:
            if check_configuration_exists(configurations_set, line):
                print(f"Configuration {line.strip()} has already been solved.")

except Exception as e:
    print(f"Error: {e}")
