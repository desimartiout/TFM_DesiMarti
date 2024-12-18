import logging
from typing import Any, List

import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

# from src.constants import EMBEDDING_MODEL_PATH
from libs.utils import setup_logging

# Initialize logger
setup_logging()  # Configures logging for the application
logger = logging.getLogger(__name__)


# @st.cache_resource(show_spinner=False)
# def get_embedding_model() -> SentenceTransformer:
#     logger.info(f"Cargando modelo de embeddings desde la ruta: {EMBEDDING_MODEL_PATH}")
#     return SentenceTransformer(EMBEDDING_MODEL_PATH)


# def generate_embeddings(chunks: List[str]) -> List[np.ndarray[Any, Any]]:
#     model = get_embedding_model()
#     embeddings = [np.array(model.encode(chunk)) for chunk in chunks]
#     logger.info(f"Generados los embedings para {len(chunks)} bloques de texto.")
#     return embeddings
