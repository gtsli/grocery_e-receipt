# Synthetic Data

This folder contains all of the information regarding the cleaning and generation of data. To date, this project lacks a real world training dataset and thus for the completion of this project we had to rely on synthetically generating our own data based on common rules we saw across multiple receipt items from different stores. **NOTE:** once legitimate real world data is obtained, the synthetic data and its entire pipeline should be REPLACED.

# How The Synthetic Data Generation Pipeline Works

## /synthetic_data/data/

The `/synthetic_data/data/` folder holds all data files, including:
* `products.csv` - the data downloaded from USDA website containing uncleaned, branded, and descripted data
* `receipt_data_manual.csv` - the manually collected receipt information (~ 400 lines) for manual evaluation of our algorithms 
* `cleaned_*.csv` - data that has run through the cleaning pipeline and has been cleaned
  * `cleaned_branded_data.json` - cleaned data containing brands (to test approaches dealing with brands)
  * `cleaned_data.json` - cleaned data WITHOUT brands (to test approaches dealing with NO brands)
* `final_train_labels.json` - json file containing training data and training labels after having run through the synthetic data generation pipeline (~ 500k lines of data)
* `final_branded_train_labels.json` - json file containing branded training data and training labels after having run through the synthetic data generation pipeline
* `abbreviated_brands.json` - json file containing all brands and their corresponding representation in receipt format (EX: "VILLAGE HEARTH" --> "VLLG HRTH")
* `abbreviated_descriptors.json` - json file containing all descriptors and their corresponding representation in receipt format (EX: "PREMIUM" --> "PRMM")
* `brands.json` - json file containing a list of all the brands we have identified in `products.csv`
* `descriptors.json` - json file containing a list of all the descriptors we have identified in `products.csv` like: "100% natural", "premium", "organic", etc



To start the pipeline, only `products.csv` is required. All of the other files are generated off of `products.csv`. To run this script, simply run through all the cells.

## /synthetic_data/scripts/

This folder contains all of the scripts necessary clean out the data from `products.csv` and generate our training data and training labels from our self-deduced receipt mapping rules.

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

To run this script, simply run through all the cells.