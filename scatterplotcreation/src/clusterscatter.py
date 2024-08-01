import os
import sys
import plotly.graph_objects as go # type: ignore
import pandas as pd
import numpy as np
from dataformatting import csv_to_dict_cluster, multi_csv_to_dict_cluster
from ssecret import remotepath

# get file path from command line argument and splice the machine name
file_path = sys.argv[1]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
non_multi = True if 'multithreaded' not in file_path else False
data = csv_to_dict_cluster(file_path) if non_multi else multi_csv_to_dict_cluster(file_path)

# iterate over each day's data
for day in data:
    # format the data into a DataFrame
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    df = pd.DataFrame(day)
    # get the day in plain text
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    if day['timestamp'][0].date() != pd.Timestamp.now().date():
        if os.path.exists(rf'../output/Scatterplot - Cluster {day_text} Transfers.html') and non_multi:
            continue
        elif os.path.exists(rf'../output/Scatterplot - Cluster Multithreaded {day_text} Transfers.html') and not non_multi:
            continue

    ten_GB_data = df[df['type'] == '10 GB']
    ten_MB_data = df[df['type'] == '10 MB']
    mean_gb = np.mean(ten_GB_data['transferspeed_MB/s'])
    std_dev_gb = np.std(ten_GB_data['transferspeed_MB/s'])
    mean_mb = np.mean(ten_MB_data['transferspeed_MB/s'])
    std_dev_mb = np.std(ten_MB_data['transferspeed_MB/s'])

    ### plotting
    fig = go.Figure()
    z_scores_gb = [(x - mean_gb) / std_dev_gb for x in ten_GB_data['transferspeed_MB/s']]
    z_scores_mb = [(x - mean_mb) / std_dev_mb for x in ten_MB_data['transferspeed_MB/s']]
    fig.add_trace(go.Scatter(x=ten_GB_data['timestamp'], 
                        y=ten_GB_data['transferspeed_MB/s'], 
                        mode='markers', 
                        marker=dict(color="red"), 
                        name=f"10GB",
                        hoverinfo='x+y+text',
                        hovertext=[f"10GB, Z-score: {z:.2f}" for z in z_scores_gb]))
    fig.add_trace(go.Scatter(x=ten_MB_data['timestamp'], 
                        y=ten_MB_data['transferspeed_MB/s'], 
                        mode='markers', 
                        marker=dict(color="blue", symbol='diamond'), 
                        name=f"10MB",
                        hoverinfo='x+y+text',
                        hovertext=[f"10MB, Z-score: {z:.2f}" for z in z_scores_mb]))
    
    fig.update_layout(title=f'Scatterplot - Cluster {"Multithreaded" if not non_multi else ""} {day_text} Transfers',
                        xaxis_title='Timestamp',
                        xaxis=dict(
                            tickmode='auto',
                            tickformat='%m-%d %I:%M %p',
                            rangeslider=dict(visible=True)
                        ),
                        yaxis_title='Transfer Speed (MB/s)',
                        legend_title='Transfer Size',
                        legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=1),
                        margin=dict(b=150))
    
    # add std dev and variance for all data
    variance_gb = np.var(ten_GB_data['transferspeed_MB/s'])
    variance_mb = np.var(ten_MB_data['transferspeed_MB/s'])
    stat_text = f"10 GB Data<br>Std Dev: {std_dev_gb:.2f}<br>Variance: {variance_gb:.2f}"
    stat_text += f"<br><br>10 MB Data<br>Std Dev: {std_dev_mb:.2f}<br>Variance: {variance_mb:.2f}"

    fig.add_annotation(text=stat_text, xref="paper", yref="paper",
                    x=.5, y=-0.625, showarrow=False, align="left",
                    bordercolor="Black", borderwidth=1)

    # save plot as PDF
    if non_multi:
        fig.write_html(rf'../output/Scatterplot - Cluster {day_text} Transfers.html')
    else:
        fig.write_html(rf'../output/Scatterplot - Cluster Multithreaded {day_text} Transfers.html')
    
    # display interactive plot
    fig.show()