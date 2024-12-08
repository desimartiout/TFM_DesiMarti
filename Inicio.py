import logging
import os
import time

import streamlit as st

from src.utils import setup_logging, stream_data, display_sidebar_content, display_main_content, apply_custom_css, apply_cab
from src.constants import LOGO_URL_LARGE, LOGO_URL_SMALL, CHATBOT_WELLCOME, ESTILOS_INICIO

# Initialize logger
setup_logging()  # Set up logging configuration
logger = logging.getLogger(__name__)

# Main execution
if __name__ == "__main__":
    apply_cab("Chatbot AyudaMe.ai")
    apply_custom_css(logger)
    display_sidebar_content(logger)
    display_main_content(logger)
