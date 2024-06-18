import os
import random
import string

# Define the file size in bytes
file_size = 10 * 1024 * 1024  # 10MB

for i in range(0, 10000):
    # Define the path to the output file
    output_file = f"tenmeg-{i}.txt"

    # Generate random data
    data = ''.join(random.choices(string.ascii_letters + string.digits, k=file_size))

    # Write the data to the output file
    with open(output_file, 'w') as file:
        file.write(data)

    print(f"file '{output_file}' generated successfully!")