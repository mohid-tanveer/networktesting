import sys
import os
import time
import csv
import socket
from secret import pnpaths, locations

# Get the host name and location
host_name = socket.gethostname()
location = locations[host_name]

# get current protocol node from command line argument
curr_pn = sys.argv[1]
# remote path to the folder with the files to be read
remote_path = pnpaths[int(curr_pn[-1]) - 1]

def read_files_from_directory(directory):
    elapsed_time = 0
    
    for root, dirs, files in os.walk(directory):
        # iterate over all files in the directory
        # in the case of one file, will only be one iteration
        for file in files:
            # get individual file path and read the file
            file_path = os.path.join(root, file)
            print(f"Reading file: {file_path}")
            with open(file_path, 'r') as file:
                temp_start_time = time.time()
                content = file.read()
                temp_end_time = time.time()
            temp_elapsed_time = temp_end_time - temp_start_time
            # add the elapsed time to the total elapsed time
            elapsed_time += temp_elapsed_time
    
    # calculate the transfer speed in MB/s
    transfer_speed = (10737418240 / elapsed_time) / 1000000

    return elapsed_time, transfer_speed

def networktesting(directory_path):
    # declare the type of file being read
    type = '10 GB' if 'tengigfile' in directory_path else '10 MB'
    # init the list to store the read times tuples
    read_times = []
    # get the folder name
    folder_name =  os.path.basename(directory_path)
    # iterate over the directory 3 times
    for i in range(1, 4):
        # read files from directory and get the time taken, file size and transfer speed
        time_taken, transfer_speed = read_files_from_directory(directory_path)
        print(f"Total time taken for {folder_name} test {i}: {time_taken} seconds")
        t = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
        # append the tuple to the read times list
        read_times.append((current_time, transfer_speed, curr_pn, type))
    # check if a results file exists
    exists = True if os.path.exists(rf'{remote_path}\results\{host_name} ({location}).csv') else False
    # if result file doesn't exist, create it and write the headers
    if not exists:
        with open(rf'{remote_path}\results\{host_name} ({location}).csv', mode='w') as file:
            writer = csv.writer(file)
            # if the file did not exist, write the headers
            if not exists: 
                writer.writerow(['timestamp', 'transferspeed', 'protocolnode', 'type'])
    # write the results to a csv file
    with open(rf'{remote_path}\results\{host_name} ({location}).csv', mode='a') as file:
        writer = csv.writer(file)
        for row in read_times:
            writer.writerow(row)

def main():
    print(f"Testing {curr_pn}")
    # test the network transfer speed of the specified directory/directories
    print("testing tengigfile")
    networktesting(rf'{remote_path}\tengigfile')
    print("testing tenmegfiles")
    networktesting(rf'{remote_path}\tenmegfiles')

main()