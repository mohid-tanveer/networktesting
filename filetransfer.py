import os
import time
import csv

def read_files_from_directory(directory, individual_read_times=None):
    start_time = time.time()
    
    for root, dirs, files in os.walk(directory):
        # iterate over all files in the directory
        for file in files:
            # get individual file path and read the file
            file_path = os.path.join(root, file)
            temp_start_time = time.time()
            with open(file_path, 'r') as f:
                content = f.read()
            temp_end_time = time.time()
            # if individual_read_times is not None, store the read time
            # for the file
            temp_elapsed_time = temp_end_time - temp_start_time
            if individual_read_times is not None:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                individual_read_times.append(temp_elapsed_time, current_time)
    
    end_time = time.time()

    elapsed_time = end_time - start_time
    return elapsed_time, individual_read_times

# directory to 10 gb file
directory_path = r'\\remote_server\shared_folder'
teng_read_times = []
# do 3 tests on the read times for the 10 gb file
for i in range(1, 4):
    time_taken, _ = read_files_from_directory(directory_path, None)
    print(f"Total time taken for 10 gig test {i}: {time_taken} seconds")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    teng_read_times.append((time_taken, current_time))

# directory to 10 mb files
directory_path = r'\\remote_server\shared_folder'
tenm_read_times = []
individual_read_times = []
# do 3 tests on the read times for the 10 mb files
# also store the individual read times for each file on each test
for i in range(1, 4):
    time_taken, individual_read_times = read_files_from_directory(directory_path, individual_read_times)
    print(f"Total time taken for 10 meg test {i}: {time_taken} seconds")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    tenm_read_times.append((time_taken, current_time))

# append the ten gig read times, ten meg read times, and individual read times
# to csv files
