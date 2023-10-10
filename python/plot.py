import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from files
with open('MD_LC.json', 'r') as f:
    data1 = json.load(f)

# Convert data to DataFrame
df = pd.DataFrame(data1)
df['implementation'] = 'Manhattan Distance + Linear Conflict'

# 1. Histogram for Max Search Depth - Implementation 1
fig1, ax1 = plt.subplots(figsize=(5, 4))
fig1.subplots_adjust(bottom=0.2)
sns.histplot(df['max_search_depth'], kde=False, bins=20, color='skyblue', ax=ax1)
ax1.set_title('Histogram for Max Search Depth\nManhattan Dist.+Linear Conflict')
ax1.set_xlabel('Max Search Depth')
ax1.set_ylabel('Frequency')
fig1.savefig('Histogram_Max_Search_Depth_MD_LC.png')

# 2. Box Plot for Time Taken - Implementation 1
fig2, ax2 = plt.subplots(figsize=(5, 4))
fig2.subplots_adjust(bottom=0.2)

sns.boxplot(x='time_taken_ms', data=df, color='lightgreen', ax=ax2)
ax2.set_xscale('log')
ax2.set_yscale('linear')
ax2.set_title('Box Plot for Time Taken\nManhattan Dist.+Linear Conflict')
ax2.set_xlabel('Time Taken (ms)')

fig2.savefig('Box_Plot_Time_Taken_MD_LC.png')

# 3. Density Plot for Nodes Expanded - Implementation 1
fig3, ax3 = plt.subplots(figsize=(5, 4))
fig3.subplots_adjust(bottom=0.2)

sns.kdeplot(df['nodes_expanded'], fill=True, color='lightcoral', ax=ax3)
ax3.set_xscale("log")
ax3.set_yscale("linear")
ax3.set_title('Density Plot for Nodes Expanded\nManhattan Dist.+Linear Conflict')
ax3.set_xlabel('Nodes Expanded')
ax3.set_ylabel('Density')
fig3.savefig('Density_Plot_Nodes_Expanded_MD_LC.png')

plt.show()
