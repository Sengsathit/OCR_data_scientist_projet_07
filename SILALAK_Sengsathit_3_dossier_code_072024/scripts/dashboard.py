import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st

# Obtenez le répertoire courant du script
current_directory = os.path.dirname(os.path.abspath(__file__))

st.title('PRÊTS À DÉPENSER : credits scoring')