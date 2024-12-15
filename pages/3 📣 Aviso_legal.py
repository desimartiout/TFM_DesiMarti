import streamlit as st
import logging
from src.constantesWeb import ESTILOS, TEXTO_AVISOLEGAL
from src.utils import apply_custom_css, display_sidebar_content, apply_cab

# # Configuración de la página
# st.set_page_config(page_title="HelpMe.ai - Aviso Legal", layout="wide")

logger = logging.getLogger(__name__)

apply_cab("HelpMe.ai - Aviso Legal")
apply_custom_css(logger)
display_sidebar_content(logger)

# Interfaz de la aplicación
st.title("Aviso Legal")
st.markdown(TEXTO_AVISOLEGAL, unsafe_allow_html=True)
