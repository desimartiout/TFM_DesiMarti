import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
# st.set_page_config(page_title="Análisis de Evaluación de Ragas", layout="wide")
# st.title("Análisis de Evaluación de Ragas")

from config.web_config import REPORT_CAB, REPORT_TITLE
from src.utils import apply_cab_report

# Configuración de la página
apply_cab_report(REPORT_CAB)
st.title(REPORT_TITLE)

# Cargar archivo CSV
st.sidebar.header("Cargar Archivo")
uploaded_file = st.sidebar.file_uploader("fichero evaluación ragas CSV", type=["csv"])

if uploaded_file:
    # Leer archivo CSV
    df = pd.read_csv(uploaded_file, delimiter=";")

    df = df.drop(columns=['reference','context_recall','factual_correctness'])
    
    # Convertir las columnas numéricas a tipo numérico (si están como cadenas)
    # numeric_cols = [
    #     "context_recall", "factual_correctness", "faithfulness",
    #     "semantic_similarity", "answer_relevancy", "context_precision"
    # ]

    numeric_cols = [
        "faithfulness",
        "semantic_similarity", "answer_relevancy", "context_precision"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    st.write("### Dataset")
    st.dataframe(df, use_container_width=True)

    # Análisis básico
    st.write("### Análisis descriptivo")
    st.write(df.describe())

    # Selección de columna para análisis visual
    if numeric_cols:
        col = st.selectbox("Selecciona una columna para análisis visual:", numeric_cols)

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

else:
    st.info("Sube un archivo CSV desde el menú lateral para comenzar.")
