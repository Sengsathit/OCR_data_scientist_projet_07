#!/bin/bash

# Arrêt de l'instance du Dashboard
lsof -i tcp:8501 | awk '/8501/{print $2}' | xargs kill

# Lancer le dashboard en arrière-plan avec nohup
cd /home/ubuntu/OCR_data_scientist_projet_07
source .venv/bin/activate
cd SILALAK_Sengsathit_3_dossier_code_072024/scripts
nohup streamlit run dashboard.py > dashboard.out 2> dashboard.err < /dev/null &