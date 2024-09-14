import sys
import os
import pandas as pd

# Ajouter le chemin vers le dossier contenant api.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from api import load_model, load_pickle # type: ignore

# Tester le chargement du model
def test_load_model():
    model_uri = 'runs:/df3aafe9939d4db18b8bea11bb384589/xgboost_classifier_best_model'
    model = load_model(model_uri)
    assert model is not None

# Tester le chargement de l'imputer
def test_load_imputer():
    imputer_path = os.path.join(os.path.dirname(__file__), "..", "tools", "imputer.pkl")
    imputer = load_pickle(imputer_path)
    assert imputer is not None

# Tester le chargement du scaler
def test_load_scaler():
    imputer_path = os.path.join(os.path.dirname(__file__), "..", "tools", "scaler.pkl")
    imputer = load_pickle(imputer_path)
    assert imputer is not None