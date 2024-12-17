import os
import logging
from pathlib import Path
from langchain_core.documents.base import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import pickle as pkl
import shutil
from datetime import datetime
import numpy as np
import dill

INDEX_FAISS = "faiss_index.pkl"
RETRIEVER_FAISS = "faiss_index.pkl"
RUTA_FAISS = "/faiss/"
LOG_FILE_PATH = "/logs/"
OLLAMA_MODEL_NAME = "llamaAyudas:latest"
FAISS_SENTENCE_TRANSFORMER = "paraphrase-multilingual-MiniLM-L12-v2"

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

class BdFaiss():

    def __init__(self):
        self.embedding_llm = OllamaEmbeddings(model=OLLAMA_MODEL_NAME)
        self.ruta_faiss = RUTA_FAISS

    def cargarDocumento(self, documento, metadato, id):
        
        documentos = []
        # Convertir la cadena en un objeto Document
        document = Document(page_content=documento)

        # document = Document(
        #         page_content=documento,  # El contenido principal del documento
        #         metadata={
        #             metadato
        #         },
        #         id=id
        #     )
        # Añadir el Documento a la lista
        documentos.append(document)
        self.documentos = documentos

        # # # Crear embeddings usando OpenAI (o el modelo que prefieras)
        # # embeddings = OpenAIEmbeddings()
        # # # Convertir el texto a embeddings (vectores)
        # # embedding_vector = embeddings.embed_documents([document.page_content])[0]

        # # Inicializar un modelo de Sentence Transformer para obtener embeddings
        # model = SentenceTransformer(FAISS_SENTENCE_TRANSFORMER)  # Modelo open source para embeddings
        # embedding_vector = model.encode([documento])  # Generar embeddings para la lista de textos

        # # Inicializar FAISS y agregar el vector
        # dimension = len(embedding_vector)  # La dimensión del vector de embedding
        # self.retriever
        # faiss_index = FAISS.IndexFlatL2(dimension)  # Usar IndexFlatL2 o cualquier otro índice de FAISS

        # # Convertir el vector a un formato que FAISS pueda manejar
        # faiss_vector = np.array(embedding_vector, dtype=np.float32).reshape(1, -1)

        # # Agregar el vector a FAISS
        # faiss_index.add(faiss_vector)

    # def cargarDocumento(documento, metadato, id):
    #     client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))

    #     sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=CHROMA_SENTENCE_TRANSFORMER)

    #     # collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, embedding_function=sentence_transformer_ef, metadata={"hnsw:space": "cosine"})
    #     collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME, metadata={"hnsw:space": "cosine"})
        
    #     # Inicializar un modelo de Sentence Transformer para obtener embeddings
    #     model = SentenceTransformer(CHROMA_SENTENCE_TRANSFORMER)  # Modelo open source para embeddings
    #     embeddings = model.encode([documento])  # Generar embeddings para la lista de textos

    #     # #Opcion con OPENAIEmbeddings
    #     # # Crear embeddings usando OpenAI (o el modelo que prefieras)
    #     # embeddings_model = OpenAIEmbeddings()

    #     # # Convertir el texto a embeddings (vectores)
    #     # embeddings = embeddings_model.embed_documents([documento])[0]

    #     collection.upsert(
    #         documents=[documento],
    #         metadatas=dict(metadato),
    #         ids=[id],
    #         embeddings=embeddings
    #     )

    def generar_vector_store(self):
        text_splitter = RecursiveCharacterTextSplitter()
        documents_embd = text_splitter.split_documents(self.documentos)
        self.vector_index = FAISS.from_documents(documents_embd, self.embedding_llm)
        self.retriever = self.vector_index.as_retriever()

    def persistir_bbdd_vectorial(self):
        if os.path.exists(self.ruta_faiss):
            # Si existe, borra su contenido
            for filename in os.listdir(self.ruta_faiss):
                file_path = os.path.join(self.ruta_faiss, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Error al eliminar {file_path}. Razón: {e}')
        else:
            # Si no existe, crea el directorio
            os.makedirs(self.ruta_faiss)

        try:
            with open(self.ruta_faiss / Path(INDEX_FAISS), 'wb') as archivo:
                # pkl.dump(self.vector_index, archivo)
                dill.dump(self.vector_index, archivo)
        except Exception as e:
            logger.error(f'Un Error se produjo al intentar guardar la base de datos de embbedings vector Index: {e}')

        try:
            with open(self.ruta_faiss / Path(RETRIEVER_FAISS), 'wb') as archivo:
                # pkl.dump(self.retriever, archivo)
                dill.dump(self.retriever, archivo)
        except Exception as e:
            logger.error(f'Un Error se produjo al intentar guardar la base de datos de embbedings tipo retriever: {e}')


if __name__ == '__main__':
    """
    Método principal para probar la clase.
    """
    BDVect = BdFaiss()
    retriever = BDVect.cargarDocumento("contenido","metadato","12")
    BDVect.generar_vector_store()
    BDVect.persistir_bbdd_vectorial()
