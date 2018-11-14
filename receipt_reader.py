from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/get-receipt-info", methods=["GET"])
def getReceiptInfo():
    receipt = request.get_data()
    soup = BeautifulSoup(receipt, "html.parser")
    items = list(soup.p.stripped_strings)
    receipt_info = []
    for item in items[0].splitlines():
        print(item.lower())
        receipt_info.append(find_closest_string(item.lower()))
    return jsonify({"items": receipt_info})

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
    app.run(debug=True)