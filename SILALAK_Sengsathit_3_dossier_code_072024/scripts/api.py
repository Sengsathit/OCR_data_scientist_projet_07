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

# Fonction pour charger le modèle MLflow
def load_model(model_uri):
    mlflow.set_tracking_uri("http://13.38.185.52:8080")
    return mlflow.sklearn.load_model(model_uri)

# Fonction pour charger un fichier pickle
def load_pickle(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

# Fonction pour charger le dataset
def load_dataset(csv_path):
    return pd.read_csv(csv_path)

# Fonction pour initialiser l'explainer SHAP
def initialize_explainer(model):
    return shap.TreeExplainer(model)

# Fonction de prédiction avec SHAP
def predict_and_explain(model, explainer, imputer, scaler, df, sk_id_curr):
    # Sélectionner les caractéristiques en fonction de l'ID du client
    sample = df[df['SK_ID_CURR'] == sk_id_curr]
    if sample.empty:
        return None, None, None  # Gestion du cas où l'ID est invalide
    sample_features = sample.drop(columns=['SK_ID_CURR', 'TARGET'])
    sample = imputer.transform(sample_features)
    sample = scaler.transform(sample)
    
    # Prédire la probabilité
    prediction = model.predict_proba(sample)
    probability = float(prediction[0][1])

    # Calculer les valeurs SHAP
    shap_values_local = explainer.shap_values(sample)[0]
    
    # Créer les listes des importances de caractéristiques positives et négatives
    feature_importances_positive = [
        {'feature_name': feature_name, 'shap_value': float(shap_value)}
        for feature_name, shap_value in zip(sample_features.columns, shap_values_local)
        if shap_value > 0
    ]
    feature_importances_negative = [
        {'feature_name': feature_name, 'shap_value': float(shap_value)}
        for feature_name, shap_value in zip(sample_features.columns, shap_values_local)
        if shap_value < 0
    ]

    return probability, feature_importances_positive, feature_importances_negative

# Fonction pour calculer les importances globales des features
def calculate_global_importances(explainer, imputer, scaler, df):
    # Appliquer l'imputation et le scaling sur toutes les données sauf 'SK_ID_CURR' et 'TARGET'
    X = df.drop(columns=['SK_ID_CURR', 'TARGET'])
    X_imputed = imputer.transform(X)
    X_scaled = scaler.transform(X_imputed)

    # Calculer les valeurs SHAP pour toutes les données
    shap_values_global = explainer.shap_values(X_scaled)[0]

    # Calculer les importances globales (moyenne des valeurs absolues des SHAP globales)
    return [
        {'feature_name': feature_name, 'shap_value': float(abs(shap_value_global).mean())}
        for feature_name, shap_value_global in zip(X.columns, shap_values_global.T)
    ]

@app.route("/scoring", methods=['POST'])
def scoring():
    data = request.json
    sk_id_curr = data['sk_id_curr']
    
    # Vérifier si sk_id_curr est fourni et s'il est numérique
    if sk_id_curr is None or not isinstance(sk_id_curr, (int, float)):
        return jsonify({'error': 'sk_id_curr must be a numeric value'}), 400
    
    # Prédiction
    probability, feature_importances_positive, feature_importances_negative = predict_and_explain(
        model, 
        explainer, 
        imputer, 
        scaler, 
        df, 
        sk_id_curr
    )
    
    # Vérifier si la prédiction a fonctionné
    if probability is None:
        return jsonify({'error': 'Invalid sk_id_curr'}), 400
    
    # Retourner la prédiction avec les valeurs SHAP
    return jsonify({
        'sk_id_curr': sk_id_curr,
        'threshold': threshold,
        'probability': probability,
        'feature_importances_positive': feature_importances_positive,
        'feature_importances_negative': feature_importances_negative,
        'feature_importances_global': feature_importances_global
    })

if __name__ == "__main__":
    # Initialisation des variables globales
    model_uri = 'runs:/8b9687c798834eb5b9e070154b21cf44/xgboost_classifier_best_model'
    model = load_model(model_uri)
    imputer = load_pickle(os.path.join(current_directory, "..", "tools", "imputer.pkl"))
    scaler = load_pickle(os.path.join(current_directory, "..", "tools", "scaler.pkl"))
    df = load_dataset(os.path.join(current_directory, "..", "data", "df_train_domain.csv"))
    explainer = initialize_explainer(model)
    threshold = 0.51
    feature_importances_global = calculate_global_importances(explainer, imputer, scaler, df)

    port = os.environ.get("PORT", 5000)
    app.run(debug=False, host="0.0.0.0", port=int(port))