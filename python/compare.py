import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from files
with open('MD.json', 'r') as f:
    data1 = json.load(f)
    
with open('MD_LC.json', 'r') as f:
    data2 = json.load(f)

# Convert data to DataFrame
df1 = pd.DataFrame(data1)
df1['implementation'] = 'Manhattan Distance'

df2 = pd.DataFrame(data2)
df2['implementation'] = 'Manhattan + Linear Conflict'

# Concatenate DataFrames for comparison plots
df = pd.concat([df1, df2])

# Save Individual Subplot Figures
def save_subplots():
    # 4. Side-by-Side Box Plot for Time Taken
    plt.figure(figsize=(5, 4))
    sns.boxplot(x='implementation', y='time_taken_ms', data=df, palette='pastel')
    plt.yscale('log')
    plt.title('Side-by-Side Box Plot for Time Taken')
    plt.xlabel('Implementation')
    plt.ylabel('Time Taken (ms)')
    plt.savefig('BoxPlot_TimeTaken.png')
    plt.close()

    # 5. Overlayed Kernel Density Estimation for Max Search Depth
    plt.figure(figsize=(5, 4))
    sns.kdeplot(df1['max_search_depth'], fill=True, color='skyblue', label='Manhattan Distance')
    sns.kdeplot(df2['max_search_depth'], fill=True, color='lightcoral', label='Manhattan + Linear Conflict')
    plt.title('Overlayed KDE for Max Search Depth')
    plt.xlabel('Max Search Depth')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig('KDE_MaxSearchDepth.png')
    plt.close()

    # 6. Aggregate Bar Graph for Nodes Expanded
    plt.figure(figsize=(5, 4))
    average_nodes_expanded = df.groupby('implementation')['nodes_expanded'].mean().reset_index()
    sns.barplot(x='implementation', y='nodes_expanded', data=average_nodes_expanded, palette='pastel')
    plt.title('Aggregate Bar Graph for Average Nodes Expanded')
    plt.xlabel('Implementation')
    plt.ylabel('Average Nodes Expanded')
    plt.savefig('BarGraph_NodesExpanded.png')
    plt.close()

save_subplots()

# Create a Figure for Comparison Plots
fig = plt.figure(figsize=(15, 10))
fig.suptitle("Comparison between Manhattan Distance and Manhattan + Linear Conflict")

# 4. Side-by-Side Box Plot for Time Taken
ax4 = fig.add_subplot(2, 3, 1)
sns.boxplot(x='implementation', y='time_taken_ms', data=df, palette='pastel', ax=ax4)
ax4.set_yscale('log')
ax4.set_title('Side-by-Side Box Plot for Time Taken')
ax4.set_xlabel('Implementation')
ax4.set_ylabel('Time Taken (ms)')

# 5. Overlayed Kernel Density Estimation for Max Search Depth
ax5 = fig.add_subplot(2, 3, 2)
sns.kdeplot(df1['max_search_depth'], fill=True, color='skyblue', ax=ax5, label='Manhattan Distance')
sns.kdeplot(df2['max_search_depth'], fill=True, color='lightcoral', ax=ax5, label='Manhattan + Linear Conflict')
ax5.set_title('Overlayed KDE for Max Search Depth')
ax5.set_xlabel('Max Search Depth')
ax5.set_ylabel('Density')
ax5.legend()

# 6. Aggregate Bar Graph for Nodes Expanded
ax6 = fig.add_subplot(2, 3, 3)
average_nodes_expanded = df.groupby('implementation')['nodes_expanded'].mean().reset_index()
sns.barplot(x='implementation', y='nodes_expanded', data=average_nodes_expanded, palette='pastel', ax=ax6)
ax6.set_title('Aggregate Bar Graph for Average Nodes Expanded')
ax6.set_xlabel('Implementation')
ax6.set_ylabel('Average Nodes Expanded')

# Adjust the layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
fig.subplots_adjust(bottom=0.2)

# Save the Overall Comparison Figure
fig.savefig('Comparison_Plot.png')

# Show the Multiplot Figure
plt.show()
