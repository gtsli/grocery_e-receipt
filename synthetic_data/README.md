Synthetic Data

This folder contains all of the information regarding the cleaning and generation of data.

The data folder holds all data files, including:
	- the data downloaded from USDA website (products.csv)
	- the manually collected receipt information (receipt_data_manual.csv)
	- cleaned data (any file starting with "cleaned_")

	Currently, our team keeps track of manually collected receipt data in a Google Drive document. This document needs to be downloaded into this folder and replace the old receipt_data_manual.csv. Any time a new receipt_data_manual.csv is created, the manual_data_cleaning script needs to be run to clean all of the new information to create an updated testing set.

	USDA updates their downloadable databases once or twice a year. When this happens, the new database will need to be downloaded, and the cleaning and data generation process will need to be repeated

The scripts folder contains all of the scripts that clean or generate data
	- EDA_cleaning.ipynb cleans products.csv to create cleaned_data.json and cleaned_branded_data.json, which are used to generate synthetic data
	- manual_data_cleaning.ipynb cleans receipt_data_manual.csv to create cleaned_receipt_data_manual.csv, which is used as a testing set for our approaches
	- synthetic_data_generator.ipynb takes in either cleaned_data.json or cleaned_branded_data.json and applies different rules and patterns to generate abbreviations that simulate what would be on a real receipt. The output is called final_train_labels.json

To run a script, use Jupyter Notebook. All scripts are written in Jupyter Notebooks due to the volume of data being processed.

Any sr_legacy files pertain to the second database that USDA offers, which mostly contains produce items. We are currently not working with this data due to the volume of data
