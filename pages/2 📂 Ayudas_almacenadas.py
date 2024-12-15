import logging
import os
import time

import streamlit as st
#from PyPDF2 import PdfReader

from src.embeddings import get_embedding_model
from src.searchchromadb import get_all_documents, cargarDocumento
from src.utils import setup_logging, apply_cab, apply_custom_css, display_sidebar_content
from src.constantesWeb import ESTILOS

import json

# Initialize logger
setup_logging()  # Set up centralized logging configuration
logger = logging.getLogger(__name__)

apply_cab("HelpMe.ai - Listado ayudas almacenadas")
apply_custom_css(logger)

def leer_yaml_como_string(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            datos = file.read()
        return datos
    except FileNotFoundError:
        print(f"El archivo en la ruta {file_path} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def render_upload_page() -> None:
    """
    Renders the document upload page for users to upload and manage PDFs.
    Shows only the documents that are present in the OpenSearch index.
    """

    st.title("Ayudas almacenadas en el sistema")
    # Placeholder for the loading spinner at the top
    model_loading_placeholder = st.empty()

    # Display the loading spinner at the top for loading the embedding model
    if "embedding_models_loaded" not in st.session_state:
        with model_loading_placeholder:
            with st.spinner("Loading models for document processing..."):
                get_embedding_model()
                st.session_state["embedding_models_loaded"] = True
        logger.info("Modelo de embeddings cargado.")
        model_loading_placeholder.empty()  # Clear the placeholder after loading

    UPLOAD_DIR = "uploaded_files"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Initialize or clear the documents list in session state
    st.session_state["documents"] = []

    #Obtenemos los documentos de chromadb
    document_names = get_all_documents()
    
    logger.info(document_names)
    logger.info("Obtenidos nombres de documentos desde Chromadb.")

    if document_names.get('documents'):  # Verifica que 'documents' no sea None o esté vacío
        st.subheader(f"Actualmente tenemos :blue[{len(document_names['ids'])}] ayudas almacendas :sunglasses:")
        st.caption("Puedes ver el detalle almacenado pinchando en cada ayuda")
        for id_, document, metadata in zip(document_names['ids'], document_names['documents'], document_names['metadatas']):
            logger.info(f"ID: {id_}, Document: {len(document)}, Metadata: {metadata}")
            st.session_state["documents"].append(
                {"filename": id_, "content": document, "metadata": metadata, "file_path": None}
            )
    else:
        print("No documents to process.")

    if "deleted_file" in st.session_state:
        st.success(
            f"El fichero '{st.session_state['deleted_file']}' fué correctamente borrado."
        )
        del st.session_state["deleted_file"]

    if st.session_state["documents"]:
        for idx, doc in enumerate(st.session_state["documents"], 1):
            with st.expander(f"Ayuda {doc['filename']}", expanded=False):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown("**Documento**")
                    st.code(doc['content'], language="yaml", line_numbers=False, wrap_lines=True)
                with col2:
                    st.markdown("**Metadatos**")
                    # st.json(doc['metadata'])
                    st.code(doc['metadata'], language="json", line_numbers=False, wrap_lines=True)

if __name__ == "__main__":
    if "documents" not in st.session_state:
        st.session_state["documents"] = []
    render_upload_page()
    display_sidebar_content(logger)
