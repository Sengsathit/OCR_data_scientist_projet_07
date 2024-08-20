import pytest
from unittest.mock import patch, Mock
import os
import sys

# Obtenir le répertoire du fichier actuel 
current_file_directory = os.path.dirname(__file__)

# Créer un chemin relatif vers le dossier 'Scripts'
scripts_directory = os.path.abspath(os.path.join(current_file_directory, '..', 'scripts'))

# Insérer ce chemin au début de sys.path
sys.path.insert(0, scripts_directory)

def test_pass():
    assert True