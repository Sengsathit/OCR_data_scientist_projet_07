import os
import sys
import joblib
import pandas as pd
import pytest
from flask import Flask, jsonify, request

# Ajouter le chemin relatif du fichier api.py au sys.path pour pouvoir l'importer
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

def test_pass():
    assert True