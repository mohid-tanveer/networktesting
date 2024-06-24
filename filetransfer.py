import os
import time
import csv

def read_files_from_directory(directory, individual_read_times=None):
    elapsed_time = 0
    file_total_size = 0
    
    for root, dirs, files in os.walk(directory):
        # iterate over all files in the directory
        # in the case of the one 10 gb file, will only be one iteration
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
            # if individual_read_times is not None, store the read time
            # for the file
            temp_elapsed_time = temp_end_time - temp_start_time
            # add the elapsed time to the total elapsed time
            elapsed_time += temp_elapsed_time
            individual_transfer_speed = file_size / temp_elapsed_time
            # if tracking individual file reads (10 mb files) append data to its list
            if individual_read_times is not None:
                t = time.localtime()
                current_time = time.strftime("%H:%M:%S", t)
                individual_read_times.append(temp_elapsed_time, current_time, file_size, individual_transfer_speed)
    
    # calculate the transfer speed
    transfer_speed = file_total_size / elapsed_time

    return elapsed_time, individual_read_times, file_total_size, transfer_speed

# directory to 10 gb file
directory_path = r'\\remote_server\shared_folder' # temp path for now
# do 3 tests on the read times for the 10 gb file and store results
teng_read_times = []
for i in range(1, 4):
    time_taken, _, file_size, transfer_speed = read_files_from_directory(directory_path)
    print(f"Total time taken for 10 gig test {i}: {time_taken} seconds")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    teng_read_times.append((time_taken, current_time, file_size, transfer_speed))

# directory to 10 mb files
directory_path = r'\\remote_server\shared_folder'
# do 3 tests on the read times for the 10 mb files and store results
tenm_read_times = []
# also store the individual read times for each file on each test
individual_read_times = []
for i in range(1, 4):
    time_taken, individual_read_times, file_size, transfer_speed = read_files_from_directory(directory_path, individual_read_times)
    print(f"Total time taken for 10 meg test {i}: {time_taken} seconds")
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    tenm_read_times.append((time_taken, current_time, file_size, transfer_speed))

# append the ten gig read times, ten meg read times, and individual read times
# to csv files

# write to the ten gig read times csv file
with open('teng_read_times.csv', mode='a') as file:
    writer = csv.writer(file)
    for row in teng_read_times:
        writer.writerow(row)

# write to the ten meg read times csv file
with open('tenm_read_times.csv', mode='a') as file:
    writer = csv.writer(file)
    for row in tenm_read_times:
        writer.writerow(row)

# write to the individual read times csv file
with open('individual_read_times.csv', mode='a') as file:
    writer = csv.writer(file)
    for row in individual_read_times:
        writer.writerow(row)

