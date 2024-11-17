import logging
from typing import Dict, Iterable, List, Optional

import ollama
import streamlit as st

from src.constants import ASSYMETRIC_EMBEDDING, OLLAMA_MODEL_NAME
from src.embeddings import get_embedding_model
from src.opensearch import hybrid_search
from src.utils import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@st.cache_resource(show_spinner=False)
def ensure_model_pulled(model: str) -> bool:
    try:
        available_models = ollama.list()
        if model not in available_models:
            logger.info(f"Modelo {model} not encontrado localmente. Descargando el modelo ...")
            ollama.pull(model)
            logger.info(f"Modelo {model} ha sido descargado y ya está disponible localmente.")
        else:
            logger.info(f"Modelo {model} está disponible localmente.")
    except ollama.ResponseError as e:
        logger.error(f"Error al comprobar el modelo o al descargarlo: {e.error}")
        return False
    return True


def run_llama_streaming(prompt: str, temperature: float) -> Optional[Iterable[str]]: 
    try:
        logger.info("Respuesta desde el modelo OLlama.")
        stream = ollama.chat(
            model=OLLAMA_MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            options={"temperature": temperature},
        )
    except ollama.ResponseError as e:
        logger.error(f"Error durante llamada al modelo OLlama: {e.error}")
        return None

    return stream


def prompt_template(query: str, context: str, history: List[Dict[str, str]]) -> str:
    prompt = """
            Eres un asistente chat (chatbot) para ayudar obtener ingformación de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario para encontrar las subvenciones que necesite el usuario en base a sus criterios de búsqueda.
            * Deberás de identificar las oportunidades de ayudas y subvenciones.
            * Proporciona detalles el organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Ofrece consejos sobre cómo mejorar mi aplicación y aumentar mis posibilidades de éxito.
            * Cuando te pregunten por las ayudas y subvenciones centrate en la información que te proporciona el contexto.

            * Es importante que los resultados sean precisos y actualizados.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.
            """
    
    if context:
        prompt += (
            "Utiliza este contexto para responder a la pregunta.\nContext:\n"
            + context
            + "\n"
        )
    else:
        prompt += "Responde a las preguntas con lo mejor de tu conocimiento.\n"

    if history:
        prompt += "Historial de conversación:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            prompt += f"{role}: {content}\n"
        prompt += "\n"

    prompt += f"User: {query}\nAssistant:"
    logger.info("Prompt construido con contexto e historial de conversación.")
    return prompt


def generate_response_streaming(
    query: str,
    use_hybrid_search: bool,
    num_results: int,
    temperature: float,
    chat_history: Optional[List[Dict[str, str]]] = None,
) -> Optional[Iterable[str]]:
    chat_history = chat_history or []
    max_history_messages = 10
    history = chat_history[-max_history_messages:]
    context = ""

    # Include hybrid search results if enabled
    if use_hybrid_search:
        logger.info("Haciendo bíusqueda híbrida.")
        if ASSYMETRIC_EMBEDDING:
            prefixed_query = f"passage: {query}"
        else:
            prefixed_query = f"{query}"
        embedding_model = get_embedding_model()
        query_embedding = embedding_model.encode(
            prefixed_query
        ).tolist()  # Convert tensor to list of floats
        search_results = hybrid_search(query, query_embedding, top_k=num_results)
        logger.info("Búsqueda híbrida completada.")

        # Collect text from search results
        for i, result in enumerate(search_results):
            context += f"Ayuda {i}:\n{result['_source']['text']}\n\n"

    # Generate prompt using the prompt_template function
    prompt = prompt_template(query, context, history)

    logger.info(f"prompt: {prompt}")

    return run_llama_streaming(prompt, temperature)
