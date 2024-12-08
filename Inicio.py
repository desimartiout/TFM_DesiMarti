import logging
import os
import time

import streamlit as st

from src.utils import setup_logging, stream_data, display_sidebar_content, apply_custom_css, apply_cab
from src.constants import LOGO_URL_LARGE, LOGO_URL_SMALL, CHATBOT_WELLCOME, ESTILOS_INICIO

# Initialize logger
setup_logging()  # Set up logging configuration
logger = logging.getLogger(__name__)

def display_main_content(logger) -> None:
    st.title("Chatbot para búsqueda de ayudas y subvenciones del Gobierno de España ")
    #st.write_stream(stream_data(CHATBOT_WELLCOME))
    st.write(CHATBOT_WELLCOME)
    logger.info("Mostrar página bienvenida.")

# Main execution
if __name__ == "__main__":
    apply_cab("Chatbot AyudaMe.ai")
    apply_custom_css(logger)
    display_sidebar_content(logger)
    display_main_content(logger)
