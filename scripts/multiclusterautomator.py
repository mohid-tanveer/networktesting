import os
import sys
import atexit
import signal
import socket

round_complete = False

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")
    os.system([f"python3 ../scatterplotcreation/src/scatterplot.py ../results/clusterIB\ multithreaded.csv"])


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
    os.system(f"python multithreadedclusterIB.py")
    print(f"Running multi threaded script")
    os.system(f"python singlethreadedclusterIB.py")
