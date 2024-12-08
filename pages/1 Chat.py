import logging
import os

import streamlit as st

from src.chat import (  # type: ignore
    generate_response_streaming,
    get_embedding_model,
    generate_response,
)
from src.constants import OLLAMA_MODEL_NAME, OLLAMA_TEMPERATURE, CHROMA_NUMDOCUMENTS
from src.utils import setup_logging

# Initialize logger
setup_logging()  # Configures logging for the application
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(page_title="HelpMe.AI - Chatbot", page_icon="🤖")

# Apply custom CSS
st.markdown(
    """
    <style>
    /* Main background and text colors */
    body { background-color: #f0f8ff; color: #002B5B; }
    .sidebar .sidebar-content { background-color: #006d77; color: white; padding: 20px; border-right: 2px solid #003d5c; }
    .sidebar h2, .sidebar h4 { color: white; }
    .block-container { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); }
    .footer-text { font-size: 1.1rem; font-weight: bold; color: black; text-align: center; margin-top: 10px; }
    .stButton button { background-color: #118ab2; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px; }
    .stButton button:hover { background-color: #07a6c2; color: white; }
    h1, h2, h3, h4 { color: #006d77; }
    .stChatMessage { background-color: #e0f7fa; color: #006d77; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .stChatMessage.user { background-color: #118ab2; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)
logger.info("Custom CSS applied.")


# Main chatbot page rendering function
def render_chatbot_page() -> None:
    # Set up a placeholder at the very top of the main content area
    st.title("HelpMe.AI - Chatbot")
    model_loading_placeholder = st.empty()

    # Initialize session state variables for chatbot settings
    if "num_results" not in st.session_state:
        st.session_state["use_hybrid_search"] = False
    if "num_results" not in st.session_state:
        st.session_state["num_results"] = CHROMA_NUMDOCUMENTS
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = OLLAMA_TEMPERATURE

    st.session_state["num_results"] = st.sidebar.number_input(
        "Número de resultados en la ventana de contexto",
        min_value=1,
        max_value=10,
        value=st.session_state["num_results"],
        step=1,
    )
    st.session_state["temperature"] = st.sidebar.slider(
        "Temperatura de respuesta",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state["temperature"],
        step=0.1,
    )

    # Display logo or placeholder
    logo_path = "images/logo.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=220)
        logger.info("Logo mostrado.")
    else:
        st.sidebar.markdown("### Logo Placeholder")
        logger.warning("Logo no encontrado, mostrando placeholder.")

    # Sidebar headers and footer
    st.sidebar.markdown(
        "<h2 style='text-align: center;'>HelpMe.ai</h2>", unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<h4 style='text-align: center;'>Tu chatbot de ayuda conversacional</h4>",
        unsafe_allow_html=True,
    )

    # Footer text
    st.sidebar.markdown(
        """
        <div class="footer-text">
            © 2024 Desi Martí
        </div>
        """,
        unsafe_allow_html=True,
    )
    logger.info("Barra lateral configurada.")

    # Display loading spinner at the top of the main content area
    with model_loading_placeholder.container():
        st.spinner("Cargando modelos para el chat...")

    # Load models if not already loaded
    if "embedding_models_loaded" not in st.session_state:
        with model_loading_placeholder:
            with st.spinner("Cargando modelos de embedding y Ollama para búsqueda híbrida..."):
                get_embedding_model()
                #ensure_model_pulled(OLLAMA_MODEL_NAME)
                st.session_state["embedding_models_loaded"] = True
        logger.info("Modelo de embedding cargado.")
        model_loading_placeholder.empty()

    # Initialize chat history in session state if not already present
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process user input and generate response
    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        logger.info("Entrada recibida.")

        # Generate response from assistant
        with st.chat_message("assistant"):
            with st.spinner("Generando respuesta..."):
                response_placeholder = st.empty()
                response_text = ""

                response_text = generate_response(
                    prompt,
                    use_hybrid_search=st.session_state["use_hybrid_search"],
                    num_results=st.session_state["num_results"],
                    temperature=st.session_state["temperature"],
                    chat_history=st.session_state["chat_history"],
                )

            response_placeholder.markdown(response_text)
            st.session_state["chat_history"].append(
                {"role": "assistant", "content": response_text}
            )
            logger.info("Respuesta generada y mostrada.")
            
            st.toast(f"Respuesta generada y mostrada.") # Mensaje TOAST

            #Feedback from th user https://github.com/trubrics/streamlit-feedback
            #feedback = streamlit_feedback(feedback_type="thumbs", align="flex-start")
            #feedback = streamlit_feedback(feedback_type="faces", on_submit=_submit_feedback)
            #streamlit_feedback(
            #    feedback_type="thumbs",on_submit=_submit_feedback
            #)
            # para ejecutar npm en powershell
            # #Set-ExecutionPolicy RemoteSigned -Scope CurrentUser ​


def _submit_feedback(user_response, emoji=None):
    st.toast(f"Feedback submitted: {user_response}", icon=emoji)
    logger.info("Feedback submitted: {user_response}")
    #return user_response.update({"some metadata": 123})

# Main execution
if __name__ == "__main__":
    render_chatbot_page()
