import sys
import json
import re
"""Takes two command line arguments [formatted-solutions.txt] and [path to save JSON] and converts the regular formatted text file to JSON and saves it at the designated location"""
# Check if correct number of command line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python script_name.py input_file_path output_file_path")
    sys.exit(1)

# Fetch the input and output file paths from command line arguments
input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

# Initialize the list to store the puzzles
puzzles = []

# Read the input file and parse the content
try:
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    puzzle = {}
    for line in lines:
        # Find the puzzle configuration
        if line.startswith("Solving puzzle"):
            match = re.match(r"Solving puzzle \d+: ([\d\s]+)", line.strip())
            if match:
                configuration = match.group(1)
                puzzle = {"configuration": configuration.strip()}
        
        # Find the path and steps
        elif line.startswith("Path found with steps:"):
            steps = line[len("Path found with steps: "):].strip()
            puzzle["steps"] = steps
        
        # Find the max search depth reached for the puzzle
        elif line.startswith("Max search depth reached for puzzle"):
            match = re.match(r"Max search depth reached for puzzle \d+: (\d+)", line.strip())
            if match:
                max_search_depth = int(match.group(1))
                puzzle["max_search_depth"] = max_search_depth
        
        # Find the time taken
        elif line.startswith("Time taken"):
            match = re.match(r"Time taken (\d+) ms", line.strip())
            if match:
                time_taken = int(match.group(1))
                puzzle["time_taken_ms"] = time_taken
                puzzles.append(puzzle)

    # Save the parsed content to the output file in JSON format
    with open(output_file_path, 'w') as file:
        json.dump(puzzles, file, indent=4)

except Exception as e:
    print(f"Error: {e}")
