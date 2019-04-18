
# Personal Virtual Inventory Receipt Translation Github

## Release Notes version Receipt Understanding 1.0

#### New Software Features
* Manually collected receipt data cleaning process
* Synthetic data generation process
* Initial trials of deep learning approaches to translate receipt data
* Initial trials of edit distance to translate receipt data
* Initial trials of gradient boosted decision trees to translate receipt data
* API to connect to basic receipt parser and receipt translation machine learning models
* Demo UI to showcase the functionality of the receipt translation machine learning models

#### Bug Fixes
* Optimized edit distance approach by organizing the data into buckets and only searching through relevant buckets
* Search functionality in UI only worked on some machines and not others-- now works on all machines

#### Known Bugs and Defects
* The approaches contained in this release represent the initial research conducted in this area and are not ready for production/sale. They do, however, represent a good base from which to move forward
* API receipt parsing is hard coded to read Publix receipts only and has only been tested with one Publix e-receipt since this is not the focus of the release
* Due to a lack of available real world data, the machine learning approaches were trained using synthetic data. If real world data is obtained, the models should be retrained
* We have only about 380 manually collected receipts for testing purposes. There is some inconsistency in matching each receipt item to USDA database items due to human error and variability

# Introduction

Over 100 million Americans are currently diagnosed with diabetes or prediabetes and this number is only expected to grow in the near future. Diabetes is often associated with a plethora of negative effects, including drastic unwanted changes in lifestyle, negative body image, and poor mental health. While lifestyle changes decrease the chance of a prediabetic patient becoming diabetic by 17%, the current standard practices for helping prediabetic patients make this jump (a brochure, food journaling, etc.) are either impersonal, distant, or time-consuming. Our client Gavin Max, experienced businessman and entrepreneur, has conducted extensive market research and inquiry to create the Personal Virtual Inventory (PVI) project, the future tool for aiding prediabetic individuals in making healthy dietary decisions.

The Personal Virtual Inventory Project will help millions of diabetic and prediabetic individuals take control of their health by keeping track of their food purchases and formulating meal plans that adhere to dietary restrictions recommended by doctors. The idea of the project is to read in electronic receipts and automatically populate an inventory for a user, which they can use to keep track of their physical food inventory with minimal manual input. The system will use this inventory to generate recipes that follow any medical-necessary diets to support a healthy lifestyle. Due to the complex nature of this project, our team is specifically focusing on creating an API that can accept an electronic receipt and return pertinent information from the receipt, including the grocery store, the total cost of the purchase, and a description of each item that was purchased. We will focus solely on electronic receipts received via email that grocery stores like Publix and Walmart currently support; these emails often use HTML to format the receipt within the email.

## Pipeline

The following displays the general pipeline of the project. For more information about this project and the pipeline process, review the accompanying documentation. 
<img src="imgs/Pipeline_Static.jpg" width="1000" height="600">

# Install Guide

## Pre-requisites
Before continuing, it is necessary to have several components:
* A C++ compiler. Please install [Build Tools for Microsoft Visual Studio]([https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017)). Scroll down to `Tools for Visual Studio 2019` and press download on the section titled: `Build Tools for Visual Studio 2019`. 
* This project requires [python 3.6](https://www.python.org/downloads/)+. Please install [python 3.6](https://www.python.org/downloads/) for the designated operating system you are using. If asked about putting python in your PATH, say yes. 
* This project uses postman for manually testing the API. If you wish to manually test the API, please install postman [here](https://www.getpostman.com/downloads/).

Once all the above pre-requisites are downloaded, open a terminal or command prompt. Navigate to the root directory of the project. We have provided a build script to install all of the necessary dependencies and libraries for this project. To install them, follow the command:
```
$ sudo pip install --upgrade pip
$ pip install --upgrade -r requirements.txt
```
If the above does not work on Windows, try:
```
$ pip install --user --upgrade -r requirements.txt
```
You are set!

## Troubleshooting
* If you are using a virtual environment like `Anaconda`, Microsoft's C++ build tools may not work inside your virtual environment due to environment paths. Please deactivate your environment and rerun the build script (only `weighted-levenshtein` library requires the C++ build tools)
* If the build script (`requirements.txt`) does not work due to a version imbalance (very low chance of happening), please either:
	* Update your pip with: `$ sudo pip install --upgrade pip` or
	* Go into `requirements.txt` and change the version requirements to a supported version. Ex: `keras==2.2.4` --> `keras==2.2.5`, etc.




**PLEASE NOTE: Every major project folder contains their own individual and unique README that heavily details both the content of the folder and how to run it**




# Navigation

This project is organized by the different high level folders, each high level folder has a more detailed README as well to help describe necessary steps for set up, explain the file structure, content, and dependencies: 

#### /api
This section contains the code necessary to run the web service (API) that can receive an HTML receipt as input and return the JSON-formatted parsing of the receipt.
#### /approaches
This section contains the code written to test and train the three different approaches used to try to understand receipts.
#### /flaskapp 
This section contains all the necessary code to run a webapp that will display every functionality of this project. 
#### /synthetic data 
This section contains the code written to process the USDA branded product database by cleaning it and generating synthetic data that can be used for the different approaches.