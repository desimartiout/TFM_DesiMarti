import logging
from typing import Dict, Iterable, List, Optional

import ollama
import time
import streamlit as st

from src.constants import ASSYMETRIC_EMBEDDING, OLLAMA_MODEL_NAME
from src.embeddings import get_embedding_model
#from src.opensearch import hybrid_search
from src.searchchromadb import consultaChromadb

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
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

def prompt_template_old(query: str, context: str, history: List[Dict[str, str]]) -> str:
    prompt = """

            Eres un asistente chat (chatbot) para ayudar obtener información de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario a encontrar las subvenciones que necesite en base a sus preguntas.
            * Debes proporcionar detalles del organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Sofo ofrece información a partir del Contexto proporcionado.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.

            """
    
    if context:
        prompt += f"""----
            Contexto:
                {context}
            ---"""
    else:
        prompt += "Responde a las preguntas con lo mejor de tu conocimiento.\n"

    """ if history:
        prompt += "Historial de conversación:\n"
        for msg in history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"]
            prompt += f"{role}: {content}\n"
        prompt += "\n" """

    prompt += f"Pregunta: \n{query} \n"
    logger.info("Prompt construido con contexto e historial de conversación.")
    return prompt

def prompt_template(query: str, context: str, history: List[Dict[str, str]]) -> str:
    prompt = """
        Eres un asistente experto en subvenciones que recibe un listado de documentos en formato YAML. Tu tarea es:
            1. Analizar el contenido.
            2. Resumirlo en formato claro y comprensible.
            3. Destacar las partes más importantes: enlaces, beneficiarios, fechas clave y presupuesto.
            4. No te inventes nada.

            El formato de cada documento YAML es:
            Convocatoria: 
            Detalle de la convocatoria de ayuda o  subvención: 795854
            Enlace a convocatoria: 
            Órgano, comunidad, autonomía, región, provincia o ayuntamiento convocante: 
            Enlace / url a sede electr�nica presentaci�n ayuda: 
            Fecha de recepci�n: 
            Tipo de ayuda: 
            Tipo de convocatoria: 
            Presupuesto total: 
            Descripción: 
            Tipos de beneficiarios: 
            Sectores involucrados: 
            Regi�n de impacto: 
            Finalidad: 
            Bases reguladoras: 
            URL Bases Reguladoras: 
            Publicaci�n en diario oficial: 
            Estado de convocatoria abierta: 
            Fecha de inicio de solicitudes: 
            Fecha de fin de solicitudes: 
            Inicio de convocatoria: 
            Fin de convocatoria: 
            Reglamento: 
            Otros documentos de la convocatoria: 
            
            El formato que espero del listado de ayudas es el siguiente:

            **Convocatoria de Ayuda: 795795**
            - **Órgano convocante:** MURCIA - AYUNTAMIENTO DE MURCIA
            - **Enlace a la convocatoria:** [Acceder](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795795)
            - **Sede electrónica para presentar solicitud:** [Ir a sede](https://sede.murcia.es/areas?idCategoria=10004)
            - **Presupuesto total:** 205,000 Euros
            - **Descripción:** Subvenciones para costes de explotaci�n de taxis adaptados.
            - **Beneficiarios:** PYME y personas f�sicas que desarrollan actividad econ�mica.
            - **Sectores involucrados:** Otro transporte terrestre de pasajeros.
            - **Región de impacto:** Regi�n de Murcia (ES62).
            - **Estado de convocatoria:** Cerrada.
            - **Fechas importantes:**
            - Inicio solicitudes: 15/11/2024
            - Fin solicitudes: 28/11/2024
            - **Documentos relevantes:**
            1. **Publicación en el BORM:** [PUBLICACION_BORM.pdf](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159031)
            2. **Certificado:** [Certificado_2024.pdf](https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159030)

            """

    prompt += f"""
        Usando esta información: {context}
        Responde: {query}]
        """
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

def generate_response_streaming_new(
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

    llm = ChatOllama(
        model=OLLAMA_MODEL_NAME,
        temperature=temperature,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Tu eres un asistente virtual para contestar a ayudas públicas del gobierno de españa, te adjuntaré una información que debes usar para proporcionar la respuesta. No te inventes información que no esté en esta información.",
            ),
            ("human", "{input}"),
        ]
    )

    queryContext = f"Usando esta información: {context}. Responde: {query}" 

    chain = prompt | llm
    ai_msg = chain.invoke(
        {
            "input": f"{queryContext}",
        }
    )

    logger.info(f"Prompt: {queryContext}")
    logger.info(f"Respuesta: {ai_msg.content}")
    
    return ai_msg.content

