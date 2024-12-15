import logging
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
import os
from datetime import datetime

from config.chromadb_config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_PATH, CHROMA_PERSIST_PATH, CHROMA_SENTENCE_TRANSFORMER, LOG_FILE_PATH

def setup_logging() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
    ruta_log = ruta_actual + LOG_FILE_PATH

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}.log")

    logging.basicConfig(
        filename=log_file_path,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        encoding="utf-8"
    )

# Inicializo el logger
setup_logging()
logger = logging.getLogger(__name__)

def cargarDocumento(documento, metadato, id):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))

    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    
    # Inicializar un modelo de Sentence Transformer para obtener embeddings
    model = SentenceTransformer(CHROMA_SENTENCE_TRANSFORMER)  # Modelo open source para embeddings

    embeddings = model.encode([documento])  # Generar embeddings para la lista de textos

    #TODO: Hay que arreglar lo de los metadatos, espera un diccionario  -> array json con par clave valor
    collection.add(
        documents=[documento],
        metadatas=None,
        ids=[id],
        embeddings=embeddings
    )