# Network Testing

This repository contains files and scripts for testing network and storage transfer speeds. The purpose of this project is to measure the performance of file transfers between a local machine and a remote folder or server.

## File Structure

The file structure of this repository is as follows:

```plaintext
networktesting/
├── README.md
├── scripts/
│    ├── filetransfer.py
│    ├── localfiletransfer.py
│    └── data_creation/
│          ├── 10g.py (sample script to create a 10gb file)
│          └── 10m.py (sample script to create 10gb worth of 10mb files)
└── results/
      ├── mtanveer_tengigfile.csv (sample output file storing results from folder 'tengigfile' to host mtanveer)
      ├── mtanveer_tenmegfiles.csv (sample output file storing results from folder 'tenmegfiles' to host mtanveer)
      └── mtanveer_tenmegfiles_individual.csv (same as above for individual files being transferred from the folder)
```

- `README.md`: This file provides an overview of the project and its file structure.
- `scripts/`: This directory contains the scripts used for both the network/storage testing as well as data creation.
- `results/`: This directory stores the results of the network testing in CSV format.

## Usage

To perform network testing, follow these steps:

1. Clone this repository to your local machine.
2. Navigate to the `scripts/` directory.
3. Run the `filetransfer.py` script to initiate the file transfer.
4. Once the transfer is complete, the script will generate the results and append the values to the files in the results folder.

Please note that you may need to modify the scripts to specify the remote folder or server you wish to test.
