import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
import matplotlib.dates as mdates
from dataformatting import multi_csv_to_dict

# define protocol node colors
protocol_colors = {
    'pn001': 'red', 'pn002': 'blue', 'pn003': 'green',
    'pn004': 'purple', 'pn005': 'orange', 'pn006': 'brown'
}

# get file path from command line argument and splice the machine name
file_path = sys.argv[1]
machine = file_path.split(".")[0].split("/")[-1]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
data = csv_to_dict(file_path)
# iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)
    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')

    # isolate 10 GB and 10 MB data
    gb_data = df[df['type'] == '10 GB']
    mb_data = df[df['type'] == '10 MB']

    ### plotting

    # calculate figure width by range of timestamps
    time_range = day['timestamp'].max() - day['timestamp'].min()
    time_range_hours = time_range.total_seconds() / 3600
    fig_width = 10 + time_range_hours * 2
    plt.figure(figsize=(fig_width, 8)) 

    # scatter plot for 10 GB transfers with square markers mapping color to protocol node
    plt.scatter(gb_data['timestamp'], gb_data['transferspeed_MB/s'], s=100, c=gb_data['protocolnode'].map(protocol_colors), marker='s', label='10 GB')

    # scatter plot for 10 MB transfers with circle markers mapping color to protocol node
    plt.scatter(mb_data['timestamp'], mb_data['transferspeed_MB/s'], s=100, c=mb_data['protocolnode'].map(protocol_colors), marker='o', label='10 MB')

    # add labels and title
    plt.xlabel('Timestamp')
    plt.ylabel('Transfer Speed (MB/s)')
    plt.title(f'{machine} File Transfers on {day_text}')

    # create legend for transfer size and protocol nodes
    size_legend = plt.legend(title="Transfer Size", loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    protocol_patches = [Patch(color=color, label=protocol) for protocol, color in protocol_colors.items()]
    # add the transfer size and protocol node legends to the plot
    plt.legend(handles=protocol_patches, title="Protocol Nodes", loc='upper right', bbox_to_anchor=(1.15, 0.85), borderaxespad=0.)
    plt.gca().add_artist(size_legend)

    # format x axis to show date and time in 30 minute intervals
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # Ensure a half-hour interval
    plt.xticks(rotation=45)
    # set the x-axis limits to first and last timestamp
    plt.xlim(day['timestamp'].min() - pd.Timedelta(minutes=30), day['timestamp'].max() + pd.Timedelta(minutes=30))
    # set the y-axis limits to min and max
    transferspeed_array = np.array(day['transferspeed_MB/s'])
    plt.ylim(transferspeed_array.min() - 50, transferspeed_array.max() + 50)

    # save plot as PDF
    plt.savefig(f'../output/Scatterplot - {machine} {day_text} Transfers.pdf', format='pdf', bbox_inches='tight')
    # display interactive plot
    plt.show()