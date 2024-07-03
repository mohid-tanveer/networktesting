import pandas as pd

def partition_data(data, multi=False):
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
    
    # format the partitioned data
    for i in range(len(partitioned_data)):
        if not multi:
            formatted_data = {
                'timestamp': [d['timestamp'] for d in partitioned_data[i]],
                'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
                'protocolnode': [d['protocolnode'] for d in partitioned_data[i]],
                'type': [d['type'] for d in partitioned_data[i]]
            }
        else:
            formatted_data = {
                'timestamp': [d['timestamp'] for d in partitioned_data[i]],
                'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
                'protocolnode': [d['protocolnode'] for d in partitioned_data[i]],
                'threadtype': [d['threadtype'] for d in partitioned_data[i]]
            }
        partitioned_data[i] = formatted_data
        
    return partitioned_data

def cluster_partition_data(data, multi=False):
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
    
    # format the partitioned data
    for i in range(len(partitioned_data)):
        if not multi:
            formatted_data = {
                'timestamp': [d['timestamp'] for d in partitioned_data[i]],
                'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
                'type': [d['type'] for d in partitioned_data[i]]
            }
        else:
            formatted_data = {
                'timestamp': [d['timestamp'] for d in partitioned_data[i]],
                'transferspeed_MB/s': [round(d['transferspeed (MB/s)'], 10) for d in partitioned_data[i]],
                'threadtype': [d['threadtype'] for d in partitioned_data[i]]
            }
        partitioned_data[i] = formatted_data
        
    return partitioned_data

def csv_to_dict(file_path):
    # read csv file into a dataframe
    df = pd.read_csv(file_path)
    # convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    # init data list
    data = []
    # divide the data into groups of 3 averaging the timestamp and transferspeed
    # represents one run of the networktesting function
    for i in range(0, len(data_dict), 3):
        # average the timestamp and transferspeed
        timestamp = pd.to_datetime([d['timestamp'] for d in data_dict[i:i+3]]).mean()
        transferspeed = sum(d['transferspeed'] for d in data_dict[i:i+3]) / 3
        protocolnode = data_dict[i]['protocolnode']
        type = data_dict[i]['type']
        data.append({'timestamp': timestamp.strftime('%-m/%-d/%y %-I:%M %p'), 'transferspeed (MB/s)': transferspeed,
                     'protocolnode': protocolnode, 'type': type})
        return partition_data(data)

def multi_csv_to_dict(file_path):
    # read csv file into a dataframe
    df = pd.read_csv(file_path)
    # convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    # init data list
    data = []
    # divide the data into groups of 3 averaging the timestamp and transferspeed
    # represents one run of the networktesting function
    for d in data_dict:
        # average the timestamp and transferspeed
        timestamp = pd.to_datetime(d['timestamp'])
        transferspeed = d['transferspeed']
        threadtype = d['threadtype']
        data.append({'timestamp': timestamp.strftime('%-m/%-d/%y %-I:%M %p'), 'transferspeed (MB/s)': transferspeed,
                     'threadtype': threadtype})
    return partition_data(data, True)

def csv_to_dict_cluster(file_path):
    # read csv file into a dataframe
    df = pd.read_csv(file_path)
    # convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    # init data list
    data = []
    # divide the data into groups of 3 averaging the timestamp and transferspeed
    # represents one run of the networktesting function
    for i in range(0, len(data_dict), 3):
        # average the timestamp and transferspeed
        timestamp = pd.to_datetime([d['timestamp'] for d in data_dict[i:i+3]]).mean()
        transferspeed = sum(d['transferspeed'] for d in data_dict[i:i+3]) / 3
        type = data_dict[i]['type']
        data.append({'timestamp': timestamp.strftime('%-m/%-d/%y %-I:%M %p'), 'transferspeed (MB/s)': transferspeed,
                     'type': type})
    return cluster_partition_data(data)

def multi_csv_to_dict_cluster(file_path):
    # read csv file into a dataframe
    df = pd.read_csv(file_path)
    # convert the DataFrame to a dictionary
    data_dict = df.to_dict(orient='records')
    # init data list
    data = []
    # divide the data into groups of 3 averaging the timestamp and transferspeed
    # represents one run of the networktesting function
    for d in data_dict:
        # average the timestamp and transferspeed
        timestamp = pd.to_datetime(d['timestamp'])
        transferspeed = d['transferspeed']
        threadtype = d['threadtype']
        data.append({'timestamp': timestamp.strftime('%-m/%-d/%y %-I:%M %p'), 'transferspeed (MB/s)': transferspeed,
                     'threadtype': threadtype})
    return cluster_partition_data(data, True)