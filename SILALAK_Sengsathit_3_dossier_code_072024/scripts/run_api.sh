#!/bin/bash

# Arrêt de l'instance du Dashboard
pid=$(sudo netstat -tulpn | grep :5000 | awk '{print $7}' | cut -d/ -f1)
if [ -n "$pid" ]; then
    sudo kill -9 $pid
fi

# Lancer l'API en arrière-plan avec nohup
cd /home/ubuntu/OCR_data_scientist_projet_07_livrables/
source .venv/bin/activate
nohup python SILALAK_Sengsathit_3_dossier_code_072024/scripts/api.py > nohup.out 2> nohup.err < /dev/null &
