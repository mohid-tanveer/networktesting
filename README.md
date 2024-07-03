# Network Testing

This repository contains files and scripts for testing network and storage transfer speeds. The purpose of this project is to measure the performance of file transfers between a local machine and a remote folder or server.

## File Structure

The file structure of this repository is as follows:

```plaintext
networktesting/
├── README.md
├── results/
│   ├── mtanveer (DataCenter).csv (sample output file storing results from file transfers to host mtanveer in location DataCenter)
├── scatterplotcreation/
│   ├── requirements.txt
│   └── output/ (folder to hold PDFs produced)
│   └── src/
│       ├── dataformatting.py (format excel data for scatterplotting)
│       └── scatterplot.py (produce scatterplots per machine partitioned by day)
└── scripts/
      ├── automator.py (automates the running of file transfer and pn shifting between two machines)
      ├── clusteroverib.py (transfers files on cluster over Infiniband connection)
      ├── clusteroverpn.py (transfers files on cluster over SMB connection)
      ├── ~control.txt ("lock" file for automator.py, indicates which machine is currently transferring)
      ├── data_creation/
      │   ├── 10g.py (sample script to create a 10gb file)
      │   └── 10m.py (sample script to create 10gb worth of 10mb files)
      ├── filetransfer.py (file transfer script over remote SMB connection)      
      ├── multiautomator.py (automates the running of m-t file transfer and pn shifting between two machines)    
      ├── multiclusterautomator.py (automates the running of m-t file transfer on the cluster over IB)   
      ├── multithreaded.py (multi-threaded file transfer script over remote SMB connection)    
      ├── multithreadedclusterIB.py (multi-threaded file transfer script over IB connection on cluster)          
      ├── ~secret.py (file with paths and turn order for automator)
      ├── singlethreaded.py (single-threaded file transfer for multithreaded test script)
      └── singlethreadedclusterIB.py (single-threaded file transfer for multithreaded cluster test script)
```

- `README.md`: This file provides an overview of the project and its file structure.
- `results/`: This directory stores the results of the network testing in CSV format.
- `scatterplotcreation/`: This directory contains the scripts used to produce scatterplots of data collected.
- `scripts/`: This directory contains the scripts used for both the network/storage testing as well as data creation.
- ~ (Notes: `control.txt` and `secret.py`are not included in this repository for security reasons. They contain sensitive information and should be created locally as applicable to usage.)

## Usage

To perform network testing, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the `scripts/` directory.
3. Run the `filetransfer.py` script, passing a protocol node (ex: pn001) as an argument, to initiate the file transfer.
4. Once the transfer is complete, the script will generate the results and append the values to the files in the results folder.

Please note that you may need to modify the scripts to specify the remote folder or server you wish to test.
