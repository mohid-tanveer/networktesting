import os
import sys
import socket
from secret import sp2, sp3, locations, remotepath
import subprocess

# Get the host name and location of the machine
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
    # Define the path to the scatterplot creation directory
    scatterplot_creation_dir = r"..\scatterplotcreation"
    
    # Create virtual environment if it doesn't exist
    subprocess.run(["pip", "install", "virtualenv"], check=True)
    venv_dir = os.path.join(scatterplot_creation_dir, "venv")
    if not os.path.exists(venv_dir):
        subprocess.run(["virtualenv", venv_dir], check=True)
    
    scatterplot_script = os.path.join(scatterplot_creation_dir, "src", "scatterplot.py")
    results_file = f"{os.path.join(remotepath, 'results', f'{host_name} ({location}) multithreaded.csv')}"
    activate_script = os.path.join(venv_dir, "Scripts", "activate.bat")

    # Activate virtual environment and run the script
    # Install dependencies
    activate_and_run_commands = f"\"{activate_script}\" && pip install -r \"{os.path.join(scatterplot_creation_dir, 'requirements.txt')}\" && python \"{scatterplot_script}\" \"{results_file}\" r {host_name} && deactivate"
    subprocess.run(activate_and_run_commands, shell=True, check=True)

# check and run loop
while True:
    try:
        # alternate between protocol nodes
        for pn in pn_choices:
            arg = pn
            print(f"Running single threaded script")
            subprocess.run(f"python {SCRIPT_PATH2} {arg}", shell=True, check=True)
            print(f"Running multi threaded script")
            subprocess.run(f"python {SCRIPT_PATH} {arg}", shell=True, check=True)
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
