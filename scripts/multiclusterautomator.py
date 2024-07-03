import os
import sys
import atexit
import signal
import socket
from secret import sp4, sp5

round_complete = False

# local script path (./multithreadedclusterIB.py)
SCRIPT_PATH = sp4
SCRIPT_PATH2 = sp5

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")

# register on_exit function to run on exit
atexit.register(on_exit)

def signal_handler(signum, frame):
    on_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# check and run loop
while True:
    print(f"Running single threaded script")
    os.system(f"python {SCRIPT_PATH2}")
    print(f"Running multi threaded script")
    os.system(f"python {SCRIPT_PATH}")
