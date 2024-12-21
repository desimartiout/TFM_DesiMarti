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
        
        #Mostrar documentos en la página actual
        # current_docs = st.session_state["documents"][start_idx:end_idx]

        # st.markdown(f"### Página {current_page} de {total_pages}")

        # for idx, doc in enumerate(current_docs, start=start_idx + 1):
        #     with st.expander(f"Ayuda {doc['filename']}", expanded=False):
        #         col1, col2 = st.columns([1, 1])
        #         with col1:
        #             st.markdown("**Documento**")
        #             st.code(doc['content'], language="yaml", line_numbers=False, wrap_lines=True)
        #         with col2:
        #             st.markdown("**Metadatos**")
        #             st.code(doc['metadata'], language="json", line_numbers=False, wrap_lines=True)
    else:
        #FAISS
        document_names = obtener_todos_documentos()
        num_documentos = len(document_names)
        logger.info(document_names)
        logger.info("Obtenidos nombres de documentos desde FAISS.")

        # Inicializar documentos en el estado de la sesión
        if "documents" not in st.session_state:
            st.session_state["documents"] = []

        # Agregar documentos al estado de la sesión
        if len(document_names) != 0:
            st.subheader(f"Actualmente tenemos :blue[{num_documentos}] ayudas :sunglasses:")
            st.caption("Puedes ver el detalle almacenado pinchando en cada ayuda")
            for document in document_names:
                st.session_state["documents"].append(document)
        else:
            st.write("No hay documentos para procesar.")

        logger.info(f"State: {st.session_state['documents']}")
        logger.info(f"State: {len(st.session_state['documents'])}")

        # Parámetros de paginación
        docs_per_page = 50  # Cambia este valor para ajustar el número de documentos por página
        total_docs = len(st.session_state["documents"])
        total_pages = (total_docs + docs_per_page - 1) // docs_per_page

        
        st.write("Página")
    
        st.markdown("""
        <style>
        div[data-baseweb="input"] {
            width: 80px !important;  /* Ajusta el ancho deseado */
            margin-left: auto;
            margin-right: auto;
        }
        </style>
        """, unsafe_allow_html=True)

        # Selector de página
        current_page = st.number_input(
        "Página", min_value=1, max_value=total_pages, value=1, step=1, label_visibility="collapsed"
        )
        # Índices para los documentos a mostrar
        start_idx = (current_page - 1) * docs_per_page
        end_idx = start_idx + docs_per_page

        # Documentos actuales a mostrar
        current_docs = st.session_state["documents"][start_idx:end_idx]

        st.markdown(f"### Página {current_page} de {total_pages}")

        # Mostrar los documentos con paginación
        for i, doc in enumerate(current_docs, start=start_idx + 1):
            with st.expander(f"Ayuda {i}", expanded=False):
                st.markdown("**Documento**")
                st.write(doc)

        # if st.session_state["documents"]:
            # i=0
            # for doc in st.session_state["documents"]:    
            #     with st.expander(f"Ayuda {i}", expanded=False):
            #         st.markdown("**Documento**")
            #         st.write(doc)
            #     i+=1

            # Mostrar los documentos con paginación

if __name__ == "__main__":
    if "documents" not in st.session_state:
        st.session_state["documents"] = []
    render_upload_page()
    display_sidebar_content(logger)
