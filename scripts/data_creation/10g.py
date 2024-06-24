import os
import random
import string

# Define the file size in bytes
file_size = 10 * 1024 * 1024 * 1024  # 10GB

# Define and create (if doesn't exist) the directory to store the output files
output_dir = "tengigfile"
os.makedirs(output_dir, exist_ok=True)

# Define the path to the output file
output_file = os.path.join(output_dir, f"tengig.txt")

# Define the chunk size (1MB)
chunk_size = 1024 * 1024

# Calculate the number of chunks
num_chunks = file_size // chunk_size

# Open the output file
with open(output_file, 'a') as file:
    # Generate and write the data in chunks
    for i in range(num_chunks):
        # Generate random data
        data = ''.join(random.choices(string.ascii_letters + string.digits, k=chunk_size))
        # Write the data to the output file
        file.write(data)
        # Print an update
        print(f"Written chunk {i + 1} / {num_chunks}")

print(f"file '{output_file}' generated successfully!")