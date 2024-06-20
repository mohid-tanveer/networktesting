import os
import time

def read_files_from_directory(directory):
    start_time = time.time()
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                # Do something with the file content
                content = f.read()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Total time taken: {elapsed_time} seconds")

directory_path = r'\\remote_server\shared_folder'
read_files_from_directory(directory_path)