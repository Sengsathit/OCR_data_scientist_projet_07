import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Url de l'API de scoring
api_url = 'http://13.38.185.52:5000/scoring'

# Header de la page
image_url = "https://raw.githubusercontent.com/Sengsathit/OCR_data_scientist_assets/main/header_pret_a_depenser.png"
st.image(image_url, use_column_width=True)
st.markdown(
    "<h1 style='text-align: center; font-size: 48px; margin-bottom: 40px;'>Évaluation du risque de crédit</h1>", 
    unsafe_allow_html=True
)

# Champ de saisie pour le numéro de client
client_id = st.text_input("Saisir le numéro de client")

# Bouton pour soumettre le numéro de client
if st.button("Vérifier le risque"):

    if client_id:      

        # Valeur de l'ID à envoyer à l'API
        payload = {"sk_id_curr": int(client_id)}  
        try:
            # Appel vers l'API + récupération de la réponse
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Récupérer les données JSON
                data = response.json()

                # Vérifier le dépassement du seuil de probabilité
                is_credit_default = data.get('probability') > data.get('threshold')

                # Affichage des informations récupérées
                st.markdown("***")
                st.subheader(f"Résultat de l'évaluation pour le client {data.get('sk_id_curr')}")
                st.write(f"Seuil de décision : {data.get('threshold') * 100:.2f} %")
                st.write(f"Probabilité de défaut de remboursement du client : {data.get('probability') * 100:.2f} %")

                if is_credit_default:
                    st.markdown(
                        """
                        <div style="background-color:#ffcccb;padding:10px;border-radius:5px;">
                        <strong style="color:#b30000;">Client à risque</strong>
                        </div>
                        """, unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
                        <strong style="color:#155724;">Client éligible pour un crédit</strong>
                        </div>
                        """, unsafe_allow_html=True
                    )

                # Trier les valeurs négatives du plus petit au plus grand
                sorted_negatives = sorted(data["feature_importances_negative"], key=lambda x: x["shap_value"])[:10]

                # Trier les valeurs positives du plus grand au plus petit
                sorted_positives = sorted(data["feature_importances_positive"], key=lambda x: x["shap_value"], reverse=True)[:10]

                # Affichage de la contribution des features
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader(f"Contribution des features")

                st.text("")

                # Affichage des contributions positives et négatives
                col1, col2 = st.columns(2)
                with col1:
                    st.write("##### Contributions positives")
                    for feature in sorted_positives:
                        st.write(f"{feature['feature_name']} : {feature['shap_value']:.6f}")
                with col2:
                    st.write("##### Contributions négatives")
                    for feature in sorted_negatives:
                        st.write(f"{feature['feature_name']} : {feature['shap_value']:.6f}")

            else:
                # Afficher l'erreur retournée par l'API
                st.error(f"L'API a retourné une erreur : {response}")

        except Exception as e:
            # Traiter les exceptions
            st.error(f"Erreur lors de l'appel API : {e}")
    else:

        st.warning("Veuillez saisir un numéro de client.")