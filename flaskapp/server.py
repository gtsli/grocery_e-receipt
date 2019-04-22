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

# gbdt imports
from feature_engineering import get_dataframe

'''
Global Variables
'''
manual_search=""
text=""
receipt_titles_global=""
lstm_output=""
edit_distance_output=""
gbdt_output=""
app = Flask(__name__)


@app.route("/")
def reload():
	return render_template("index.html")


@app.route("/retrieve", methods=['POST', 'GET'])
def retrieve():
	searched = request.form['searched_receipt']
	lstm_output_searched, edit_distance_output_searched, gbdt_output_searched = predict(searched, True, None)
	print('lstm_output = ', lstm_output)
	print('edit_distance_output = ', edit_distance_output)
	print('gbdt_output =', gbdt_output)
	return render_template("index.html", manual_search=True,
										lstm_output_searched=lstm_output_searched,
						   				gbdt_output_searched=gbdt_output_searched,
										edit_distance_output_searched=edit_distance_output_searched,
										text=text,
										receipt_titles=receipt_titles_global,
										lstm_output=lstm_output,
										edit_distance_output=edit_distance_output,
						   				gbdt_output=gbdt_output)

@app.route("/index")
def load_blank():
	return render_template("index.html")

@app.route('/uploader', methods = ['POST'])
def upload_file():
	file = request.files['receipt']
	if file.filename != '':
		data = file.read()
		output = requests.get("http://127.0.0.1:8080/get-receipt-info", data=data).content.decode("utf-8")
		loaded = json.loads(output)
		return predict(searched=None, internal_call=False, receipt=loaded, receipt_titles=loaded["items"])
		# return render_template("index.html", text=loaded)




@app.route("/predict", methods=['POST', 'GET'])
def predict(searched=None, internal_call=False, receipt=None, receipt_titles=None):
	'''
	important variables:
	tokenizer - tokenizer for tokenizing text
	lstm_model - trained lstm model
	le - label encoder to decode output
	'''

	# lstm
	K.clear_session()
	lstm_path = "../approaches/LSTM/"
	with open(lstm_path+"pickled/tokenizer_300k_1epoch.pickle", 'rb') as handle:
		tokenizer = pickle.load(handle)
	lstm_model = load_model(lstm_path+"models/lstm_300k_epochs_1.h5")
	le = preprocessing.LabelEncoder()
	le.classes_ = np.load(lstm_path+"pickled/labelencoder_classes_300k_1epoch.npy")
	tokenizer.oov_token = None


	# edit distance
	with open('../approaches/edit_distance/cleaned_bucket_data.json', encoding="ASCII") as f:
		data = json.load(f)

	# gbdt
	gbdt_path = "../approaches/gbdt/"
	gbdt_model = pickle.load(open(gbdt_path+"models/gbdt_model.sav", "rb"))
	gbdt_le = preprocessing.LabelEncoder()
	gbdt_le.classes_ = np.load(gbdt_path+"pickled/labelencoder_gbdt_classes.npy")

	## if internal call ##
	if internal_call:
		# lstm
		encoded_x = tokenizer.texts_to_sequences([searched])
		padded = pad_sequences(encoded_x, 25)
		lstm_preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in lstm_preds]
		lstm_preds = le.inverse_transform(pred_labels)

		# gbdt
		df = get_dataframe([searched.upper()])
		gbdt_preds = gbdt_model.predict(df.drop(columns=['x', 'y'], axis=1))
		gbdt_preds = gbdt_le.inverse_transform(gbdt_preds)[0]

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
		return (lstm_preds, edit_distance_pred, gbdt_preds)
	else:
		print ('receipt titles = ', receipt_titles)
		encoded_x = tokenizer.texts_to_sequences(receipt_titles)
		padded = pad_sequences(encoded_x, 25)
		lstm_preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in lstm_preds]
		lstm_preds = le.inverse_transform(pred_labels)

		# gbdt
		titles = []
		for title in receipt_titles:
			titles.append(title.upper())
		df = get_dataframe(titles)
		gbdt_preds = gbdt_model.predict(df.drop(columns=['x', 'y'], axis=1))
		gbdt_preds = gbdt_le.inverse_transform(gbdt_preds)

		#=========================================================

		# edit distance
		edit_distance_preds = []
		for title in receipt_titles[:]:

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

		global manual_search
		global text
		global receipt_titles_global
		global lstm_output
		global edit_distance_output
		global gbdt_output

		manual_search=False
		text=receipt
		receipt_titles_global=receipt_titles
		lstm_output=lstm_preds
		edit_distance_output=edit_distance_preds
		gbdt_output = gbdt_preds
		print("edit_distance_output " + str(edit_distance_output))


		return render_template("index.html", manual_search=False,
											text=receipt,
											receipt_titles=receipt_titles,
											lstm_output=lstm_preds,
											edit_distance_output=edit_distance_preds,
							   				gbdt_output=gbdt_preds)






if __name__ == "__main__":
	app.run(debug=True, port=5000)