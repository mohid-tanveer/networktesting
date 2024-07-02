import sys
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch
import matplotlib.dates as mdates
from dataformatting import excel_to_dict

# Define colors for each protocol node for consistency
protocol_colors = {
    'pn001': 'red', 'pn002': 'blue', 'pn003': 'green',
    'pn004': 'purple', 'pn005': 'orange', 'pn006': 'brown'
}

file_path = sys.argv[1]
machine = file_path.split(".")[0]
data = excel_to_dict(file_path)
for day in data:
    day['timestamp'] = pd.to_datetime(day['timestamp'], format='%m/%d/%y %I:%M %p')
    day_text = day['timestamp'][0].strftime('%m-%d-%y')
    df = pd.DataFrame(day)

    # Separate data for 10 GB and 10 MB transfers
    gb_data = df[df['Type'] == '10 GB']
    mb_data = df[df['Type'] == '10 MB']

    # Plotting
    # calculate figure width by range of timestamps
    time_range = day['timestamp'].max() - day['timestamp'].min()
    time_range_hours = time_range.total_seconds() / 3600
    # Adjust the figure width based on the time range
    # 10 hour range = 30, 5 hour range = 15, 2 hour range = 6
    fig_width = 10 + time_range_hours * 2
    plt.figure(figsize=(fig_width, 8))  # Adjusted figure size to provide more space

    # Scatter plot for 10 GB transfers
    plt.scatter(gb_data['timestamp'], gb_data['transferspeed_MB/s'], s=100, c=gb_data['protocolnode'].map(protocol_colors), marker='s', label='10 GB')

    # Scatter plot for 10 MB transfers
    plt.scatter(mb_data['timestamp'], mb_data['transferspeed_MB/s'], s=100, c=mb_data['protocolnode'].map(protocol_colors), marker='o', label='10 MB')

    # Adding labels and legend for transfer sizes
    plt.xlabel('Timestamp')
    plt.ylabel('Transfer Speed (MB/s)')
    plt.title(f'{machine} File Transfers on {day_text}')
    size_legend = plt.legend(title="Transfer Size", loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    # Create custom patches for the protocol node legend
    protocol_patches = [Patch(color=color, label=protocol) for protocol, color in protocol_colors.items()]
    # Add the protocol node legend to the plot
    plt.legend(handles=protocol_patches, title="Protocol Nodes", loc='upper right', bbox_to_anchor=(1.15, 0.85), borderaxespad=0.)

    # Add back the size legend
    plt.gca().add_artist(size_legend)

    # Formatting x-axis to show dates with specific format
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # Ensure a half-hour interval

    # Then, you have your plt.xticks(rotation=45) as before
    plt.xticks(rotation=45)

    # Formatting x-axis to show dates
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 0.85, 1])  # Adjust the rect parameter to make space for the legend

    # Before displaying the plot, save it as a PDF
    plt.savefig(f'../output/Scatterplot - {machine} {day_text} Transfers.pdf', format='pdf', bbox_inches='tight')
    # Display the plot
    plt.show()