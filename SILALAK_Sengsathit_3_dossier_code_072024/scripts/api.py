import os
import joblib
import pandas as pd
import shap
import pickle
from flask import Flask, jsonify, request

app = Flask(__name__)

# Répertoire actuel du fichier api.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Chargement du modèle
model_path = os.path.join(current_directory, "..", "model_stable", "model.pkl")
model = joblib.load(model_path)

# Chargement de l'imputer et du scaler
imputer_path = os.path.join(current_directory, "..", "tools", "imputer.pkl")
scaler_path = os.path.join(current_directory, "..", "tools", "scaler.pkl")
with open(imputer_path, 'rb') as imputer:
    imputer = pickle.load(imputer)
with open(scaler_path, 'rb') as scaler:
    scaler = pickle.load(scaler)

# Chargement du dataset
csv_path = os.path.join(current_directory, "..", "data", "df_train_domain.csv")
df = pd.read_csv(csv_path)

@app.route("/scoring", methods=['POST'])
def scoring():

    data = request.json
    sk_id_curr = data['SK_ID_CURR']

    # Sélectionner les caractéristiques en fonction de l'ID du client
    sample = df[df['SK_ID_CURR'] == sk_id_curr]
    sample = sample.drop(columns=['SK_ID_CURR', 'TARGET'])
    sample = imputer.transform(sample)
    sample = scaler.transform(sample)
    
    # Prédire 
    prediction = model.predict_proba(sample)
    probability = prediction[0][1]

    # Calculer les valeurs SHAP pour le client donné

    # Retourner le résultat du scoring ainsi que les valeurs SHAP
    return jsonify({
        'sk_id_curr': sk_id_curr,
        'probability': probability, 
        'shap_values': [],
        'feature_names': [],
        'feature_values': []
    })

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=int(port))