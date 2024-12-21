import logging
import os

import streamlit as st
from pypdf import PdfReader

from config.global_config import BD_VECTORIAL_CHROMADB, TIPO_BD_VECTORIAL
from libs.faiss_utils import agregar_documento
from libs.searchchromadb import cargarDocumento
from libs.utils import limpia_cadena, setup_logging, apply_cab, apply_custom_css, display_sidebar_content

import json

# Initialize logger
setup_logging()  # Set up centralized logging configuration
logger = logging.getLogger(__name__)

apply_cab("HelpMe.ai - Carga manual de ayudas a partir de fichero pdf.")
apply_custom_css(logger)

def render_upload_page() -> None:
    """
    Renders the document upload page for users to upload and manage PDFs.
    Shows only the documents that are present in the OpenSearch index.
    """

    st.title("Carga manual de ayudas en formato pdf")
    st.subheader("Mediante esta página puede cargar manualmente ayudas a partir de ficheros pdf")

    # Initialize or clear the documents list in session state
    st.session_state["documents"] = []

    #Permitir que se añadan nuevos documentos
    uploaded_files = st.file_uploader(
        "Puede seleccionar uno o varios ficheros en formato pdf", type="pdf", accept_multiple_files=True
    )

    if uploaded_files:
        with st.spinner("Subiendo y cargando documento. Por favor, espere..."):
            for uploaded_file in uploaded_files:
                # Cargar el archivo PDF en PdfReader
                pdf_reader = PdfReader(uploaded_file)

                text = ""
                for page in pdf_reader.pages:

                    extracted_text = page.extract_text()

                    if extracted_text:
                        # Convertir a UTF-8 explícitamente
                        extracted_text = extracted_text.encode('utf-8', errors='ignore').decode('utf-8')
                        text += extracted_text + " \n "
        
                # Mostrar el texto extraído
                st.text_area(f"Texto extraído del PDF {uploaded_file.name}", text, height=300)

                texto_limpio = limpia_cadena(text)
                print(texto_limpio)
                if (TIPO_BD_VECTORIAL==BD_VECTORIAL_CHROMADB):
                    #Chromadb
                    cargarDocumento(texto_limpio,"","")
                else:
                    #faiss
                    agregar_documento(texto_limpio)

                logger.info(f"Fichero '{uploaded_file.name}' cargado e indexado.")

        st.success(":white_check_mark: Ficheros cargados e indexados correctamente!!!!")
        st.toast(f":white_check_mark: Ficheros cargados e indexados correctamente")

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
