import logging
import os

import numpy as np
import pandas as pd

import streamlit as st

from libs.chat import (  # type: ignore
    buscar_cadena,
    ensure_model_pulled,
    generate_response_streaming_ollama,
    generate_response_streaming_openai,
    # get_embedding_model,
)
from config.global_config import OLLAMA_TEMPERATURE, CHROMA_NUMDOCUMENTS, AI_ICON, HUMAN_ICON, LLM_MODELO_SELECCIONADO,LLM_TIPOMODELO_OPENAI,LLM_TIPOMODELO_OLLAMA
from config.web.web_config import CHATBOT_INTRO, CHATBOT_CAB, CHATBOT_TITLE

from libs.utils import stream_data, display_sidebar_content, apply_cab_chat, apply_custom_css_chat

# Initialize logger
logger = logging.getLogger(__name__)
apply_cab_chat(CHATBOT_CAB)
apply_custom_css_chat(logger)

# Main chatbot page rendering function
def render_chatbot_page() -> None:
    # Set up a placeholder at the very top of the main content area
    st.title(CHATBOT_TITLE)

    # # Copy last message to clipboard
    # if st.button("Borrar Historial"):
    #     st.session_state["chat_history"] = 0
    #     logger.info("Historial borrado")

    model_loading_placeholder = st.empty()

    # Initialize session state variables for chatbot settings
    if "num_results" not in st.session_state:
        st.session_state["use_hybrid_search"] = False
    if "num_results" not in st.session_state:
        st.session_state["num_results"] = CHROMA_NUMDOCUMENTS
    if "temperature" not in st.session_state:
        st.session_state["temperature"] = OLLAMA_TEMPERATURE

    # st.session_state["num_results"] = st.sidebar.number_input(
    #     "Número de resultados en la ventana de contexto",
    #     min_value=1,
    #     max_value=10,
    #     value=st.session_state["num_results"],
    #     step=1,
    # )
    
    # st.session_state["temperature"] = st.sidebar.slider(
    #     "Temperatura de respuesta",
    #     min_value=0.0,
    #     max_value=1.0,
    #     value=st.session_state["temperature"],
    #     step=0.1,
    # )

    # Display loading spinner at the top of the main content area
    with model_loading_placeholder.container():
        st.spinner("Cargando modelos para el chat...")

    # Load models if not already loaded
    if "embedding_models_loaded" not in st.session_state:
        with model_loading_placeholder:
            with st.status("Descargando datos...", expanded=True) as status:
                st.write("Cargando modelos de embedding...")
                #st.session_state["embedding"]= get_embedding_model()
                st.write("Cargando modelo LLM Ollama...")
                #ensure_model_pulled(OLLAMA_MODEL_NAME)
                
        logger.info("Modelo de embedding cargado.")
        model_loading_placeholder.empty()

    # Initialize chat history in session state if not already present
    if "chat_history" not in st.session_state or st.session_state["chat_history"] == 0:

        st.session_state["chat_history"] = []

        message = st.chat_message("assistant", avatar=AI_ICON)
        message.write_stream(stream_data(CHATBOT_INTRO))

    logger.info("------------------")
    logger.info(st.session_state["chat_history"])
    logger.info("------------------")

    # tab1, tab2 = st.tabs(["📈 Chat", "🗃 Log"])    
    # with tab1:
    #     tab1.subheader("Chat")

    # with tab2:
    #     tab2.subheader("Historial de la conversación")
    #     tab2.write(st.session_state["chat_history"])

    # Display chat history
    for message in st.session_state["chat_history"]:
        texto = message['content']
        if message["role"]=="assistant":
            message = st.chat_message("assistant", avatar=AI_ICON)
            message.markdown(texto)
        else:
            message = st.chat_message("user", avatar=HUMAN_ICON)
            logger.info(f"Historico user: {texto}")
            message.markdown(texto)

    # Process user input and generate response
    if prompt := st.chat_input("Escribe tu consulta aquí..."):
        with st.chat_message("user", avatar=HUMAN_ICON):
            st.markdown(prompt)
        st.session_state["chat_history"].append({"role": "user", "content": prompt})
        logger.info("Entrada recibida.")

        # Generate response from assistant
        with st.chat_message("assistant", avatar=AI_ICON):
            with st.spinner("Generando respuesta..."):
                response_placeholder = st.empty()
                response_text = ""
            
                response_text = buscar_cadena(
                        prompt,
                        "",
                        num_results=st.session_state["num_results"],
                        temperature=st.session_state["temperature"],
                        chat_history=st.session_state["chat_history"],
                    )
                response_placeholder.write_stream(stream_data(response_text))
                

            st.session_state["chat_history"].append(
                {"role": "assistant", "content": response_text}
            )
            
            logger.info("Respuesta generada y mostrada.")
            st.toast(f"white_check_mark: Respuesta generada y mostrada correctamente") # Mensaje TOAST

            # sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
            # selected = st.feedback("thumbs")
            # if selected is not None:
            #     st.markdown(f"You selected: {sentiment_mapping[selected]}")
            #     st.toast(f"You selected: {sentiment_mapping[selected]}", icon=None)

# Main execution
if __name__ == "__main__":
    render_chatbot_page()
    display_sidebar_content(logger)
