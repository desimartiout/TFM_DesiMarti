import json
import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
# st.set_page_config(page_title="Análisis de Evaluación de Ragas", layout="wide")
# st.title("Análisis de Evaluación de Ragas")

from config.global_config import RAGAS_FILE_PATH
from config.web.web_config import DATASET_CAB, DATASET_TITLE
from libs.utils import apply_cab_report

# Configuración de la página
apply_cab_report(DATASET_CAB)
st.title(DATASET_TITLE)

# Directorio donde se encuentran los archivos JSON
json_directory = RAGAS_FILE_PATH  # Cambia esto por el path de tu directorio

# Listar los archivos JSON en el directorio especificado que tienen cierto tamaño
# json_files = [f for f in os.listdir(json_directory) if f.endswith('.json')]
json_files = [
    f for f in os.listdir(json_directory)
    if f.endswith('.json') and os.path.getsize(os.path.join(json_directory, f)) > 10
]

#Ordenamos descendentemente
json_files.sort(reverse=True)

# Si hay archivos JSON, mostrar el desplegable para seleccionar uno
if json_files:

    json_file_name = st.selectbox("Selecciona un archivo JSON", json_files)

    # Si se selecciona un archivo, cargarlo
    if json_file_name:
        json_file_path = os.path.join(json_directory, json_file_name)
        
        # Cargar el archivo JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Convertir el JSON a DataFrame, si es posible
        if isinstance(json_data, list):
            df_json = pd.DataFrame(json_data)
        elif isinstance(json_data, dict):
            df_json = pd.DataFrame([json_data])
        else:
            df_json = pd.DataFrame()

        # Crear tabs para mostrar el JSON y el DataFrame
        tab1, tab2 = st.tabs(["Dataset del JSON", "Fichero JSON"])

        # Tab 1: Mostrar el dataset del JSON
        with tab1:
            st.write("### Dataset del archivo JSON")
            st.dataframe(df_json, use_container_width=True)

        # Tab 2: Mostrar el archivo JSON
        with tab2:
            st.write("### Fichero JSON")
            st.json(json_data)
else:
    st.write("No se han encontrado archivos JSON en el directorio especificado.")

st.toast(f":white_check_mark: Información cargada correctamente")
