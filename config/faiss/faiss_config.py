import os
ruta_raiz = os.getcwd()

from config.global_config import SENTENCE_TRANSFORMER

# MODELO_EMBED_FAISS = "all-MiniLM-L6-v2"
MODELO_EMBED_FAISS = SENTENCE_TRANSFORMER   # Asíutilizamos el mismo modelo de embeddings para todo

LOG_FILE_PATH_FAISS = "/faiss/logs/"
# Rutas de archivos para índice y metadatos
INDEX_FILE_FAISS = ruta_raiz + "/faiss/mi_indice_faiss.index"
METADATA_FILE_FAISS = ruta_raiz + "/faiss/metadatos.json"