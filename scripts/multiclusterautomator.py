import os
import socket
from secret import sp4, sp5

round_complete = False

# local script path (./multithreadedclusterIB.py)
SCRIPT_PATH = sp4
SCRIPT_PATH2 = sp5

# check and run loop
while True:
    print(f"Running single threaded script")
    os.system(f"python {SCRIPT_PATH2}")
    print(f"Running multi threaded script")
    os.system(f"python {SCRIPT_PATH}")
