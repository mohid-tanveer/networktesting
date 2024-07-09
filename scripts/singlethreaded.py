import sys
import os
import time
import csv
import socket
from secret import pnpaths, locations

# Get the host name and location of the machine
host_name = socket.gethostname()
location = locations[host_name]

# get current protocol node from command line argument
curr_pn = sys.argv[1]
# remote path to the folder with the files to be read
remote_path = pnpaths[int(curr_pn[-1]) - 1]

def read_files_from_directory_single(directory):
    elapsed_time = 0
    
    for root, dirs, files in os.walk(directory):
        # iterate over all files in the directory
        # in the case of one file, will only be one iteration
        for file in files:
            # get individual file path and read the file
            file_path = os.path.join(root, file)
            temp_start_time = time.time()
            with open(file_path, 'r') as file:
                content = file.read()
            temp_end_time = time.time()
            temp_elapsed_time = temp_end_time - temp_start_time
            # add the elapsed time to the total elapsed time
            elapsed_time += temp_elapsed_time
    
    # calculate the transfer speed in MB/s
    transfer_speed = (10737418240 / elapsed_time) / 1000000

    return elapsed_time, transfer_speed

def networktesting_single(directory_path):
    # init the list to store the read times tuples
    single_read_times = []
    # get the folder name
    folder_name =  os.path.basename(directory_path)
    # read files from directory and get the time taken, file size and transfer speed
    # single-threaded
    time_taken, transfer_speed = read_files_from_directory_single(directory_path)
    print(f"Total time taken for single-threaded {folder_name} test: {time_taken} seconds")
    t = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", t)
    # append the tuple to the read times list
    single_read_times.append((current_time, transfer_speed, curr_pn, 'single'))
    # check if a results file exists
    exists = True if os.path.exists(rf'{remote_path}\results\{host_name} ({location}) multithreaded.csv') else False
    # if result file doesn't exist, create it and write the headers
    if not exists:
        with open(rf'{remote_path}\results\{host_name} ({location}) multithreaded.csv', mode='w') as file:
            writer = csv.writer(file)
            # if the file did not exist, write the headers
            if not exists: 
                writer.writerow(['timestamp', 'transferspeed', 'protocolnode', 'threadtype'])
    # write the results to a csv file
    with open(rf'{remote_path}\results\{host_name} ({location}) multithreaded.csv', mode='a') as file:
        writer = csv.writer(file)
        for row in single_read_times:
            writer.writerow(row)

def main():
    print(f"Testing {curr_pn}")
    # test the network transfer speed of the specified directory/directories
    print("testing s-t tenmegfiles")
    networktesting_single(rf'{remote_path}\tenmegfiles')
    
main()