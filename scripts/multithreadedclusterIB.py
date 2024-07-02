import os
import time
import csv
from concurrent.futures import ThreadPoolExecutor

def read_single_file(file_path):
    print(f"Reading file: {file_path}")
    with open(file_path, 'r') as file:
        content = file.read()
    return 

def read_files_from_directory_multi(directory):
    elapsed_time = 0
    file_total_size = 10737418240
    tasks = []
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        for root, dirs, files in os.walk(directory):
            # iterate over all files in the directory
            # in the case of one file, will only be one iteration
            for file in files:
                # get individual file path and submit a task to read the file
                file_path = os.path.join(root, file)
                tasks.append(executor.submit(read_single_file, file_path))
    end_time = time.time()
    elapsed_time = end_time - start_time
    # calculate the transfer speed
    transfer_speed = file_total_size / elapsed_time

    return elapsed_time, file_total_size, transfer_speed

def networktesting(directory_path):
    # init the list to store the read times tuples
    read_times = []
    # get the folder name
    folder_name =  os.path.basename(directory_path)
    # iterate over the directory 3 times
    for i in range(1, 4):
        # read files from directory and get the time taken, file size and transfer speed
        time_taken, file_size, transfer_speed = read_files_from_directory_multi(directory_path)
        print(f"Total time taken for {folder_name} test {i}: {time_taken} seconds")
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        # append the tuple to the read times list
        read_times.append((time_taken, current_time, file_size, transfer_speed))
    # check if a results file exists
    exists = True if os.path.exists(rf'../results/clusterIB_{folder_name}_multi.csv') else False
    # if result file doesn't exist, create it and write the headers
    if not exists:
        with open(rf'../results/clusterIB_{folder_name}_multi.csv', mode='w') as file:
            writer = csv.writer(file)
            # if the file did not exist, write the headers
            if not exists: 
                writer.writerow(['time', 'timestamp', 'filesize', 'transferspeed'])
    # write the results to a csv file
    with open(rf'../results/clusterIB_{folder_name}_multi.csv', mode='a') as file:
        writer = csv.writer(file)
        for row in read_times:
            writer.writerow(row)

def main():
    # test the network transfer speed of the specified directory/directories
    print("testing tenmegfiles")
    networktesting(rf'../tenmegfiles')
    
main()