import os
import time
import csv
import socket

# Get the host name
host_name = socket.gethostname()

# remote path to the folder with the files to be read
remote_path = '\\jude.stjude.org\ResearchHome\Departments\InformationServices\RI\HPRC\mtanveer\network_testing'

def read_files_from_directory(directory, individual_read_times):
    elapsed_time = 0
    file_total_size = 0
    
    for root, dirs, files in os.walk(directory):
        # iterate over all files in the directory
        # in the case of one file, will only be one iteration
        for file in files:
            # get individual file path and read the file
            file_path = os.path.join(root, file)
            # get file size and add to total file size
            file_size = os.path.getsize(file_path)
            file_total_size += file_size
            temp_start_time = time.time()
            with open(file_path, 'r') as file:
                content = file.read()
            temp_end_time = time.time()
            temp_elapsed_time = temp_end_time - temp_start_time
            # add the elapsed time to the total elapsed time
            elapsed_time += temp_elapsed_time
            # if tracking individual file reads (10 mb files) append data to its list
            if individual_read_times is not None:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                individual_read_times.append(temp_elapsed_time, current_time, file_size)
    
    # calculate the transfer speed
    transfer_speed = file_total_size / elapsed_time

    return elapsed_time, file_total_size, transfer_speed, individual_read_times

def networktesting(directory_path, store_individual_read_times=False):
    # init the list to store the read times tuples
    read_times = []
    # if storing individual read times, init the list
    individual_read_times = [] if store_individual_read_times else None
    # get the folder name
    folder_name =  os.path.basename(directory_path)
    # iterate over the directory 3 times
    for i in range(1, 4):
        # read files from directory and get the time taken, file size and transfer speed
        time_taken, file_size, transfer_speed, individual_read_times = read_files_from_directory(directory_path, individual_read_times)
        print(f"Total time taken for {folder_name} test {i}: {time_taken} seconds")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        # append the tuple to the read times list
        read_times.append((time_taken, current_time, file_size, transfer_speed))
    # check if a results file exists
    exists = True if os.path.exists(f'{remote_path}\results\{host_name}_{folder_name}.csv') else False
    # write the results to a csv file
    with open(f'{remote_path}\results\{host_name}_{folder_name}.csv', mode='a') as file:
        writer = csv.writer(file)
        # if the file does not exist, write the headers
        if not exists: 
            writer.writerow(['time', 'timestamp', 'filesize', 'transferspeed'])
        for row in read_times:
            writer.writerow(row)
    # if storing individual read times, write the results to a csv file
    if store_individual_read_times:
        exists = True if os.path.exists(f'{remote_path}\results\{host_name}_{folder_name}_individual.csv') else False
        with open(f'{remote_path}\results\{host_name}_{folder_name}_individual.csv', mode='a') as file:
            writer = csv.writer(file)
            # if the file does not exist, write the headers
            if not exists: 
                writer.writerow(['time', 'timestamp', 'filesize'])
            for row in individual_read_times:
                writer.writerow(row)

def main():
    # test the network transfer speed of the specified directory/directories
    networktesting('{remote_path}\tengigfile')
    networktesting('{remote_path}\tenmegfiles', True)