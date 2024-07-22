import os
import sys
import time
import socket
from secret import cf, sp, turn_order, locations, remotepath
import subprocess

# get the host name and location of the machine
host_name = socket.gethostname()
location = locations[host_name]
round_complete = False

# set up protocol node choices
pn_choices = ['pn001', 'pn002', 'pn003', 'pn004', 'pn005', 'pn006']

# control file path (./control.txt)
CONTROL_FILE = cf

# local script path (./filetransfer.py)
SCRIPT_PATH = sp

# on exit update scatter-plots with any new data
def on_exit():
    # update control.txt to exit
    with open(CONTROL_FILE, "w") as f:
        f.write('KeyboardInterrupt')

    print("Updating relevant scatterplots...")
    # Define the path to the scatterplot creation directory
    scatterplot_creation_dir = r"..\scatterplotcreation"
    
    # Create virtual environment if it doesn't exist
    subprocess.run("pip install virtualenv", shell=True, check=True)
    venv_dir = os.path.join(scatterplot_creation_dir, "venv")
    if not os.path.exists(venv_dir):
        subprocess.run(["virtualenv", venv_dir], check=True)
    
    scatterplot_script = os.path.join(scatterplot_creation_dir, "src", "scatterplot.py")
    results_file = f"{os.path.join(remotepath, 'results', f'{host_name} ({location}).csv')}"
    activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")

    # Activate virtual environment and run the script
    # Install dependencies
    activate_and_run_commands = f"\"{activate_script}\" && pip install -r \"{os.path.join(scatterplot_creation_dir, 'requirements.txt')}\" && python \"{scatterplot_script}\" \"{results_file}\" r {host_name} && deactivate"
    subprocess.run(activate_and_run_commands, shell=True, check=True)

# check if it's this machine's turn to run the script
def check_turn():
    with open(CONTROL_FILE, "r") as file:
        current_control = file.read().strip()
    if current_control == 'KeyboardInterrupt':
        raise KeyboardInterrupt
    return current_control == host_name

# Function to update control file to switch to the other machine
def switch_turn():
    next_machine = turn_order[(turn_order.index(host_name) + 1) % len(turn_order)]
    with open(CONTROL_FILE, "w") as f:
        f.write(next_machine)

# check and run loop
while True:
    try:
        # alternate between protocol nodes
        for pn in pn_choices:
            # reset round complete
            round_complete = False
            while not round_complete:
                # check if local machine's turn
                if check_turn():
                    print(f"Running script")
                    arg = pn
                    subprocess.run(f"python {SCRIPT_PATH} {arg}", shell=True, check=True)
                    switch_turn()
                    # indicate that round is complete
                    round_complete = True
                else:
                    # if not wait before checking again
                    print(f"Waiting for turn on protocol node {pn}...")
                    time.sleep(10)
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
