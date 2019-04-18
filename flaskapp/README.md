# Getting Started
To get started with the webapp and visualize the results of the algorithms, please make sure all the relevant libraries are installed by following the directions in the global README.

### Instructions:
1. *Due to the massive size of the trained LSTM model that we use in the backend, it is not possible to store the model on GitHub. Please navigate to `approaches/LSTM` and follow the instructions to train an LSTM model (Note, this may take some time). After this step is complete, continue to step 2.*
2. Make sure the trained model is in the directory `/approaches/LSTM/models`
3. Open a terminal, navigate to `/flaskapp/`
4. Type: `$ python server.py`. This will get the back end server up and running on `localhost:5000`.
5. Open a new browser (preferably incognito due to caching) and enter: `localhost:5000` in the URL. This will take you to the home page of the UI. 
6. Now, to set up the receipt parsing engine, open up a *second* terminal and navigate to `/api`
7. Type: `$ python receipt_reader.py`. This will set up the receipt reading engine on `localhost:8080`.
8. From here, you can select a Publix e-receipt to parse. We have included sample Publix e-receipts in `/api/test_files`. Selecting one of these and pressing "View Parsed Receipt Data" will send the e-receipt to the server which will:
	1. Parse the receipt
	2. Display the relevant results like: `date`, `items`, `store`, `total`, `unknowns`
	3. Predict the items the user purchased with a weighted edit distance approach and an LSTM model
9. You can also use the search bar to manually type in any receipt line item you may be curious about, for example: `hrzn mlk`, `dssrt`, `choclt cndy`, etc     