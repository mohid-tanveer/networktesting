# Network Testing

This repository contains files and scripts for testing network and storage transfer speeds. The purpose of this project is to measure the performance of file transfers between a local machine and a remote folder or server.

## File Structure

The file structure of this repository is as follows:

```plaintext
networktesting/
├── README.md
├── boxandwhiskercreation/
│    ├── output/ (folder to hold PDFs produced)
│    ├── requirements.txt (required packages for python compilation)
│    └── src
│    │   ├── boxandwhisker.py (produce box and whisker plots for data partitioned by day)
│    │   ├── boxandwhiskertotal.py (produce box and whisker plots for all data collected)
│    │   ├── dataformatting.py (format csv data for boxplotting)
│    │   └── ~sssecret.py (file with paths and turn order for automator)
├── results/
│   ├── mtanveer (DataCenter).csv (sample output file storing results from file transfers to host mtanveer in location DataCenter)
├── scatterplotcreation/
│   ├── output/ (folder to hold PDFs produced)
│   ├── requirements.txt (required packages for python compilation)
│   └── src/
│   │   ├── clusterscatter.py (produce scatterplots for cluster data partitioned by day)
│   │   ├── dataformatting.py (format csv data for scatterplotting)
│   │   ├── scatterplot.py (produce scatterplots for data by workstation partitioned by day)
│   │   ├── scatterplotconsolidated.py (produce scatterplots for data by workstation)
│   │   ├── scatterplotunaveraged.py (produce scatterplots for unaveraged data by workstations partitioned by day)
│   │   └── ~ssecret.py (file with paths and turn order for automator)
└── scripts/
      ├── automator.py (automates the running of file transfer and pn shifting between two machines (connects with below))
      ├── clusterautomator.py (automates the running of file transfer on the cluster (connects with above))
      ├── clusteroverib.py (transfers files on cluster over Infiniband connection)
      ├── clusteroverpn.py (transfers files on cluster over SMB connection)
      ├── control.txt ("lock" file for automator.py, indicates which machine is currently transferring)
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
- `boxandwhiskercreation/`: This directory contains the scripts used to produce box and whisker plots of data collected.
- `results/`: This directory stores the results of the network testing in CSV format.
- `scatterplotcreation/`: This directory contains the scripts used to produce scatterplots of data collected.
- `scripts/`: This directory contains the scripts used for both the network/storage testing as well as data creation.
- ~ (Notes: `secret.py` is not included in this repository for security reasons. It contains sensitive information and should be created locally as applicable to usage.)

## Usage

To perform network testing, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the `scripts/` directory.
3. Create a file `secret.py` or declare necessary variables locally as needed by specified script.
4. Run the `filetransfer.py` script, passing a protocol node (ex: pn001) as an argument, to initiate the file transfer.
5. Once the transfer is complete, the script will generate the results and append the values to the files in the results folder.

Variants of the normal file transfer are as follows:

- `automator.py`: This variant automates the process of protocol node shifting, machine variation, and scatterplot production following updated results. `multiautomator.py`, `clusterautomator.py`, and `multiclusterautomator.py` work in the same manner, only varying the location of testing (cluster for file transfers over IB rather than network) or type of file transfer (multithreaded transferring compared to normal singlethreaded tests).
- `clusteroverib.py`: This variant works exactly the same, only reading the file "locally" on the cluster over an Infiniband connection. `clusteroverpn.py` works more similarly to the `filetransfer.py` script by transferring through protocol node on the cluster.
- `multithreaded.py`: This variant runs a multithreaded file transfer and is paired with the `singlethreaded.py` file for comparison of results when automated. `multithreadedclusterIB.py` and `singlethreadedclusterIB.py` are also paired for multithreaded transfers over IB on the cluster.

Please note that you may need to modify the scripts to specify the remote folder or server you wish to test.
