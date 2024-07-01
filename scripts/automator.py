import os
import time
import socket

round_complete = False

# get the host name
host_name = socket.gethostname()

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# control file path
CONTROL_FILE = rf"\\jude.stjude.org\informationservices\RI\HPRC\mtanveer\networktesting\scripts\control.txt"

# local script path
SCRIPT_PATH = rf"C:\Users\mtanveer\Downloads\networktesting\scripts\filetransfer.py"

# check if it's this machine's turn to run the script
def check_turn():
    with open(CONTROL_FILE, "r") as file:
        current_control = file.read().strip()
    return current_control == host_name

# Function to update control file to switch to the other machine
def switch_turn():
    next_machine = "D242016" if host_name == "D241962" else "D241962"
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
