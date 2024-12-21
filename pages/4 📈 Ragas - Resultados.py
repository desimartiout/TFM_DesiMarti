import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
# st.set_page_config(page_title="Análisis de Evaluación de Ragas", layout="wide")
# st.title("Análisis de Evaluación de Ragas")

from config.ragas.ragas_config import RAGAS_FILE_PATH_RESULTS
from config.web.web_config import REPORT_CAB, REPORT_TITLE
from libs.utils import apply_cab_report

# Configuración de la página
apply_cab_report(REPORT_CAB)
st.title(REPORT_TITLE)

# Diccionario de descripciones
descripciones = {
    "faithfulness": "La fidelidad mide cuán precisa es la respuesta, es decir, si la respuesta es fiel al contexto proporcionado.",
    "semantic_similarity": "La similitud semántica mide cuán similar es el contenido semántico de la respuesta en comparación con el contexto.",
    "answer_relevancy": "La relevancia de la respuesta evalúa si la respuesta es pertinente para la pregunta planteada.",
    "context_precision": "La precisión del contexto mide cuán bien el contexto recuperado corresponde a la información necesaria para responder la pregunta."
}

# Directorio donde se encuentran los archivos CSV
csv_directory = RAGAS_FILE_PATH_RESULTS  # Cambia esto por el path de tu directorio

# Listar los archivos CSV en el directorio especificado
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

csv_files.sort(reverse=True)

# Si hay archivos csv, mostrar el desplegable para seleccionar uno
if csv_files:
    csv_file_name = st.selectbox("Selecciona un archivo csv", csv_files)

    # Si se selecciona un archivo, cargarlo
    if csv_file_name:
        csv_file_path = os.path.join(csv_directory, csv_file_name)
    
         # Intentar abrir el archivo CSV con diferentes encodings
        try:
            # Intentamos con utf-8
            df = pd.read_csv(csv_file_path, delimiter=";", encoding="utf-8")
        except UnicodeDecodeError:
            try:
                # Si falla, intentamos con ISO-8859-1 (latin1)
                df = pd.read_csv(csv_file_path, delimiter=";", encoding="ISO-8859-1")
            except Exception as e:
                st.error(f"Error al leer el archivo CSV: {e}")
                df = None
        
        
        # Si se cargó el archivo CSV correctamente
        if df is not None:
                       
            # df = df.drop(columns=['reference','context_recall','factual_correctness'])
            
            # Convertir las columnas numéricas a tipo numérico (si están como cadenas)
            numeric_cols = [
                "context_recall","factual_correctness", "faithfulness",
                "semantic_similarity", "answer_relevancy", "context_precision"
            ]
            
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a numérico, forzando NaN para valores inválidos
            
            # Reemplazar los NaN por 0 en las columnas numéricas
            df[numeric_cols] = df[numeric_cols].fillna(0)

            # Crear tabs para mostrar el CSV y el DataFrame
            tab1, tab2 = st.tabs(["Dataset del CSV", "Fichero CSV"])

            # Tab 1: Mostrar el dataset del CSV
            with tab1:
                st.write("### Dataset del archivo CSV")
                st.dataframe(df, use_container_width=True)

                # Análisis básico
                st.write("### Análisis descriptivo")
                st.write(df.describe())

                # Selección de columna para análisis visual
                if numeric_cols:
                    col = st.selectbox("Selecciona una columna para análisis visual:", numeric_cols)

                    # Mostrar la descripción si la columna seleccionada tiene una
                    if col in descripciones:
                        st.write(f"### Descripción de {col}")
                        st.write(descripciones[col])

                    # Histograma
                    st.write(f"#### Histograma de {col}")
                    fig, ax = plt.subplots()
                    sns.histplot(df[col], kde=True, ax=ax)
                    st.pyplot(fig)

                    # Boxplot
                    st.write(f"#### Boxplot de {col}")
                    fig, ax = plt.subplots()
                    sns.boxplot(x=df[col], ax=ax)
                    st.pyplot(fig)

                # Correlaciones entre las columnas numéricas
                st.write("### Matriz de correlación")
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm', ax=ax)
                st.pyplot(fig)

            # Tab 2: Mostrar el archivo CSV como texto
            with tab2:
                st.write("### Fichero CSV")
                with open(csv_file_path, "r", encoding="utf-8") as f:
                    st.code(f.read(), language="csv", line_numbers=True, wrap_lines=True)
else:
    st.write("No se han encontrado archivos csv en el directorio especificado.")
    st.toast(":x: No se han encontrado archivos csv en el directorio especificado.")

st.toast(f":white_check_mark: Información cargada correctamente")