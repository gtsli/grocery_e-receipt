# API

This folder contains all the files necessary to set up a local server using Flask and test our logic.

The resources folder contains every product title line by line from the USDA database. We will probably delete this in the future.

The test_files folder contains test HTML files to test our logic on. So far, the logic is hardcoded only for the Publix receipt.

The receipt_reader python file contains all of our logic thus far to set up the Flask server, parse, and translate e-receipts.

## To set up the server and test:

You will probably want Postman to make a GET HTTP request to the server.
Install at https://www.getpostman.com

To run the the web service via Flask, run the following command:
```
$ Python receipt-reader.py
```

Using Postman, make a GET request to the endpoint /get-receipt-info with the text from the Publix e-receipt HTML in the body of Postman as plain text.
Ex.: 127.00.1:5000/get-receipt-info

The Publix e-receipt is located in the /test_files folder
