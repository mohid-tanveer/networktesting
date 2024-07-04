import os
import sys

# on exit update scatter-plots with any new data
def on_exit():
    print("Updating relevant scatterplots...")
    os.system([f"python3 ../scatterplotcreation/src/scatterplot.py ../results/clusterIB\ multithreaded.csv"])

# check and run loop
while True:
    try:
        print(f"Running single threaded script")
        os.system(f"python singlethreadedclusterIB.py")
        print(f"Running multi threaded script")
        os.system(f"python multithreadedclusterIB.py")
    except KeyboardInterrupt:
        on_exit()
        sys.exit(0)
