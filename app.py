from flask import Flask, jsonify, request, render_template
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle
import os
from helpers import gen_acc_mappings, convert_text_to_seq, get_acc_code, get_acc_descr, get_pred_confidence

global model, graph
model = tf.keras.models.load_model('model/model 2018-03-09 1424.h5')
graph = tf.get_default_graph()

with open('data/misc/tokenizer.pickle', 'rb') as f:
    tokenizer = pickle.load(f)

acc_mapping_df = pd.read_feather('data/misc/acc_mapping.feather')

model_config = model.get_config()
descr_input_layer = list(filter(lambda d: d['name'] == 'descr_input', model_config['layers']))[0]
max_sequence_length = descr_input_layer['config']['batch_input_shape'][1]
vendor_input_layer = list(filter(lambda d: d['name'] == 'vendor_input', model_config['layers']))[0]
max_vendor_length = vendor_input_layer['config']['batch_input_shape'][1]

acc_indices, acc_index_to_code, acc_index_to_descr = gen_acc_mappings(acc_mapping_df)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    #dat = request.get_json()
    dat = request.form
    
    # preprocess data
    header_descr = dat['headerDescription']
    line_descr = dat['lineDescription']
    full_descr = header_descr + ' ' + line_descr
    full_descr = convert_text_to_seq(tokenizer, [full_descr], max_sequence_length)
    vendor_name = dat['vendorName']
    vendor_name = convert_text_to_seq(tokenizer, [vendor_name], max_vendor_length)
    try:
        payment_voucher_amt = np.reshape(float(dat['amount']), (1,1))
    except ValueError as e:
        return jsonify({
            'Account Code': '',
            'Account Description': '',
            'Prediction Confidence': '',
            'Error': 'Can\'t convert amt \'{}\' to float'.format(dat['amount'])
        })
    except Exception as e:
        return jsonify({
            'Account Code': '',
            'Account Description': '',
            'Prediction Confidence': '',
            'Error': 'Unhandled exception:\n{}'.format(e)
        })
    
    # need graph.as_default() to avoid "Tensor is not an element of this graph" issue when serving on Flask
    with graph.as_default():
        pred = model.predict([full_descr, vendor_name, payment_voucher_amt])[0]
    
    pred_acc_code = get_acc_code(acc_index_to_code, pred)
    pred_acc_descr = get_acc_descr(acc_index_to_descr, pred)
    pred_confidence = get_pred_confidence(pred)
    
    return jsonify({
        'Account Code': pred_acc_code,
        'Account Description': pred_acc_descr,
        'Prediction Confidence': '{}%'.format(round(pred_confidence * 100, 2))
    })

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', False))