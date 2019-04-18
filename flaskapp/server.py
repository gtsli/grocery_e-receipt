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



@app.route("/")
def reload():
	return render_template("index.html")


@app.route("/retrieve", methods=['POST', 'GET'])
def retrieve():
	searched = request.form['searched_receipt']
	output = lstm_output(searched)
	print ('output = ', output)
	return render_template("index.html", manual_search=True,
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
		loaded = json.loads(output)
		with open('data.json', 'w') as outfile:
			json.dump(loaded, outfile)
		return render_template("index.html", text=loaded)



# @app.route("/LSTM", methods=['POST', 'GET'])
def lstm_output(input_titles):
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

	encoded_x = tokenizer.texts_to_sequences(input_titles)
	padded = pad_sequences(encoded_x, 25)
	preds = lstm_model.predict(padded)
	pred_labels = [[np.argmax(x)] for x in preds]
	preds = le.inverse_transform(pred_labels)

	return preds






if __name__ == "__main__":
	app.run(debug=True, port=5000)