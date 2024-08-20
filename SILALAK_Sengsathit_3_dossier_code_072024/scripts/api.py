import os
import joblib
import pandas as pd
import shap
from flask import Flask, jsonify, request

app = Flask(__name__)

# Récupérez le répertoire actuel du fichier api.py
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.route("/predict", methods=['GET'])
def predict():

    return jsonify({
        'message': 'LLL !' 
    })

@app.route("/test", methods=['GET'])
def test():
    return jsonify({
        'message': 'This is the test route!' 
    })

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=int(port))