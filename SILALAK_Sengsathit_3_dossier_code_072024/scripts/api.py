import os
import pandas as pd
import shap
import pickle
import mlflow
import mlflow.sklearn
from flask import Flask, jsonify, request

app = Flask(__name__)

# Répertoire actuel du fichier api.py
current_directory = os.path.dirname(os.path.abspath(__file__))

# Chargement du modèle
mlflow.set_tracking_uri("http://13.38.185.52:8080")
model_uri = 'runs:/df3aafe9939d4db18b8bea11bb384589/xgboost_classifier_best_model'
model = mlflow.sklearn.load_model(model_uri)

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

# Initialisation de l'explainer SHAP
explainer = shap.TreeExplainer(model)

# Seuil de décision optimal
threshold = 0.54

@app.route("/scoring", methods=['POST'])
def scoring():

    data = request.json
    sk_id_curr = data['sk_id_curr']

    # Sélectionner les caractéristiques en fonction de l'ID du client
    sample = df[df['SK_ID_CURR'] == sk_id_curr]
    sample_features = sample.drop(columns=['SK_ID_CURR', 'TARGET'])
    sample = imputer.transform(sample_features)
    sample = scaler.transform(sample)
    
    # Prédire 
    prediction = model.predict_proba(sample)
    probability = float(prediction[0][1])

    # Calculer les valeurs SHAP pour le client donné
    shap_values = explainer.shap_values(sample)[0]
    
    # Créer les listes des importances de caractéristiques positives et négatives
    feature_importances_positive = [
        {'feature_name': feature_name, 'shap_value': float(shap_value)}
        for feature_name, shap_value in zip(sample_features.columns, shap_values)
        if shap_value > 0
    ]
    feature_importances_negative = [
        {'feature_name': feature_name, 'shap_value': float(shap_value)}
        for feature_name, shap_value in zip(sample_features.columns, shap_values)
        if shap_value < 0
    ]

    # Retourner le résultat du scoring avec les SHAP positifs et négatifs
    return jsonify({
        'sk_id_curr': sk_id_curr,
        'threshold': threshold,
        'probability': probability,
        'feature_importances_positive': feature_importances_positive,
        'feature_importances_negative': feature_importances_negative
    })

if __name__ == "__main__":
    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=int(port))