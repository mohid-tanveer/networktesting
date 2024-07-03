import os
import socket
from secret import sp2, sp3

round_complete = False

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# local script path (./multithreaded.py)
SCRIPT_PATH = sp2
SCRIPT_PATH2 = sp3

# check and run loop
while True:
    # alternate between protocol nodes
    for pn in pn_choices:
        print(f"Running single threaded script")
        arg = pn
        os.system(f"python {SCRIPT_PATH2} {arg}")
        print(f"Running multi threaded script")
        os.system(f"python {SCRIPT_PATH} {arg}")
