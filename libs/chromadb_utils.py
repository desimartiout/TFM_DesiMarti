import json
import logging
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_openai import OpenAIEmbeddings
from chromadb.config import Settings
from chromadb.utils import embedding_functions
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

def cargarDocumento_old(documento, metadato, id):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=CHROMA_SENTENCE_TRANSFORMER)

    # collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
    
    # Inicializar un modelo de Sentence Transformer para obtener embeddings
    model = SentenceTransformer(CHROMA_SENTENCE_TRANSFORMER)  # Modelo open source para embeddings
    embeddings = model.encode([documento])  # Generar embeddings para la lista de textos

    # #Opcion con OPENAIEmbeddings
    # # Crear embeddings usando OpenAI (o el modelo que prefieras)
    # embeddings_model = OpenAIEmbeddings()

    # # Convertir el texto a embeddings (vectores)
    # embeddings = embeddings_model.embed_documents([documento])[0]

    collection.upsert(
        documents=[documento],
        metadatas=dict(metadato),
        ids=[id],
        embeddings=embeddings
    )

def cargarDocumento(documento, metadato, id):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))
    try:
        logging.info(f"Antes de cargarDocumento id {id}")

        model_path = "../models/paraphrase-multilingual-MiniLM-L12-v2"
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_path)

        # sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=CHROMA_SENTENCE_TRANSFORMER)
        collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})
        # collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, embedding_function=sentence_transformer_ef)
        
        collection.upsert(
            documents=[documento],
            metadatas=dict(metadato),
            ids=[id],
        )
    except Exception as e:
        logging.error(f"Error al cargarDocumento id {id}: {e}")

