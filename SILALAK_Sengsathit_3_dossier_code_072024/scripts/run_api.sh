#!/bin/bash

# Arrêt de l'instance de l'API
lsof -i tcp:8501 | awk '/8501/{print $2}' | xargs kill

# Lancer l'API en arrière-plan avec nohup
cd /home/ubuntu/OCR_data_scientist_projet_07_livrables/
source .venv/bin/activate
cd SILALAK_Sengsathit_3_dossier_code_072024/scripts/
nohup python SILALAK_Sengsathit_3_dossier_code_072024/scripts/api.py > nohup.out 2> nohup.err < /dev/null &
