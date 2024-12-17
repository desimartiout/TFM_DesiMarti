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

apply_cab("HelpMe.ai - Carga de documentos")
apply_custom_css(logger)

# # Set page config with title, icon, and layout
# st.set_page_config(page_title="HelpMe.AI - Carga de documentos", page_icon="📂")

# # Custom CSS to style the page and sidebar
# st.markdown(
#     ESTILOS,
#     unsafe_allow_html=True,
# )

# # Add a logo (replace with your own image file path or URL)
# logo_path = "images/logo.png"  # Replace with your logo file
# if os.path.exists(logo_path):
#     st.sidebar.image(logo_path, width=220)
# else:
#     st.sidebar.markdown("### Logo Placeholder")
#     logger.warning("Logo no encontrado.")

# # Sidebar header
# st.sidebar.markdown(
#     "<h2 style='text-align: center;'>HelpMe.ai</h2>", unsafe_allow_html=True
# )
# st.sidebar.markdown(
#     "<h4 style='text-align: center;'>Tu chatbot de ayuda conversacional</h4>",
#     unsafe_allow_html=True,
# )

# # Footer
# st.sidebar.markdown(
#     """
#     <div class="footer-text">
#         © 2024 Desi Martí
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

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

    st.title("Cargar documentos")
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
        for id_, document, metadata in zip(document_names['ids'], document_names['documents'], document_names['metadatas']):
            logger.info(f"ID: {id_}, Document: {document}, Metadata: {metadata}")
            text = document
            st.session_state["documents"].append(
                {"filename": id_, "content": len(text), "file_path": None}
            )
    else:
        print("No documents to process.")

    if "deleted_file" in st.session_state:
        st.success(
            f"El fichero '{st.session_state['deleted_file']}' fué correctamente borrado."
        )
        del st.session_state["deleted_file"]

    #Permitir que se añadan nuevos documentos
    uploaded_files = st.file_uploader(
        "Cargar documentos YAML", type="yaml", accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("Uploading and processing documents. Please wait..."):
            for uploaded_file in uploaded_files:
                if uploaded_file.name in document_names:
                    st.warning(
                        f"El fichero  '{uploaded_file.name}' ya existe."
                    )
                    continue

                file_path = save_uploaded_file(uploaded_file)
                text = leer_yaml_como_string(file_path)

                file_without_extension, _ = os.path.splitext(uploaded_file.name)
                cargarDocumento(text,"", file_without_extension)

                st.session_state["documents"].append(
                    {
                        "filename": uploaded_file.name,
                        "content": text,
                        "file_path": file_path,
                    }
                )

                logger.info(f"Fichero '{uploaded_file.name}' cargado e indexado.")

        st.success("Ficheros cargados e indexados correctamente!!!!")

    if st.session_state["documents"]:
        #st.markdown("### Cargar Documentos")
        with st.expander("Administrar documentos cargados", expanded=True):
            for idx, doc in enumerate(st.session_state["documents"], 1):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(
                        f"{idx}. {doc['filename']} - {doc['content']} caracteres extraidos"
                    )
                with col2:
                    delete_button = st.button(
                        "Delete",
                        key=f"delete_{doc['filename']}_{idx}",
                        help=f"Delete {doc['filename']}",
                    )


def save_uploaded_file(uploaded_file) -> str:  # type: ignore
    UPLOAD_DIR = "uploaded_files"
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    logger.info(f"Fichero '{uploaded_file.name}' guardado en '{file_path}'.")
    return file_path


if __name__ == "__main__":
    if "documents" not in st.session_state:
        st.session_state["documents"] = []
    render_upload_page()
    display_sidebar_content(logger)
