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
	output = lstm_output(searched, True)
	print ('output = ', output)
	return render_template("ui.html", manual_search=True,
										receipt_titles=searched,
										lstm_output=output)

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



@app.route("/LSTM", methods=['POST', 'GET'])
def lstm_output(searched=None, internal_call=False):
	'''
	important variables:
	tokenizer - tokenizer for tokenizing text
	lstm_model - trained lstm model
	le - label encoder to decode output
	'''

	K.clear_session()
	lstm_path = "../approaches/LSTM/"
	with open(lstm_path+"pickled/tokenizer.pickle", 'rb') as handle:
	    tokenizer = pickle.load(handle)
	lstm_model = load_model(lstm_path+"models/lstm_50k_epochs_5.h5")
	le = preprocessing.LabelEncoder()
	le.classes_ = np.load(lstm_path+"pickled/labelencoder_classes.npy")
	tokenizer.oov_token = None

	## if internal call ##
	if internal_call:
		encoded_x = tokenizer.texts_to_sequences([searched])
		padded = pad_sequences(encoded_x, 25)
		preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in preds]
		preds = le.inverse_transform(pred_labels)
		return preds
	else:
		encoded_x = tokenizer.texts_to_sequences(receipt_titles)
		padded = pad_sequences(encoded_x, 25)
		preds = lstm_model.predict(padded)
		pred_labels = [[np.argmax(x)] for x in preds]
		preds = le.inverse_transform(pred_labels)

		return render_template("ui.html", manual_search=False,
											receipt_titles=receipt_titles,
											lstm_output=preds)






if __name__ == "__main__":
	app.run(debug=True, port=5000)