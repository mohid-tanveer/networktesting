import os
import sys
import atexit
import signal
import time
import socket
from secret import cf, sp, turn_order

round_complete = False

# get the host name
host_name = socket.gethostname()

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# control file path (./control.txt)
CONTROL_FILE = cf

# local script path (./filetransfer.py)
SCRIPT_PATH = sp

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

# check if it's this machine's turn to run the script
def check_turn():
    with open(CONTROL_FILE, "r") as file:
        current_control = file.read().strip()
    return current_control == host_name

# Function to update control file to switch to the other machine
def switch_turn():
    next_machine = turn_order[(turn_order.index(host_name) + 1) % len(turn_order)]
    with open(CONTROL_FILE, "w") as f:
        f.write(next_machine)

# check and run loop
while True:
    # alternate between protocol nodes
    for pn in pn_choices:
        # reset round complete
        round_complete = False
        while not round_complete:
            # check if local machine's turn
            if check_turn():
                print(f"Running script")
                arg = pn
                os.system(f"python {SCRIPT_PATH} {arg}")
                switch_turn()
                # indicate that round is complete
                round_complete = True
            else:
                # if not wait before checking again
                print(f"Waiting for turn on protocol node {pn}...")
                time.sleep(10)
