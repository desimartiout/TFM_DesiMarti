import logging
import os

import streamlit as st

# from src.embeddings import get_embedding_model
from libs.searchchromadb import get_all_documents, cargarDocumento
from libs.utils import setup_logging, apply_cab, apply_custom_css, display_sidebar_content

from libs.faiss_utils import obtener_todos_documentos, realizar_consulta

from config.global_config import BD_VECTORIAL_CHROMADB, BD_VECTORIAL_FAISS, TIPO_BD_VECTORIAL
from config.web.web_config import CAB_AYUDAS_ALMACENADAS

import json

# Initialize logger
setup_logging()  # Set up centralized logging configuration
logger = logging.getLogger(__name__)

apply_cab(CAB_AYUDAS_ALMACENADAS)
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

    UPLOAD_DIR = "uploaded_files"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Initialize or clear the documents list in session state
    st.session_state["documents"] = []

    if (TIPO_BD_VECTORIAL==BD_VECTORIAL_CHROMADB):
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
    else:
        #FAISS
        document_names= obtener_todos_documentos()
        num_documentos = len(document_names)
        logger.info(document_names)
        logger.info("Obtenidos nombres de documentos desde FAISS.")

        if len(document_names)!=0:  # Verifica que 'documents' no sea None o esté vacío
            st.subheader(f"Actualmente tenemos :blue[{num_documentos}] ayudas :sunglasses:")
            st.caption("Puedes ver el detalle almacenado pinchando en cada ayuda")
            for document in document_names:
                st.session_state["documents"].append(document)
        else:
            print("No documents to process.")
    
        logger.info(f"State: {st.session_state['documents']}")
        logger.info(f"State: {len(st.session_state['documents'])}")
        if st.session_state["documents"]:
            i=0
            for doc in st.session_state["documents"]:    
                with st.expander(f"Ayuda {i}", expanded=False):
                    st.markdown("**Documento**")
                    st.write(doc)
                i+=1

if __name__ == "__main__":
    if "documents" not in st.session_state:
        st.session_state["documents"] = []
    render_upload_page()
    display_sidebar_content(logger)
