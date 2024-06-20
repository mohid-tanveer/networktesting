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

# Open the output file
with open(output_file, 'w') as file:
    # Generate random data
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size))
    # Write the data to the output file
    file.write(data)

print(f"file '{output_file}' generated successfully!")