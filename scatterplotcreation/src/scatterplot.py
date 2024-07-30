import os
import sys
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
import matplotlib.dates as mdates
from dataformatting import csv_to_dict, multi_csv_to_dict
from ssecret import remotepath

# define protocol node colors
protocol_colors = {
    'pn001': 'red', 'pn002': 'blue', 'pn003': 'green',
    'pn004': 'purple', 'pn005': 'orange', 'pn006': 'brown'
}

# get file path from command line argument and splice the machine name
file_path = sys.argv[1]
remotepath += "\\scatterplotcreation\\output\\"
# check if the path needs to be local or remote
path = remotepath if sys.argv[2] == 'r' else '../scatterplotcreation/output/'
machine = sys.argv[3]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
non_multi = True if 'multithreaded' not in file_path else False
data = csv_to_dict(file_path) if non_multi else multi_csv_to_dict(file_path)

# iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)
    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    if day['timestamp'][0].date() != pd.Timestamp.now().date():
        if os.path.exists(rf'{path}Scatterplot - {machine} {day_text} Transfers.pdf') and non_multi:
            continue
        elif os.path.exists(rf'{path}Scatterplot - {machine} Multithreaded {day_text} Transfers.pdf') and not non_multi:
            continue
    if non_multi:
        # isolate 10 GB and 10 MB data
        gb_data = df[df['type'] == '10 GB']
        mb_data = df[df['type'] == '10 MB']
    else:
        # isolate multithreaded and singlethreaded data
        multi_data = df[df['threadtype'] == 'multi']
        single_data = df[df['threadtype'] == 'single']

    ### plotting

    fig = go.Figure()
    for protocol, color in protocol_colors.items():
        protocol_data = df[df['protocolnode'] == protocol]
        fig.add_trace(go.Scatter(x=protocol_data['timestamp'], 
                                 y=protocol_data['transferspeed_MB/s'], 
                                 mode='markers', 
                                 marker=dict(color=color), 
                                 name=protocol))
        
    # add labels and title
    fig.update_layout(title=f'Scatterplot - {machine} {"Multithreaded" if not non_multi else ""} {day_text} Transfers',
                        xaxis_title='Timestamp',
                        xaxis=dict(
                            tickmode='auto',  # Plotly will automatically determine ticks
                            tickformat='%m-%d %I:%M %p',  # Format for date-time ticks
                            rangeslider=dict(visible=True)  # Optional: add a range slider
                        ),
                        yaxis_title='Transfer Speed (MB/s)',
                        legend_title='Protocol Nodes',
                        legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=1))

    

    # save plot as PDF
    if non_multi:
        fig.write_html(rf'{path}Scatterplot - {machine} {day_text} Transfers.html')
    else:
        fig.write_html(rf'{path}Scatterplot - {machine} Multithreaded {day_text} Transfers.html')
    
    # display interactive plot
    fig.show()