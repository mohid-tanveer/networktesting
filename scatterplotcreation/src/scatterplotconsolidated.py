import os
import sys
import plotly.graph_objects as go # type: ignore
import numpy as np
import pandas as pd
from dataformatting import csv_to_dict_total, multi_csv_to_dict
from ssecret import remotepath

# define protocol node colors
protocol_colors = {
    'pn001': 'red', 'pn002': 'blue', 'pn003': 'green',
    'pn004': 'purple', 'pn005': 'orange', 'pn006': 'brown'
}

# get file path from command line argument and splice the machine name
file_path = sys.argv[1]
path = '../output/'
machine = sys.argv[2]
# read data from the csv file and convert it to a dictionary
# format: 
# {timestamp: [timestamp values], 
# type: [type values] or threadtype: [threadtype values],
# transferspeed_MB/s: [transferspeed_MB/s values], 
# protocolnode: [protocolnode values]}
non_multi = True if 'multithreaded' not in file_path else False
data = csv_to_dict_total(file_path) if non_multi else multi_csv_to_dict(file_path)
total = data[0]
total['timestamp'] = pd.to_datetime(total['timestamp'], format='%m/%d/%y %I:%M:%S %p')
df = pd.DataFrame(total)
df['date'] = df['timestamp'].dt.date
unique_days = df['date'].unique()
buttons = []
for day in unique_days:
    start_time = f"{day} 08:00:00"
    end_time = f"{day} 18:00:00"
    buttons.append(dict(
        method='relayout',
        label=str(day),
        args=[{'xaxis.range': [start_time, end_time]}]
    ))
buttons.append(dict(
    method='relayout',
    label='Show All',
    args=[{'xaxis.range': [min(df['timestamp']).strftime('%Y-%m-%d %H:%M:%S'), 
                           max(df['timestamp']).strftime('%Y-%m-%d %H:%M:%S')]}]
))
# iterate over each day's data
# format the data into a DataFrame
ten_GB_data = df[df['type'] == '10 GB']
ten_MB_data = df[df['type'] == '10 MB']
mean_gb = np.mean(ten_GB_data['transferspeed_MB/s'])
std_dev_gb = np.std(ten_GB_data['transferspeed_MB/s'])
mean_mb = np.mean(ten_MB_data['transferspeed_MB/s'])
std_dev_mb = np.std(ten_MB_data['transferspeed_MB/s'])
fig = go.Figure()
for protocol, color in protocol_colors.items():
    protocol_data_gb = df[(df['protocolnode'] == protocol) & (df['type'] == '10 GB')]
    protocol_data_mb = df[(df['protocolnode'] == protocol) & (df['type'] == '10 MB')]
    z_scores_gb = [(x - mean_gb) / std_dev_gb for x in protocol_data_gb['transferspeed_MB/s']]
    z_scores_mb = [(x - mean_mb) / std_dev_mb for x in protocol_data_mb['transferspeed_MB/s']]
    fig.add_trace(go.Scatter(x=protocol_data_gb['timestamp'], 
                            y=protocol_data_gb['transferspeed_MB/s'], 
                            mode='markers', 
                            marker=dict(color=color), 
                            name=f"{protocol} 10GB",
                            hoverinfo='x+y+text',
                            hovertext=[f"{protocol} 10GB, Z-score: {z:.2f}" for z in z_scores_gb]))
    fig.add_trace(go.Scatter(x=protocol_data_mb['timestamp'], 
                            y=protocol_data_mb['transferspeed_MB/s'], 
                            mode='markers', 
                            marker=dict(color=color, symbol='diamond'), 
                            name=f"{protocol} 10MB",
                            hoverinfo='x+y+text',
                            hovertext=[f"{protocol} 10MB, Z-score: {z:.2f}" for z in z_scores_mb]))

fig.update_layout(title=f'Scatterplot - {machine} {"Multithreaded" if not non_multi else ""} Transfers',
                    xaxis_title='Timestamp',
                    xaxis=dict(
                        tickmode='auto',
                        tickformat='%m-%d %I:%M:%S %p',
                        rangeslider=dict(visible=True)
                    ),
                    yaxis_title='Transfer Speed (MB/s)',
                    legend_title='Protocol Nodes',
                    legend=dict(x=1.05, y=1, bordercolor="Black", borderwidth=1),
                    margin=dict(b=150),
                    updatemenus=[dict(
                        type="buttons",
                        direction="right",
                        buttons=buttons,
                        pad={"r": 10, "t": 10},
                        showactive=True,
                        x=0.1,
                        xanchor="left",
                        y=1.1,
                        yanchor="top"
                    )])

stats_text = ""
for protocol, color in protocol_colors.items():
    protocol_data = df[df['protocolnode'] == protocol]['transferspeed_MB/s']
    if not protocol_data.empty:
        std_dev_protocol = np.std(protocol_data)
        variance = np.var(protocol_data)
        stats_text += f"{protocol}<br>Std Dev: {std_dev_protocol:.2f}<br>Variance: {variance:.2f}<br><br>"
# add std dev and variance for all data
variance_gb = np.var(ten_GB_data['transferspeed_MB/s'])
variance_mb = np.var(ten_MB_data['transferspeed_MB/s'])
stat_text = f"10 GB Data<br>Std Dev: {std_dev_gb:.2f}<br>Variance: {variance_gb:.2f}"
stat_text += f"<br><br>10 MB Data<br>Std Dev: {std_dev_mb:.2f}<br>Variance: {variance_mb:.2f}"

fig.add_annotation(text=stats_text, xref="paper", yref="paper",
                x=1.15, y=-0.6, showarrow=False, align="left",
                bordercolor="Black", borderwidth=1)
fig.add_annotation(text=stat_text, xref="paper", yref="paper",
                x=.5, y=-0.625, showarrow=False, align="left",
                bordercolor="Black", borderwidth=1)

# save plot as PDF
if non_multi:
    fig.write_html(rf'{path}Scatterplot - {machine} Total Transfers.html')
else:
    fig.write_html(rf'{path}Scatterplot - {machine} Multithreaded Total Transfers.html')

# display interactive plot
fig.show()