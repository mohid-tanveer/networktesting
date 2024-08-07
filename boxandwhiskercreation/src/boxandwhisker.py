import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
import uuid
import pandas as pd
import os
import sys
from dataformatting import csv_to_dict_box
from scipy.stats import ttest_ind # type: ignore
import numpy as np

# Define transfer size colors
transfer_size_colors = {
    '10 GB': 'crimson', '10 MB': 'crimson'
}


path = "../output/"

# get file paths from command line arguments and read data from the csv files
file_paths = sys.argv[1:3]
machine1 = sys.argv[3]
machine2 = sys.argv[4]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
data = csv_to_dict_box(file_paths[0], file_paths[1], machine1, machine2) 

# iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)
    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    for transfer_size in ['10 GB', '10 MB']:
        if (day['timestamp'][0].date() != pd.Timestamp.now().date() and 
            os.path.exists(rf'{path}Box and Whisker - {day_text} {transfer_size} Transfers.html')):
            print("file exists")
            continue
        elif (df[(df['machine'] == machine1) & (df['type'] == transfer_size)].empty 
              or df[(df['machine'] == machine2) & (df['type'] == transfer_size)].empty):
            
            continue
        # prepare figure for plotting
        fig = make_subplots(rows=1, cols=1)

        machines =[machine1, machine2]
        # iterate over machines and transfer sizes to prepare data for box plots
        for machine in machines:
            group = df[(df['machine'] == machine) & (df['type'] == transfer_size)]
            if not group.empty:
                hover_text = group['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
                fig.add_trace(go.Box(y=group['transferspeed_MB/s'], 
                                     name=f'{machine} {transfer_size}',
                                     marker_color=transfer_size_colors[transfer_size],
                                     boxpoints='all',
                                     jitter=0.3,
                                     pointpos=-1.8,
                                     boxmean='sd',
                                     notched=True,
                                     text=hover_text,
                                     hoverinfo='y+text',
                                     line=dict(color='black', width=2),
                                     fillcolor=transfer_size_colors[transfer_size],
                                     showlegend=False
                                     ))

        # create box plots
        fig.update_layout(title_text=f'{machine1} vs {machine2} - {transfer_size} Transfers',
                          yaxis_title='Transfer Speed (MB/s)',
                          margin=dict(b=170))

        # calculate and display statistical values for each machine
        stats_text = ""
        for machine in machines:
            machine_data = df[(df['machine'] == machine) & (df['type'] == transfer_size)]['transferspeed_MB/s']
            std_dev = np.std(machine_data)
            variance = np.var(machine_data)
            stats_text += f"{machine}<br>Std Dev: {std_dev:.2f}<br>Variance: {variance:.2f}<br><br>"
        fig.add_annotation(text=stats_text, xref="paper", yref="paper",
                       x=0.5, y=-0.24, showarrow=False, align="center")

        machine1_data = df[(df['machine'] == machines[0]) & (df['type'] == transfer_size)]['transferspeed_MB/s']
        machine2_data = df[(df['machine'] == machines[1]) & (df['type'] == transfer_size)]['transferspeed_MB/s']
        t_stat, p_value = ttest_ind(machine1_data, machine2_data)

        # display the t-test results
        t_test_text = f"T-test results:<br>T-statistic: {t_stat:.2f}<br>P-value: {p_value:.2e}"
        if p_value < 0.05:
            t_test_text += "<br>Difference is statistically significant"
        else:
            t_test_text += "<br>No significant difference"
        fig.add_annotation(text=t_test_text, xref="paper", yref="paper",
                       x=0.5, y=-0.34, showarrow=False, align="center", font=dict(size=10))
        fig.write_html(f'{path}Box and Whisker - {machine1} vs. {machine2} {transfer_size} Transfers.html')
        fig.show()