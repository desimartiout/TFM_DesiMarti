from langchain_core.documents.base import Document
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import faiss
import numpy as np
# import pickle as pkl
import dill as pkl
from pathlib import Path

INDEX_FAISS = "faiss_index.pkl"
RETRIEVER_FAISS = "faiss_retriever.pkl"
RUTA_FAISS = "/faiss/"
OLLAMA_MODEL_NAME = "llamaAyudas:latest"

# Suponiendo que tienes la cadena de texto que deseas convertir
texto = "Este es un ejemplo de texto que se convertirá en un Documento."

# Convertir la cadena en un objeto Document
document = Document(page_content=texto)

# # Crear embeddings usando OpenAI (o el modelo que prefieras)
# embeddings = OpenAIEmbeddings()
# # Convertir el texto a embeddings (vectores)
# embedding_vector = embeddings.embed_documents([document.page_content])[0]
# # Inicializar FAISS y agregar el vector
# dimension = len(embedding_vector)  # La dimensión del vector de embedding
# faiss_index = faiss.IndexFlatL2(dimension)  # Usar IndexFlatL2 o cualquier otro índice de FAISS
# # Convertir el vector a un formato que FAISS pueda manejar
# faiss_vector = np.array(embedding_vector, dtype=np.float32).reshape(1, -1)
# # Agregar el vector a FAISS
# faiss_index.add(faiss_vector)

# Almacenar el documento en una lista o en algún otro lugar según tu necesidad
documents = [document]

embedding_llm = OllamaEmbeddings(model=OLLAMA_MODEL_NAME)
text_splitter = RecursiveCharacterTextSplitter()
documents_embd = text_splitter.split_documents(documents)
vector_index = FAISS.from_documents(documents_embd, embedding_llm)
retriever = vector_index.as_retriever()

try:
    print(RUTA_FAISS / Path(INDEX_FAISS))
    # with open("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/dbvector/faiss/vector.pkl", 'wb') as archivo:
    with open(RUTA_FAISS / Path(INDEX_FAISS), 'wb') as archivo:
        pkl.dump(vector_index, archivo)
        
except Exception as e:
    print(f'Un Error se produjo al intentar guardar la base de datos de embbedings vector Index: {e}')

try:
    print(RUTA_FAISS / Path(RETRIEVER_FAISS))
    with open(RUTA_FAISS / Path(RETRIEVER_FAISS), 'wb') as archivo:
        pkl.dump(retriever, archivo)
        
except Exception as e:
    print(f'Un Error se produjo al intentar guardar la base de datos de embbedings tipo retriever: {e}')