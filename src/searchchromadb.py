import logging
import chromadb
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from langchain_ollama import OllamaLLM

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from src.utils import setup_logging
from src.constants import MOCK_IDS, MOCK_DOCUMENTS, MOCK_METADATAS, CHROMA_COLLECTION_NAME, CHROMA_PERSIST_PATH, CHROMA_NUMDOCUMENTS, SENTENCE_TRANSFORMER


# Inicializo el logger
setup_logging()
logger = logging.getLogger(__name__)

# Inicializar un modelo de Sentence Transformer para obtener embeddings
model = SentenceTransformer(SENTENCE_TRANSFORMER)  # Modelo open source para embeddings

def cargarDocumentosMOCK(collection):
    # Generamos embeddings manualmente a partor de objetos mockeados
    texts = [doc for doc in MOCK_DOCUMENTS]
    embeddings = model.encode(texts)  # Generar embeddings para la lista de textos

    collection.add(
        documents=MOCK_DOCUMENTS,
        metadatas=MOCK_METADATAS,
        ids=MOCK_IDS,
        embeddings=embeddings
    )
    #Si los ids son iguales los reemplaza


def cargarDocumento(documento, metadato, id):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))

    # collection = client.create_collection(
    #     name="collection_name",
    #     metadata={"hnsw:space": "cosine"} # l2 is the default
    # )
    # Valid options for hnsw:space are "l2", "ip, "or "cosine". The default is "l2" which is the squared L2 norm.
    # https://docs.trychroma.com/guides
    # Selección recomendada según el caso de uso:
    # Tipo de datos	Recomendación (hnsw:space)
    # Embeddings de texto	cosine
    # Embeddings de imágenes	l2
    # Embeddings de productos	ip (normalizados)
    # Datos de características tabulares	l2 o manhattan
    # Casos personalizados	Experimentar con varios
    
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

    embeddings = model.encode([documento])  # Generar embeddings para la lista de textos

    #TODO: Hay que arreglar lo de los metadatos, espera un diccionario  -> array json con par clave valor
    collection.add(
        documents=[documento],
        metadatas=None,
        ids=[id],
        embeddings=embeddings
    )

# Función para obtener todos los documentos
def get_all_documents():
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME,)

    #Si no tengo documentos cargados los moqueo para poder tener datos.
    #if (collection.count()==0):
        #cargarDocumentosMOCK(collection)

    #Prueba de agregar un solo documento.   
    #cargarDocumento("documento","medatadooooooosss","id_1")
    
    #Listar los documentos de la colección
    logger.info(f"SEARCH_CHROMA - Documentos en la colección {collection.count()}")

    documents = collection.get()

    # Display the documents
    for ids in documents['ids']:
        logger.info(f"SEARCH_CHROMA - Id {ids}")

    return documents

# Función para realizar una consulta (simulando una búsqueda por texto)
def query_documents(query_text: str, top_k: int = CHROMA_NUMDOCUMENTS):
    client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH, settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)
    #Si no tengo documentos cargados los moqueo para poder tener datos.
    #if (collection.count()==0):
        #cargarDocumentosMOCK(collection)
  
    #Listar los documentos de la colección
    logger.info(f"SEARCH_CHROMA - Documentos en la colección {collection.count()}")
    #collection = client.get_collection(CHROMA_COLLECTION_NAME)
  
    # Generar el embedding para la consulta
    query_embedding = model.encode([query_text]).tolist()

    logger.info(f"SEARCH_CHROMA - Previo a consulta")

    # Realizar una búsqueda de similitud
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )


    logger.info(f"SEARCH_CHROMA - resultados: {results}")

    return results


# def query_documents(query_text: str, top_k: int = CHROMA_NUMDOCUMENTS, similarity_threshold: float = 0.8):
#     # Crear cliente persistente
#     client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)
#     collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

#     # Verificar si hay documentos cargados
#     logger.info(f"SEARCH_CHROMA - Documentos en la colección {collection.count()}")

#     # Preprocesar la consulta
#     preprocessed_query = preprocess_text(query_text)
    
#     # Generar el embedding para la consulta
#     query_embedding = model.encode([preprocessed_query]).tolist()
    
#     # Realizar una búsqueda de similitud
#     results = collection.query(
#         query_embeddings=query_embedding,
#         n_results=top_k
#     )

#     logger.info(f"SEARCH_CHROMA - results {results}")
    
#     # Filtrar resultados según umbral de similitud
#     filtered_results = [
#         result for result in results['documents'] 
#         if result['score'] >= similarity_threshold
#     ]

#     logger.info(f"SEARCH_CHROMA - Resultados filtrados: {len(filtered_results)}")
#     logger.info(f"SEARCH_CHROMA - results {filtered_results}")

#     return filtered_results

# def preprocess_text(text: str) -> str:
#     # Limpieza básica del texto
#     return text.lower().strip()

# OTROS MÉTODOS QUE AHORA NO SE UTILIZAN PERO PARA LAS PRUEBAS INICIALES FUERON ÚTILES

# Método para consultar en la base de datos vectorial
def consultaChromadb(query_text, top_k, similarity_threshold: float = 1.0):
    logger.info(f"SEARCH_CHROMA - query_text: {query_text}")
    results = query_documents(query_text, top_k)
    contexto = ""

    logger.info(f"SEARCH_CHROMA - results {results}:")
    # Mostrar resultados de la consulta
    # for result in results["documents"]:
    #     for texto in result:
    #         #print(result)
    #         contexto += f"Convocatoria: {texto}\n"
    
    for i in range(len(results["documents"])):
        result = results["documents"][i]
        logger.info(f"SEARCH_CHROMA - distances {results['distances'][i]}:")
        for j in range(len(result)):
            if results['distances'][i][j] <= similarity_threshold:
                logger.info(f"SEARCH_CHROMA - {results['distances'][i][j]}:")    
                texto = result[j]
                contexto += f"Convocatoria: {texto}\n"

    logger.info(f"SEARCH_CHROMA - Contexto {contexto}:")

    return contexto

# #Método para consultar en la bd vectorial y con el resultado ir al LLM a completar la contestación de una forma básica
# def consultaBasica_NOUSO(query_text: str, top_k: int = 5):
#     logger.info(f"SEARCH_CHROMA - query_text: {query_text}")
#     contexto = consultaChromadb(query_text, top_k)

#     #Consulta básica sin Prompt
#     llm = OllamaLLM(model=OLLAMA_MODEL_NAME, temperature=OLLAMA_TEMPERATURE)
#     prompt = f"Usando esta información: {contexto} \n Responde: {query_text}]"
#     #Basada en el resultado de ChromaDB
#     respuesta = llm(prompt)

#     # Imprimir la respuesta
#     logger.info(f"SEARCH_CHROMA - Prompt: {prompt}")
#     # Imprimir la respuesta
#     logger.info(f"SEARCH_CHROMA - Respuesta: {respuesta}")

# #Método para consultar en la bd vectorial y con el resultado ir al LLM a completar la contestación mediante prompt
# def consultaPrompt_NOUSO(query_text: str, top_k: int = 5):
#     contexto = consultaChromadb(query_text, top_k)

#     llm = ChatOllama(
#         model=OLLAMA_MODEL_NAME,
#         temperature=OLLAMA_TEMPERATURE,
#     )

#     prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 "Tu eres un asistente virtual para contestar a ayudas públicas del gobierno de españa, te adjuntaré una información que debes usar para proporcionar la respuesta. No te inventes información que no esté en esta información.",
#             ),
#             ("human", "{input}"),
#         ]
#     )

#     queryContext = f"Usando esta información: {contexto}. Responde: {query_text}" 

#     chain = prompt | llm
#     ai_msg = chain.invoke(
#         {
#             "input": f"{queryContext}",
#         }
#     )
#     logger.info(f"SEARCH_CHROMA - queryContext: {queryContext}")
#     logger.info(f"SEARCH_CHROMA - {ai_msg}")