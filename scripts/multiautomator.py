import os
import sys
import atexit
import signal
import socket
from secret import sp2, sp3, locations
import subprocess

host = socket.gethostname()
location = locations[host]

round_complete = False

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# local script path (./multithreaded.py)
SCRIPT_PATH = sp2
SCRIPT_PATH2 = sp3

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")
    subprocess.run([rf"python3 ..\scatterplotcreation\src\scatterplot.py ..\results\{host}\ ({location})\ multithreaded.csv"], shell=True)

# register on_exit function to run on exit
atexit.register(on_exit)

def signal_handler(signum, frame):
    on_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# check and run loop
while True:
    # alternate between protocol nodes
    for pn in pn_choices:
        print(f"Running single threaded script")
        arg = pn
        os.system(f"python {SCRIPT_PATH2} {arg}")
        print(f"Running multi threaded script")
        os.system(f"python {SCRIPT_PATH} {arg}")
