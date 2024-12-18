import logging
from typing import Dict, Iterable, List, Optional

import ollama
import streamlit as st

from src.constants import OLLAMA_MODEL_NAME
from src.embeddings import get_embedding_model
#from src.opensearch import hybrid_search
from src.searchchromadb import consultaChromadb

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
            Eres un asistente experto en subvenciones. A continuación, te proporcionaré los datos de una convocatoria en formato estructurado YAML. Tu tarea es:
            1. Analizar el contenido.
            2. Resumirlo en formato claro y comprensible.
            3. Destacar las partes más importantes: enlaces, beneficiarios, fechas clave y presupuesto.

            Aquí tienes los datos:

            El formato que espero del listado de ayudas está en YAML y es el siguiente:

            **Convocatoria de Ayuda: 795795**
            - **Órgano convocante:** MURCIA - AYUNTAMIENTO DE MURCIA
            - **Enlace a la convocatoria:** [Acceder](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795795)
            - **Sede electrónica para presentar solicitud:** [Ir a sede](https://sede.murcia.es/areas?idCategoria=10004)
            - **Presupuesto total:** 205,000 Euros
            - **Descripción:** Subvenciones para costes de explotación de taxis adaptados.
            - **Beneficiarios:** PYME y personas físicas que desarrollan actividad económica.
            - **Sectores involucrados:** Otro transporte terrestre de pasajeros.
            - **Región de impacto:** Región de Murcia (ES62).
            - **Estado de convocatoria:** Cerrada.
            - **Fechas importantes:**
            - Inicio solicitudes: 15/11/2024
            - Fin solicitudes: 28/11/2024
            - **Documentos relevantes:**
            1. **Publicación en el BORM:** [PUBLICACION_BORM.pdf](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159031)
            2. **Certificado:** [Certificado_2024.pdf](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159030)
            
            """
    
    if context:
        prompt += (
            "\nAquí tienes el contexto de las convocatorias encontradas en la búsqueda:\nContexto:\n \""""
            + context
            + "\"""\n"
            + "He detectado que me has proporcionado múltiples documentos YAML. Enumeraré primero las convocatorias y luego procederé a resumir cada una:\n"
            + "1. Convocatoria 795795\n"
            + "2. Convocatoria XXXX...\n"
            + "Resumen de cada convocatoria:\n"
            + "---\n"
            + "**Convocatoria 795795**\n"
            + "[Resumen aquí]\n"
            + "---\n"
            + "**Convocatoria XXXX**\n"
            + "[Resumen aquí]\n"

        )
    else:
        prompt += "Responde a las preguntas con lo mejor de tu conocimiento.\n"

    """ if history:
        prompt += "Historial de conversación:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            prompt += f"{role}: {content}\n"
        prompt += "\n" """

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
    
    context = consultaChromadb(query, num_results)

    # Generate prompt using the prompt_template function
    prompt = prompt_template(query, context, history)

    logger.info(f"prompt: {prompt}")

    return run_llama_streaming(prompt, temperature)
