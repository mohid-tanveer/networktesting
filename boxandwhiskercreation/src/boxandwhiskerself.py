import plotly.graph_objects as go # type: ignore
from plotly.subplots import make_subplots # type: ignore
import pandas as pd
import os
import sys
from dataformatting import csv_to_dict_box_self
from scipy.stats import ttest_ind # type: ignore
import numpy as np

# Define transfer size colors
transfer_size_colors = {
    '10 GB': 'crimson', '10 MB': 'crimson'
}


path = "../output/"

# get file paths from command line arguments and read data from the csv files
file_path = sys.argv[1]
machine = sys.argv[2]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
data = csv_to_dict_box_self(file_path, machine) 

# iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)

    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    if df[(df['type'] == '10 GB')].empty or df[(df['type'] == '10 MB')].empty:
        continue
    fig = make_subplots(rows=1, cols=1)

    # iterate over transfer sizes to prepare data for box plots
    for transfer_size in ['10 GB', '10 MB']:
        group = df[(df['type'] == transfer_size)]
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
                             showlegend=True
                             ))

        # create box plots
        fig.update_layout(title_text=f'Box and Whisker Plot for {day_text} - {machine}',
                      yaxis_title='Transfer Speed (MB/s)',
                      margin=dict(b=170))
        
        gb_data = df[(df['type'] == '10 GB')]['transferspeed_MB/s']
        mb_data = df[(df['type'] == '10 MB')]['transferspeed_MB/s']
        t_stat, p_value = ttest_ind(gb_data, mb_data)

        # display the t-test results
        t_test_text = f"T-test results:<br>T-statistic: {t_stat:.2f}<br>P-value: {p_value:.2e}"
        if p_value < 0.05:
            t_test_text += "<br>Difference is statistically significant"
        else:
            t_test_text += "<br>No significant difference"
        fig.add_annotation(text=t_test_text, xref="paper", yref="paper",
                        x=0.5, y=-0.34, showarrow=False, align="center", font=dict(size=10))
        
        fig.write_html(f'{path}Box and Whisker - {day_text} {machine} Transfers.html')
        fig.show()