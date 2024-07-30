import os
import sys
import subprocess

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")
    # define the path to the scatterplot creation directory
    scatterplot_creation_dir = "../scatterplotcreation"
    
    # create virtual environment if it doesn't exist
    subprocess.run(["pip", "install", "virtualenv"], check=True)
    venv_dir = os.path.join(scatterplot_creation_dir, "venv")
    if not os.path.exists(venv_dir):
        subprocess.run(["virtualenv", venv_dir], check=True)
    
    scatterplot_script = os.path.join(scatterplot_creation_dir, "src", "clusterscatter.py")
    results_file = f"../results/clusterIB multithreaded.csv"
    activate_script = os.path.join(venv_dir, "bin", "activate")

    # activate virtual environment, install dependencies, and run the script
    activate_and_run_commands = f"source '{activate_script}' && pip install -r '{os.path.join(scatterplot_creation_dir, "requirements.txt")}' && python '{scatterplot_script}' '{results_file}' && deactivate"
    subprocess.run(activate_and_run_commands, shell=True, check=True)

# check and run loop
while True:
    try:
        print(f"Running single threaded script")
        subprocess.run(f"python singlethreadedclusterIB.py", shell=True, check=True)
        print(f"Running multi threaded script")
        subprocess.run(f"python multithreadedclusterIB.py", shell=True, check=True)
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
