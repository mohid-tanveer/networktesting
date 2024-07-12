import os
import sys
import time
from secret import turn_order
import subprocess


# get the host name
host_name = 'cluster'

# control file path (./control.txt)
CONTROL_FILE = '../../controlfolder/control.txt'

# local script path (./filetransfer.py)
SCRIPT_PATH = './clusteroverib.py'

# on exit update scatter-plots with any new data
def on_exit():
    # update control.txt to exit
    with open(CONTROL_FILE, "w") as f:
        f.write('KeyboardInterrupt')
        
    print("Updating relevant scatterplots...")
    # Define the path to the scatterplot creation directory
    scatterplot_creation_dir = "../scatterplotcreation"
    
    # Create virtual environment if it doesn't exist
    subprocess.run(["pip", "install", "virtualenv"], check=True)
    venv_dir = os.path.join(scatterplot_creation_dir, "venv")
    if not os.path.exists(venv_dir):
        subprocess.run(["virtualenv", venv_dir], check=True)
    
    scatterplot_script = os.path.join(scatterplot_creation_dir, "src", "clusterscatter.py")
    results_file = f"../results/{host_name}IB.csv"
    activate_script = os.path.join(venv_dir, "bin", "activate")

    # Activate virtual environment and run the script
    # Install dependencies
    activate_and_run_commands = f"source '{activate_script}' && pip install -r '{os.path.join(scatterplot_creation_dir, "requirements.txt")}' && python '{scatterplot_script}' '{results_file}' && deactivate"
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
        # check if local machine's turn
        if check_turn():
            print(f"Running script")
            subprocess.run(f"python {SCRIPT_PATH}", shell=True, check=True)
            switch_turn()
        else:
            # if not wait before checking again
            print(f"Waiting for turn...")
            time.sleep(10)
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
