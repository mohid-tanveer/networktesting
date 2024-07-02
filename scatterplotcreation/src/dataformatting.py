import pandas as pd

def excel_to_dict(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    data = []
    # Divide the data into groups of 3 averaging the timestamp and transferspeed
    for i in range(0, len(data_dict), 3):
        # Ensure all timestamps are converted to datetime objects before averaging
        timestamp = pd.to_datetime([d['timestamp'] for d in data_dict[i:i+3]]).mean()
        transferspeed = sum(d['transferspeed'] for d in data_dict[i:i+3]) / 3
        protocolnode = data_dict[i]['protocolnode']
        Type = data_dict[i]['Type']
        # Convert timestamp to the desired format right away
        data.append({'timestamp': timestamp.strftime('%-m/%-d/%y %-I:%M %p'), 'transferspeed (MB/s)': transferspeed,
                     'protocolnode': protocolnode, 'Type': Type})
    
    # partition data by days
    data.sort(key=lambda x: x['timestamp'])
    partitioned_data = []
    current_day = data[0]['timestamp'].split()[0]
    current_partition = []
    for d in data:
        if d['timestamp'].split()[0] == current_day:
            current_partition.append(d)
        else:
            partitioned_data.append(current_partition)
            current_partition = [d]
            current_day = d['timestamp'].split()[0]
    if current_partition:
        partitioned_data.append(current_partition)
    
    for i in range(len(partitioned_data)):
        formatted_data = {
            'timestamp': [d['timestamp'] for d in partitioned_data[i]],
            'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
            'protocolnode': [d['protocolnode'] for d in partitioned_data[i]],
            'Type': [d['Type'] for d in partitioned_data[i]]
        }
        partitioned_data[i] = formatted_data
    return partitioned_data

