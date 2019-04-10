# Synthetic Data

This folder contains all of the information regarding the cleaning and generation of data. To date, this project lacks a real world training dataset and thus for the completion of this project we had to rely on synthetically generating our own data based on common rules we saw across multiple receipt items from different stores. **NOTE:** once legitimate real world data is obtained, the synthetic data and its entire pipeline should be REPLACED.

# How the Synthetic Data Generation and the Manual Data Pipelines Work

## /synthetic_data/data/

The `/synthetic_data/data/` folder holds all data files, including:
* `products.csv` - the data downloaded from USDA website containing uncleaned, branded, and descripted data
* `receipt_data_manual.csv` - the manually collected receipt information (~ 400 lines) for manual evaluation of our algorithms 
* `cleaned_*.csv` - data that has run through the cleaning pipeline and has been cleaned
  * `cleaned_branded_data.json` - cleaned data containing brands (to test approaches dealing with brands)
  * `cleaned_data.json` - cleaned data WITHOUT brands (to test approaches dealing with NO brands)
  * `cleaned_receipt_data_manual.csv` - cleaned manual data that goes through the same cleaning process found in `EDA_Cleaning.ipynb`
* `no_matches_manual_data.csv` - a list of all manually collected data with no corresponding match in `products.csv`
* `final_train_labels.json` - json file containing training data and training labels after having run through the synthetic data generation pipeline (~ 500k lines of data)
* `final_branded_train_labels.json` - json file containing branded training data and training labels after having run through the synthetic data generation pipeline
* `abbreviated_brands.json` - json file containing all brands and their corresponding representation in receipt format (EX: "VILLAGE HEARTH" --> "VLLG HRTH")
* `abbreviated_descriptors.json` - json file containing all descriptors and their corresponding representation in receipt format (EX: "PREMIUM" --> "PRMM")
* `brands.json` - json file containing a list of all the brands we have identified in `products.csv`
* `descriptors.json` - json file containing a list of all the descriptors we have identified in `products.csv` like: "100% natural", "premium", "organic", etc


To start the manual data cleaning pipeline, only `receipt_data_manual.csv` is required. All of the other manual data files, listed below, are generated off of `receipt_data_manual.csv`.
* `cleaned_receipt_data_manual.csv` 
* `no_matches_manual_data.csv`

To start the synthetic data generation pipeline, only `products.csv` is required. All of the other files are generated off of `products.csv`.


## /synthetic_data/scripts/

This folder contains all of the scripts necessary clean out the data from `products.csv` and generate our training data and training labels from our self-deduced receipt mapping rules. It also includes a script that cleans the manual data.

Relevant files:
* `EDA_Cleaning.ipynb` - .ipynb script containing code to explore the dataset and clean out `products.csv` by removing details such as descriptors, brands, units, bad products, symbols, bad characters (commas, etc). **This script outputs:** `/synthetic_data/data/descriptors.json`, `/synthetic_data/data/cleaned_branded_data.json`, `/synthetic_data/data/cleaned_data.json` 
* `synthetic_data_generator.ipynb` - .ipynb script with all of our manually generated rules to create synthetic training data and labels. **This script outputs:** `/synthetic_data/data/final_train_labels.json`, `/synthetic_data/data/abbreviated_brands.json`, `/synthetic_data/data/abbreviated_descriptors.json`. The current rules are:
  * first_char - takes first 3 characters of every word
  * first_last_char - takes first and last characters of every word
  * first_consonants - takes first three consonants of every word
  * first_last_consonants - takes first two and last consonants of every word
  * brand_first_letters - takes first letter of each word in the brand (if present)
  * first_letters - takes first letter of each word
  * remove_vowels - removes all vowels
* `manual_data_cleaning.ipynb` - cleans all of the manually collected data and corresponding products.csv matches in the same way as EDA_Cleaning.ipynb **This script outputs:** `/synthetic_data/data/cleaned_receipt_data_manual.csv`, `/synthetic_data/data/no_matches_manual_data.csv`

To run a script, simply run through all the cells.

## How to clean manually collected data:
* If necessary, update products.csv from the USDA website (only updated once or twice a year)
  * Go to https://ndb.nal.usda.gov/ndb/search/list?maxsteps=6&format=&count=&max=25&sort=fd_s&fgcd=&manu=&lfacet=&qlookup=&ds=&qt=&qp=&qa=&qn=&q=&ing=&offset=550&order=asc
  * Click downloads
  * Select BFPD ASCII Files
  * Rename “products.csv” and place in the data folder in synthetic_data
* Collect data in a csv file called “receipt_data_manual.csv” (save in the data folder) with the following columns
  * receipt_name (the actual abbreviated name found on the receipt)
  * full_product_title (what the full product title of the item is that uniquely defines it, like “Granny Smith Apples”)
  * general_product_title (the off hand name people use to refer to this product, like “apples”)
  * store (the store where the item was bought)
  * product_database (what you think the best match in products.csv is for this item)
* Run “manual_data_cleaning.ipynb” found in the scripts folder in synthetic_data. This will generate two files:
  * “cleaned_receipt_data_manual.csv”: a cleaned version of receipt data manual csv
    * All entries have leading and trailing spaces removed
    * Capitalization is standardized
    * The products.csv matches in the column “products_database” are cleaned in the same way that products.csv is cleaned in “EDA_Cleaning.ipynb”
    * The results are found in new columns called “no_brand_descriptor_title” and “no_descriptor_title”
  * “no_matches_manual_data.csv”: a list of all the receipt items for which you did not find a suitable match in products.csv. These represent the limitations of the USDA database
