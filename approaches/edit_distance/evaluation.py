# evaluation.py - evaluate weighted edit distance
import csv
import sys
import json
import numpy as np

sys.path.insert(0, '../evaluation')
from eval import partial_acc  

from fuzzywuzzy import fuzz
from weighted_levenshtein import lev, osa, dam_lev

def find_closest_string(string):
    print("string: " + string)
    products = open("../../api/resources/Products")
    closest_ratio = None
    closest_string = None
    for line in products.readlines():
        distance = fuzz.ratio(string, line.lower())
        if closest_ratio is None or distance > closest_ratio:
            closest_ratio = distance
            closest_string = line.lower()
    print("closest_string: " + str(closest_string))
    return closest_string


def find_closest_string_weighted(string):
    print("string: " + string)
    
    with open('cleaned_bucket_data.json', encoding="ASCII") as f:
        data = json.load(f)        

    # find first letter of every word in the string
    words = string.split()
    letters = [word[0] for word in words]

    # get corresponding buckets 
    first_letter = string[0]
    products = []
    for bucket in data:
        if bucket[0][0] == first_letter:
            products += bucket

    # remove non-ascii characters
    cleaned_products = []
    for entry in products:
        cleaned_entry = ""
        for character in entry:
            if ord(character) <= 128:
                cleaned_entry += character
        cleaned_products.append(cleaned_entry)

    insert_costs = np.full(128, .3, dtype=np.float64)  # make an array of all 1's of size 128, the number of ASCII characters
    transpose_costs = np.full((128, 128), .7, dtype=np.float64)
    delete_costs = np.full(128, 1.2, dtype=np.float64)

    closest_distance = 999999
    closest_string = None

    for line in cleaned_products:
        distance = osa(string.lower(), line.lower(), insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs)
        if closest_distance is None or distance < closest_distance:
            closest_distance = distance
            closest_string = line.lower()
    print("closest_string weighted: " + str(closest_string))
    return closest_string


with open("../../synthetic_data/data/receipt_data_manual.csv") as manual:
	lines = csv.reader(manual)
	# skip the first line, which is a header
	next(manual)
	edit_distance_predicted = []
	weighted_edit_distance_predicted = []
	actual = []

	# testing purposes
	# row = next(lines)
	# # print(row[0])
	# receipt_name = row[0]
	# edit_distance = find_closest_string(receipt_name)
	# weighted_edit_distance = find_closest_string_weighted(receipt_name)
	# edit_distance_predicted.append(edit_distance)
	# weighted_edit_distance_predicted.append(weighted_edit_distance)
	# actual.append(row[4])

	for row in lines:
		receipt_name = row[0]
		database_name = row[4]
		if not (database_name == None or len(database_name) == 0):
			edit_distance = find_closest_string(receipt_name)
			weighted_edit_distance = find_closest_string_weighted(receipt_name)
		
			if not (edit_distance == None or len(edit_distance) == 0) and not (weighted_edit_distance == None or len(weighted_edit_distance) == 0):
				edit_distance_predicted.append(edit_distance)
				weighted_edit_distance_predicted.append(weighted_edit_distance)
				actual.append(database_name)
	edit_distance_accuracy = partial_acc(edit_distance_predicted, actual)
	weighted_edit_distance_accuracy = partial_acc(weighted_edit_distance_predicted, actual)
	print("edit_distance_accuracy " + str(edit_distance_accuracy))
	print("weighted_edit_distance_accuracy " + str(weighted_edit_distance_accuracy))






