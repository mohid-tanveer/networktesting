import os
import sys
import socket
from secret import sp2, sp3, locations

host_name = socket.gethostname()
location = locations[host_name]

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# local script path (./singlethreaded.py and ,/multithreaded.py)
SCRIPT_PATH = sp2
SCRIPT_PATH2 = sp3

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")
    os.system(rf'python3 ..\scatterplotcreation\src\scatterplot.py ..\results\"{host_name} ({location}) multithreaded.csv"')

# check and run loop
while True:
    try:
        # alternate between protocol nodes
        for pn in pn_choices:
            arg = pn
            print(f"Running single threaded script")
            os.system(f"python {SCRIPT_PATH2} {arg}")
            print(f"Running multi threaded script")
            os.system(f"python {SCRIPT_PATH} {arg}")
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
