# src/utils.py

import logging
import re
from typing import List
import time
import streamlit as st
from datetime import datetime
import os
import json

from src.constants import LOG_FILE_PATH, LOGO_URL_SMALL, LOGO_URL_LARGE, URL_WEB, RAGAS_FILE_PATH
from src.constantesWeb import ESTILOS_INICIO, ESTILOS



def setup_logging() -> None:

    current_date = datetime.now().strftime("%Y-%m-%d")

    ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python

    ruta_log = ruta_actual + LOG_FILE_PATH

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}.log")

    logging.basicConfig(
        filename=log_file_path,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        encoding="utf-8"
    )

def write_eval_to_json(user_input: str, response: str, retrieved_contexts: list, reference: str) -> None:
    """
    Escribe una entrada en un archivo JSON con los datos proporcionados.
    
    :param user_input: Pregunta del usuario.
    :param response: Respuesta generada.
    :param retrieved_contexts: Lista de contextos recuperados.
    :param reference: Texto de referencia.
    """

    # Crear el nombre del archivo con la fecha
    ragas_file_path = nombre_fichero_ragas_eval()

    # Si el archivo existe, cargarlo; de lo contrario, iniciar una lista vacía
    if os.path.isfile(ragas_file_path):
        with open(ragas_file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    # Crear el diccionario con los datos
    entry = {
        "user_input": user_input,
        "reference": reference,
        "response": response,
        "retrieved_contexts": retrieved_contexts,
    }
    
    # Agregar la nueva entrada
    data.append(entry)
    
    # Escribir los datos actualizados en el archivo
    with open(ragas_file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def nombre_fichero_ragas_eval() -> str:
    """
    Devuelve el nombre del fichero de evaluación donde se alacenarán los datos.
    """
    current_date = datetime.now().strftime("%Y_%m_%d")

    # Crear el nombre del archivo con la fecha
    ragas_file_path = os.path.join(RAGAS_FILE_PATH, f"{current_date}_ragas.json")
    
    return ragas_file_path

def clean_text(text: str) -> str:
    # Remove hyphens at line breaks (e.g., 'exam-\nple' -> 'example')
    text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

    # Replace newlines within sentences with spaces
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n+", "\n", text)

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    cleaned_text = text.strip()
    logging.info("Texto limpiado.")
    return cleaned_text


def chunk_text(text: str, chunk_size: int, overlap: int = 100) -> List[str]:
    # Clean the text before chunking
    text = clean_text(text)
    logging.info("Texto preparado para trocear.")

    # Tokenize the text into words
    tokens = text.split(" ")

    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]
        chunk_text = " ".join(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap  # Move back by 'overlap' tokens

    logging.info(
        f"Texto separado en {len(chunks)} partes con tamaño de parte {chunk_size} and overlap {overlap}."
    )
    return chunks

def stream_data(texto):
    for word in texto.split(" "):
        yield word + " "
        time.sleep(0.04)


################### HTML y Estilos ###################

def apply_cab_chat(title) -> None:
    st.set_page_config(
        page_title=title, page_icon=LOGO_URL_SMALL
    )

    st.logo(
        LOGO_URL_LARGE,
        link=URL_WEB,
        icon_image=LOGO_URL_SMALL,
    )

def apply_cab(title) -> None:
    st.set_page_config(
        page_title=title, page_icon=LOGO_URL_SMALL, layout="wide"
    )

    st.logo(
        LOGO_URL_LARGE,
        link=URL_WEB,
        icon_image=LOGO_URL_SMALL,
    )

def apply_custom_css(logger) -> None:
    """Applies custom CSS styling to the Streamlit page and sidebar."""
    st.markdown(
        ESTILOS_INICIO,
        unsafe_allow_html=True,
    )
    logger.info("Css aplicado.")


def apply_custom_css_chat(logger) -> None:
    """Applies custom CSS styling to the Streamlit page and sidebar."""
    st.markdown(
        ESTILOS,
        unsafe_allow_html=True,
    )
    logger.info("Css aplicado.")


def display_logo(logger, logo_path: str) -> None:
    """Displays the logo in the sidebar or a placeholder if the logo is not found.

    Args:
        logo_path (str): The file path for the logo image.
    """
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo displayed.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo not found, displaying placeholder.")

def display_sidebar_content(logger) -> None:
    st.sidebar.divider()
    # Sidebar headers and footer
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>AyudaMe.ai</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Tu chatbot conversacional para búsqueda de ayudas públicas del Gobierno de España</h4>",
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    st.sidebar.markdown("**Origen de los datos:**", unsafe_allow_html=True)
    # st.sidebar.image("images/iconoWebEstado.ico", width=50)
    st.sidebar.markdown("Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas. <a href='https://www.pap.hacienda.gob.es/bdnstrans/GE/es/inicio'>🔗</a>", unsafe_allow_html=True)
    st.sidebar.markdown("***Intervención General de la Administración del Estado***", unsafe_allow_html=True)
    st.sidebar.markdown("<a href='Aviso_legal'>Página aviso legal</a>", unsafe_allow_html=True)

    # Footer text
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2024 Desi Martí
        </div>
        """,
        unsafe_allow_html=True,
    )

    logger.info("Mostrar barra lateral.")