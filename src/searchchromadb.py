import logging
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from src.utils import setup_logging
from src.constants import MOCK_IDS, MOCK_DOCUMENTS, MOCK_METADATAS, CHROMA_COLLECTION_NAME, CHROMA_PERSIST_PATH, OLLAMA_MODEL_NAME, OLLAMA_TEMPERATURE, SENTENCE_TRANSFORMER


# Inicializo el logger
setup_logging()
logger = logging.getLogger(__name__)

# Inicializar un modelo de Sentence Transformer para obtener embeddings
model = SentenceTransformer(SENTENCE_TRANSFORMER)  # Modelo open source para embeddings

def cargarDocumentosMOCK(collection):
    # Generamos embeddings manualmente
    texts = [doc for doc in MOCK_DOCUMENTS]
    embeddings = model.encode(texts)  # Generar embeddings para la lista de textos

    collection.add(
        documents=MOCK_DOCUMENTS,
        metadatas=MOCK_METADATAS,
        ids=MOCK_IDS,
        embeddings=embeddings
    )
    #Si los ids son iguales los reemplaza

# Función para obtener todos los documentos
def get_all_documents():
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    #Si no tengo documentos cargados los moqueo para poder tener datos.
    if (collection.count()==0):
        cargarDocumentosMOCK(collection)
    
    #Listar los documentos de la colección
    logger.info(f"SEARCH_CHROMA - Documentos en la colección {collection.count()}")

    documents = collection.get()

    # Display the documents
    for ids in documents['ids']:
        logger.info(f"SEARCH_CHROMA - Id {ids}")

    return documents

# Función para realizar una consulta (simulando una búsqueda por texto)
def query_documents(query_text: str, top_k: int = 3):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    #Si no tengo documentos cargados los moqueo para poder tener datos.
    if (collection.count()==0):
        cargarDocumentosMOCK(collection)
    
    #Listar los documentos de la colección
    logger.info(f"SEARCH_CHROMA - Documentos en la colección {collection.count()}")

    #collection = client.get_collection(CHROMA_COLLECTION_NAME)
    
    # Generar el embedding para la consulta
    query_embedding = model.encode([query_text]).tolist()
    
    # Realizar una búsqueda de similitud
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    return results


# OTROS MÉTODOS QUE AHORA NO SE UTILIZAN PERO PARA LAS PRUEBAS INICIALES FUERON ÚTILES

# Método para consultar en la base de datos vectorial
def consultaChromadb(query_text, top_k):
    results = query_documents(query_text, top_k)
    contexto = ""

    # Mostrar resultados de la consulta
    for result in results["documents"]:
        #print(result)
        contexto += f"Texto: {result}\n"

    logger.info(f"SEARCH_CHROMA - Contexto {contexto}:")

    return contexto

#Método para consultar en la bd vectorial y con el resultado ir al LLM a completar la contestación de una forma básica
def consultaBasica(query_text: str, top_k: int = 5):
    contexto = consultaChromadb(query_text, top_k)

    #Consulta básica sin Prompt
    llm = OllamaLLM(model=OLLAMA_MODEL_NAME, temperature=OLLAMA_TEMPERATURE)
    prompt = f"Usando esta información: {contexto} \n Responde: {query_text}]"
    #Basada en el resultado de ChromaDB
    respuesta = llm(prompt)

    # Imprimir la respuesta
    logger.info(f"SEARCH_CHROMA - Prompt: {prompt}")
    # Imprimir la respuesta
    logger.info(f"SEARCH_CHROMA - Respuesta: {respuesta}")

#Método para consultar en la bd vectorial y con el resultado ir al LLM a completar la contestación mediante prompt
def consultaPrompt(query_text: str, top_k: int = 5):
    contexto = consultaChromadb(query_text, top_k)

    llm = ChatOllama(
        model=OLLAMA_MODEL_NAME,
        temperature=OLLAMA_TEMPERATURE,
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

    queryContext = f"Usando esta información: {contexto}. Responde: {query_text}" 

    chain = prompt | llm
    ai_msg = chain.invoke(
        {
            "input": f"{queryContext}",
        }
    )
    logger.info(f"SEARCH_CHROMA - queryContext: {queryContext}")
    logger.info(f"SEARCH_CHROMA - {ai_msg}")