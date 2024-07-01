# Network Testing

This repository contains files and scripts for testing network and storage transfer speeds. The purpose of this project is to measure the performance of file transfers between a local machine and a remote folder or server.

## File Structure

The file structure of this repository is as follows:

```plaintext
networktesting/
├── README.md
├── results/
│   ├── mtanveer_tengigfile.csv (sample output file storing results from folder 'tengigfile' to host mtanveer)
│   ├── mtanveer_tenmegfiles.csv (sample output file storing results from folder 'tenmegfiles' to host mtanveer)
│   └── mtanveer_tenmegfiles_individual.csv (same as above for individual files being transferred from the folder)
└── scripts/
      ├── afterhours.py (script to iterate through all protocol nodes during afterhours)
      ├── automator.py (automates the running of file transfer and pn shifting between two machines)
      ├── clusteroverib.py (transfers files on cluster over Infiniband connection)
      ├── clusteroverpn.py (transfers files on cluster over SMB connection)
      ├── control.txt ("lock" file for automator.py, indicates which machine is currently transferring)
      ├── data_creation/
      │   ├── 10g.py (sample script to create a 10gb file)
      │   └── 10m.py (sample script to create 10gb worth of 10mb files)
      └── filetransfer.py (file transfer script over remote SMB connection)
```

- `README.md`: This file provides an overview of the project and its file structure.
- `results/`: This directory stores the results of the network testing in CSV format.
- `scripts/`: This directory contains the scripts used for both the network/storage testing as well as data creation.

## Usage

To perform network testing, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the `scripts/` directory.
3. Run the `filetransfer.py` script, passing a protocol node (ex: pn001) as an argument, to initiate the file transfer.
4. Once the transfer is complete, the script will generate the results and append the values to the files in the results folder.

Please note that you may need to modify the scripts to specify the remote folder or server you wish to test.
