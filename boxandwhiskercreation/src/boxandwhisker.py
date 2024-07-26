import os
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dataformatting import csv_to_dict_box
from sssecret import remotepath

# Define transfer size colors
transfer_size_colors = {
    '10 GB': 'blue', '10 MB': 'green'
}

path = remotepath + "\\boxandwhiskercreation\\output\\"

# Get file paths from command line arguments and read data from the csv files
file_paths = sys.argv[1:3]  # Assuming the first two arguments after the script name are file paths
machine1 = sys.argv[3]
machine2 = sys.argv[4]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
data = csv_to_dict_box(file_paths[0], file_paths[1], machine1, machine2) 

# Iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)
    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    if (day['timestamp'][0].date() != pd.Timestamp.now().date() and 
        os.path.exists(rf'{path}Box and Whisker - {day_text} Transfers.pdf')):
        continue
    # Group data by machine, then by transfer size, and ensure each group has sets of 3 data points
    grouped = df.groupby(['machine', 'type'])

    # Prepare figure for plotting
    plt.figure(figsize=(28, 8))
    positions = []
    box_data = []
    colors = []
    labels = []

    # Iterate over groups to prepare data for box plots
    for (machine, transfer_size), group in grouped:
        if len(group) >= 3:  # Ensure there are at least 3 data points
            # Calculate position for the box plot
            position = len(positions) + 1
            positions.append(position)
            # Prepare data for the box plot
            box_data.append(group['transferspeed_MB/s'].values[:3])  # Take first 3 data points
            colors.append(transfer_size_colors[transfer_size])
            labels.append(f"{machine} - {transfer_size}")

    # Create box plots
    box = plt.boxplot(box_data, positions=positions, patch_artist=True)
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # Add labels and title
    plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha="right")
    plt.ylabel('Transfer Speed (MB/s)')
    plt.title(f'Box and Whisker Plot for {day}')

    # Calculate and display statistical values directly on the plot
for i, transfer_size in enumerate(['10 GB', '10 MB']):
    ts_data = df[df['type'] == transfer_size]['transferspeed_MB/s']
    std_dev = np.std(ts_data)
    variance = np.var(ts_data)
    # Annotate the plot with Std Dev and Variance for each transfer size
    # Adjust the y-position as needed to avoid overlapping with the plot elements
    y_position = min(ts_data) - 0.05 * min(ts_data)  # Example position, adjust as needed
    plt.text(i + 1, y_position, f"Std Dev: {std_dev:.2f}\nVariance: {variance:.2f}", ha='center')

    plt.savefig(rf'{path}Box and Whisker - {day_text} Transfers.pdf', format='pdf')

    # Show plot
    plt.show()