import logging
import os

import streamlit as st

from src.utils import setup_logging

# Initialize logger
setup_logging()  # Set up logging configuration
logger = logging.getLogger(__name__)

# Set page config with title, icon, and layout
st.set_page_config(
    page_title="Chatbot Ayuda.me", page_icon="🤖"
)


# Custom CSS to style the page and sidebar
def apply_custom_css() -> None:
    """Applies custom CSS styling to the Streamlit page and sidebar."""
    st.markdown(
        """
        <style>
        /* Main background and text colors */
        body {
            background-color: #f0f8ff;  /* Light cyan background */
            color: #002B5B;  /* Dark blue text for readability */
        }
        .sidebar .sidebar-content {
            background-color: #006d77;  /* Dark cyan sidebar background */
            color: white;
            padding: 20px;
            border-right: 2px solid #003d5c;  /* Darker border */
        }
        .sidebar h2, .sidebar h4 {
            color: white;  /* White text for sidebar headings */
        }
        .block-container {
            background-color: white;  /* White content background */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Subtle shadow for modern look */
        }
        /* Center content inside columns */
        .stColumn {
            text-align: center;
        }
        /* Style for the centered and bold footer text */
        .footer-text {
            font-size: 1.1rem;
            font-weight: bold;
            color: black;
            text-align: center;
            margin-top: 10px;
        }
        /* Style buttons to look modern and attractive */
        .stButton button {
            background-color: #118ab2;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
        }
        .stButton button:hover {
            background-color: #07a6c2;
            color: white;
        }
        /* Headings inside the main page */
        h1, h2, h3, h4 {
            color: #006d77;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Css aplicado.")


# Function to display logo or placeholder
def display_logo(logo_path: str) -> None:
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

def display_main_content() -> None:
    st.title("Chatbot para búsqueda de ayudas y subvenciones del Gobierno de España 📄🤖")
    st.markdown(
        """
        Bienvenido al Chatbot Ayuda.me 👋
        
        Esta ayuda permite la búsqueda de información de ayudas y subvenciones del Gobierno de Espala
        
        """
    )
    logger.info("Mostrar página bienvenida.")


def display_sidebar_content() -> None:
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>Jam with AI</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Tu Chatbot de ayudas</h4>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2024 Desi Martí
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Mostrar barra lateral.")


# Main execution
if __name__ == "__main__":
    apply_custom_css()
    display_logo("images/logo.png")
    display_sidebar_content()
    display_main_content()
