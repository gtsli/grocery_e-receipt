import re
import numpy as np

from decimal import Decimal

from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
from weighted_levenshtein import lev, osa, dam_lev
app = Flask(__name__)

@app.route("/get-receipt-info", methods=["GET"])
def get_receipt_info():
	receipt = request.data.decode('utf-8')
	print (type(receipt))
	store = get_store(receipt)
	date = get_date(receipt)
	items = get_items(receipt)
	total = get_total(receipt)
	return jsonify(date=date, items=items, store=store, total=total, unknowns=[])


def get_store(receipt):
    # find start of address line
    lines = receipt.splitlines()
    curr = 0
    while "<p class=\"MsoNormal\" align=\"center\" style=\"text-align:center\">" \
          "<span style=\"font-size:10.0pt;font-family:Courier\"><" not in lines[curr]:
        curr += 1
        # error if no address found
        if curr == len(lines):
            return None

    address = re.findall(r'>(?:[A-Za-z]|\d|\s|\.)+</a>', lines[curr])[0]
    address = address[1:-4]
    curr += 1
    address += " " + re.findall(r'(.*?)<u>', lines[curr])[0]
    return address


def get_date(receipt):
    return re.findall(r'\d\d\/\d\d\/\d\d\d\d', receipt)[0]


def get_total(receipt):
    return re.findall(r'\$\d?\d\.\d\d', receipt)[0]


def get_items(receipt):
    # find start of line items
    lines = receipt.splitlines()
    curr = 0
    while not lines[curr].startswith("<pre style=\"text-align:center\">"):
        curr += 1
        # error if no items found
        if curr == len(lines):
            return None

    # parse out items and price
    items = []
    while "Order Total" not in lines[curr]:
        if "Promotion" in lines[curr]:
            # subtract promotion from previous line
            print(re.findall(r'(?:\d?\d?\d\.\d\d)', lines[curr])[0])
            promotion = Decimal(re.findall(r'(?:\d?\d?\d\.\d\d)', lines[curr])[0])
            items[-1][1] = str(Decimal(items[-1][1]) - promotion)
        elif "You Saved" not in lines[curr]:
            item = re.findall(r'(?:[A-Z]|\d)(?:[A-Z]|\s|\d|\.|%)+', lines[curr])
            if len(item) == 1:
                curr += 1
                # get price from next line
                next_line = re.findall(r'(?:\d?\d?\d\.\d\d)', lines[curr])
                item.append(next_line[-1])
                items.append(item)
            else:
                items.append(item[:2])
        curr += 1

    return translate_items(items)


# work will be done here
def translate_items(items):
    translated = []
    for item in items:
        translated.append(find_closest_string_weighted(item[0]))
    return translated


def find_closest_string(string):
    products = open("resources/Products")
    closest_ratio = None
    closest_string = None
    for line in products.readlines():
        distance = fuzz.ratio(string, line.lower())
        if closest_ratio is None or distance > closest_ratio:
            closest_ratio = distance
            closest_string = line.lower()
    return closest_string


def find_closest_string_weighted(string):
    print("string: " + string)
    insert_costs = np.full(128, .3, dtype=np.float64)  # make an array of all 1's of size 128, the number of ASCII characters
    transpose_costs = np.full((128, 128), .7, dtype=np.float64)
    delete_costs = np.full(128, 1.2, dtype=np.float64)
    # delete_costs = np.ones(128, dtype=np.float64)
    # print(transpose_costs)
    # print(delete_costs)
    products = open("resources/Products")
    # products = open("resources/cleaned_data_branded.csv")
    closest_distance = 999999
    closest_string = None
    # print(dam_lev('BANANA', 'BANANAAAAA', insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs))
    # debug = True
    for line in products.readlines():
        # cost to go from string to product name
        # distance = lev(string, line.lower(), insert_costs=insert_costs, delete_costs=delete_costs)
        # print("product: " + str(line.upper()))
        # if debug == True:
        #     print(line.upper().strip())
            # print(len(line.upper().strip()))
            # print(len("MOCHI ICE CREAM BONBONS"))
            # debug = False
        # if line.lower() == "bananas":
        #     print("@@@@@@@LKAJSDKASLKJDLAJSLD:AJ")
        distance = osa(string.lower(), line.lower(), insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs)
        # if line.lower().strip() == "bananas":
        #     print("distance: " + str(distance)) 
        # distance = dam_lev(string, line.lower(), insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs)
        # distance = fuzz.ratio(string, line.lower())
        if closest_distance is None or distance < closest_distance:
            closest_distance = distance
            closest_string = line.lower()
    print("closest_string: " + closest_string)
    # print("closest_distance: " + str(closest_distance))
    return closest_string


if __name__ == "__main__":
    # find_closest_string_weighted("strawberry yogurt!!!")
    # find_closest_string_weighted("strwbry ygrt")
    # find_closest_string_weighted("BANANAS")
    app.run(debug=True, use_reloader=False)