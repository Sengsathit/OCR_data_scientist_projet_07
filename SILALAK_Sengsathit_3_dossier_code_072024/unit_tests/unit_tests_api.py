import sys
import os
import pandas as pd

# Ajouter le chemin vers le dossier contenant api.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from api import load_model, load_pickle, load_dataset

def test_load_model():
    model_uri = 'runs:/df3aafe9939d4db18b8bea11bb384589/xgboost_classifier_best_model'
    model = load_model(model_uri)
    assert model is not None

def test_load_pickle():
    imputer_path = os.path.join(os.path.dirname(__file__), "..", "tools", "imputer.pkl")
    imputer = load_pickle(imputer_path)
    assert imputer is not None

def test_load_dataset():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "df_train_domain.csv")
    df = load_dataset(csv_path)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty