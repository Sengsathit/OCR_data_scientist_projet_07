<img src="https://raw.githubusercontent.com/Sengsathit/OCR_data_scientist_assets/main/header_pret_a_depenser.png" alt="Alternative text" />

# Description
Ce projet a pour objectif de développer un modèle de scoring pour une entreprise financière afin d'évaluer la probabilité de remboursement d'un crédit par ses clients. Le modèle utilise des données variées (comportementales, financières, etc.) pour prédire le risque de défaut et classifier les demandes de crédit. Le modèle est optimisé pour minimiser les faux positifs, où un client à risque serait approuvé, tout en utilisant des techniques MLOps pour un déploiement continu et une gestion efficace du cycle de vie du modèle.

# Processus de déploiement

Le déploiement du projet est entièrement automatisé, assurant une mise à jour continue à la fois pour l'API et le Dashboard. Ce pipeline de déploiement permet de garantir un suivi en temps réel et un accès direct pour tester et visualiser les résultats.

- **API** : L'API permet de calculer la probabilité de défaut d'un client basé sur son identifiant unique. Elle est mise en production sur un serveur et est accessible via l'URL suivante : http://13.38.185.52:5000/scoring.
    - **Exemple de requête (POST)** : 
      ```json
      {
          "sk_id_curr": 100002
      }
      ```
    - La réponse contiendra la probabilité de défaut de remboursement du crédit, ainsi que les scores de contribution des features ayant le plus d'impact sur le modèle.

- **Dashboard** : Un dashboard interactif est également en ligne et permet de visualiser les prédictions en temps réel et l'analyse des features. Vous pouvez accéder au dashboard [ICI](http://13.38.185.52:8501) et tester le modèle sur les numéros client suivant : `100002` et `100040`


# Arborescence du projet

```bash
OCR_data_scientist_projet_07/
│
├── SILALAK_Sengsathit_1_notebook_data_preparation_072024.ipynb           # Notebook pour l'analyse exploratoire et le feature engineering
├── SILALAK_Sengsathit_2_notebook_modelisation_072024.ipynb               # Notebook pour la modélisation et la sélection du meilleur modèle
├── SILALAK_Sengsathit_3_dossier_code_072024/                             # Dossier relatif à l'API de scoring et au Dashboard
│    ├── data/                                                            # Dossier pour les datasets
│    │    └── df_train_domain.csv.zip                                     # Dataset pour simuler et évaluer un client par le modèle
│    ├── scripts/                                                         # Dossier des scripts de déploiement de l'API et du Dashboard
│    │    ├── api.py                                                      # Script de l'API (Flask)
│    │    ├── dashboard.py                                                # Script du Dashboard (Streamlit)
│    │    ├── run_api.sh                                                  # Script bash pour exécuter un instance de l'API sur le serveur
│    │    └── run_dashboard.py                                            # Script bash pour exécuter un instance du Dashboard sur le serveur
│    ├── tools/                                                           # Dossier contenant divers outils de manipulation de données
│    │    ├── imputer.pkl                                                 # Imputer utilisé lors du feature engineering
│    │    └── scaler.pkl                                                  # Scaler utilisé lors du feature engineering
│    └── unit_tests/                                                      # Dossier des tests unitaires
│         ├── unit_tests_api.py                                           # Tests unitaires de l'API
│         └── unit_tests_dashboard.py                                     # Tests unitaires du Dashboard
├── SILALAK_Sengsathit_4_Tableau_HTML_data_drift_evidently_072024.html    # Fichier de présentation des résultats de l'analyse du Data Drift
├── SILALAK_Sengsathit_5_presentation_072024.pdf                          # Slides de présentation de ce projet
├── requirements.txt                                                      # Fichier des dépendances
└── README.md                                                             # Ce fichier
```