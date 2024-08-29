import os
import joblib
import pandas as pd
import shap
from flask import Flask, jsonify, request

app = Flask(__name__)

# Récupérez le répertoire actuel du fichier api.py
current_directory = os.path.dirname(os.path.abspath(__file__))

@app.route("/scoring", methods=['GET'])
def scoring():

    # Effectuer la prédiction en fonction de l'ID du client

    # Calculer les valeurs SHAP pour le client donné

    # Retourner le résultat du scoring ainsi que les valeurs SHAP
    return jsonify({
        'probability': 0.5, 
        'shap_values': [],
        'feature_names': [],
        'feature_values': []
    })

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=int(port))