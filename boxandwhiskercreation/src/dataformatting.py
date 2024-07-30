import pandas as pd

def partition_data_box(data, total):
    data.sort(key=lambda x: x['timestamp'])
    partitioned_data = []
    if total:
        # skip partitioning and directly format the entire dataset
        formatted_data = {
            'timestamp': [d['timestamp'] for d in data],
            'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in data],
            'protocolnode': [d['protocolnode'] for d in data],
            'type': [d['type'] for d in data],
            'machine': [d['machine'] for d in data]
        }
        partitioned_data.append(formatted_data)
        return partitioned_data
    # else partition data by days
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
    
    # format the partitioned data
    for i in range(len(partitioned_data)):
        formatted_data = {
            'timestamp': [d['timestamp'] for d in partitioned_data[i]],
            'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
            'protocolnode': [d['protocolnode'] for d in partitioned_data[i]],
            'type': [d['type'] for d in partitioned_data[i]],
            'machine': [d['machine'] for d in partitioned_data[i]]
        }
        partitioned_data[i] = formatted_data
        
    return partitioned_data

def csv_to_dict_box(file_path, file_path2, machine1, machine2, total=False):
    # read both csv files into dataframes
    df1 = pd.read_csv(file_path)
    df2 = pd.read_csv(file_path2)
    # convert the DataFrames to dictionaries
    data_dict1 = df1.to_dict(orient='records')
    data_dict2 = df2.to_dict(orient='records')
    # init singular data list
    data = []
    for d in data_dict1:
        timestamp = pd.to_datetime(d['timestamp'])
        transferspeed = d['transferspeed']
        protocolnode = d['protocolnode']
        type = d['type']
        formatted_timestamp = timestamp.strftime('%m/%d/%y %I:%M %p')
        formatted_timestamp = formatted_timestamp.replace('/0', '/').replace(' 0', ' ')
        data.append({'timestamp': formatted_timestamp, 'transferspeed (MB/s)': transferspeed,
                     'protocolnode': protocolnode, 'type': type, 'machine': machine1})
    for d in data_dict2:
        timestamp = pd.to_datetime(d['timestamp'])
        transferspeed = d['transferspeed']
        protocolnode = d['protocolnode']
        type = d['type']
        formatted_timestamp = timestamp.strftime('%m/%d/%y %I:%M %p')
        formatted_timestamp = formatted_timestamp.replace('/0', '/').replace(' 0', ' ')
        data.append({'timestamp': formatted_timestamp, 'transferspeed (MB/s)': transferspeed,
                     'protocolnode': protocolnode, 'type': type, 'machine': machine2})
    return partition_data_box(data, total)