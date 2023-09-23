import json
import sys
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

if len(sys.argv) != 2:
    print("Usage: python script_name.py file_path")
    sys.exit(1)

file_path = sys.argv[1]
# file_path = "solutions-master.json"
try:
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        data = json.load(file)

    if not data:
        print("Error: Empty JSON file.")
        sys.exit(1)
    
    # Extracting max_search_depth and time_taken_ms values
    search_depths = [entry.get('max_search_depth', 0) for entry in data]
    # convert to seconds 
    times = [entry.get('time_taken_ms', 0)//1000 for entry in data]

    # Calculating y-axis limits
    y_min = math.floor(min(times))
    y_max = math.ceil(max(times))

    # Sorting the values based on search_depth for better visualization
    sorted_values = sorted(zip(search_depths, times))
    search_depths, times = zip(*sorted_values)
    
    # Plotting the chart
    plt.figure(figsize=(10, 5))
    plt.plot(search_depths, times, marker='o', linestyle='-')
    plt.xlabel('Max Search Depth')
    plt.ylabel('Time Taken (s)')
    plt.title('Comparison of Max Search Depth and Time Taken (s)')
    plt.xticks(range(40, 80,5))  # Setting x-axis ticks to whole numbers
    plt.ylim(1, 20000)  # Setting the y-axis limit to 1 to 20000 seconds
    plt.yticks(range(0, 20000, 1000))  # Setting y-axis ticks every 1000 seconds

    plt.grid(True)
    plt.show()

except json.JSONDecodeError:
    print("Error: Invalid JSON file.")
except Exception as e:
    print(f"Error: {e}")
