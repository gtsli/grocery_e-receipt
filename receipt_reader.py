import re
from decimal import Decimal

from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/get-receipt-info", methods=["GET"])
def get_receipt_info():
    receipt = request.get_data()
    store = get_store(receipt)
    date = get_date(receipt)
    items = get_items(receipt)
    total = get_total(receipt)
    return jsonify(date=date, items=items, store=store, total=total)


def get_store(receipt):
    return""


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
    return items


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


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)