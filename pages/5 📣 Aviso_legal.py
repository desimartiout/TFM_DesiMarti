import streamlit as st
import logging
from config.web.web_config import TEXTO_AVISOLEGAL, CAB_AVISOLEGAL
from libs.utils import apply_custom_css, display_sidebar_content, apply_cab

logger = logging.getLogger(__name__)

apply_cab(CAB_AVISOLEGAL)
apply_custom_css(logger)
display_sidebar_content(logger)

# Interfaz de la aplicación
st.title("Aviso Legal")
st.markdown(TEXTO_AVISOLEGAL, unsafe_allow_html=True)
