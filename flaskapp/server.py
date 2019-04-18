from flask import Flask, render_template, request
import json
import numpy as np
import sklearn
import pickle
import requests
from keras import backend as K


##LSTM imports
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import text_to_word_sequence
from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Activation, Dropout, Input, Flatten, Embedding, LSTM
from keras.utils import np_utils
from keras.utils import to_categorical
from sklearn import preprocessing

# edit distance imports
from fuzzywuzzy import fuzz
from weighted_levenshtein import lev, osa, dam_lev

app = Flask(__name__)
with open("receipt_outputs/ex_output.json") as in_json:
	receipt_titles = json.load(in_json)


@app.route("/")
def reload():
	with open("receipt_outputs/ex_output.json") as in_json:
		receipt_titles = json.load(in_json)
	return render_template("ui.html", receipt_titles=receipt_titles)

@app.route("/retrieve", methods=['POST', 'GET'])
def retrieve():
	searched = request.form['searched_receipt']
	lstm_output, edit_distance_output = predict(searched, True)
	print('lstm_output = ', lstm_output)
	print('edit_distance_output = ', edit_distance_output)
	return render_template("ui.html", manual_search=True,
										receipt_titles=searched,
										lstm_output=lstm_output,
										edit_distance_output=edit_distance_output)

@app.route("/index")
def load_blank():
	return render_template("index.html")

@app.route('/uploader', methods = ['POST'])
def upload_file():
	file = request.files['receipt']
	if file.filename != '':
		data = file.read()
		output = requests.get("http://127.0.0.1:8080/get-receipt-info", data=data).content.decode("utf-8")
		json_data = output
		with open('data.json', 'w') as outfile:
			json.dump(json_data, outfile)
		output = output.split("],")
		return render_template("index.html", text=output)



@app.route("/predict", methods=['POST', 'GET'])
def predict(searched=None, internal_call=False):
	'''
	important variables:
	tokenizer - tokenizer for tokenizing text
	lstm_model - trained lstm model
	le - label encoder to decode output
	'''

	# lstm
	K.clear_session()
	lstm_path = "../approaches/LSTM/"
	with open(lstm_path+"pickled/tokenizer.pickle", 'rb') as handle:
		tokenizer = pickle.load(handle)
	lstm_model = load_model(lstm_path+"models/lstm_50k_epochs_5.h5")
	le = preprocessing.LabelEncoder()
	le.classes_ = np.load(lstm_path+"pickled/labelencoder_classes.npy")
	tokenizer.oov_token = None

	# edit distance
	with open('../approaches/edit_distance/cleaned_bucket_data.json', encoding="ASCII") as f:
		data = json.load(f)

	## if internal call ##
	if internal_call:
		# lstm
		encoded_x = tokenizer.texts_to_sequences([searched])
		padded = pad_sequences(encoded_x, 25)
		lstm_preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in lstm_preds]
		lstm_preds = le.inverse_transform(pred_labels)

		#=========================================================

		# edit distance

		# find first letter of every word in the string
		words = searched.split()
		letters = [word[0] for word in words]

		# get corresponding buckets 
		first_letter = searched[0]
		products = []
		for bucket in data:
			if bucket[0][0].lower() == first_letter.lower():
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
			distance = osa(searched.lower(), line.lower(), insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs)
			if closest_distance is None or distance < closest_distance:
				closest_distance = distance
				closest_string = line.lower()

		edit_distance_pred = closest_string
		return (lstm_preds, edit_distance_pred)
	else:
		encoded_x = tokenizer.texts_to_sequences(receipt_titles)
		padded = pad_sequences(encoded_x, 25)
		lstm_preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in lstm_preds]
		lstm_preds = le.inverse_transform(pred_labels)

		#=========================================================

		# edit distance
		edit_distance_preds = []
		for title in receipt_titles:
			
			# find first letter of every word in the string
			words = title.split()
			letters = [word[0] for word in words]

			# get corresponding buckets 
			first_letter = title[0]
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
				distance = osa(title.lower(), line.lower(), insert_costs=insert_costs, transpose_costs=transpose_costs, delete_costs=delete_costs)
				if closest_distance is None or distance < closest_distance:
					closest_distance = distance
					closest_string = line.lower()

			edit_distance_preds.append(closest_string)

		return render_template("ui.html", manual_search=False,
											receipt_titles=receipt_titles,
											lstm_output=lstm_preds,
											edit_distance_output=edit_distance_preds)






if __name__ == "__main__":
	app.run(debug=True, port=5000)