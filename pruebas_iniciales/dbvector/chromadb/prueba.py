import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import numpy as np

# Crear una instancia de ChromaDB con una configuración persistente
#client = chromadb.Client(Settings(persist_directory="./store/"))
client = chromadb.PersistentClient(path="./store/")

# Definir un conjunto de datos de ejemplo (documentos)
documents = [
    {"id": "4", "text": "Este es el primer docum."},
    {"id": "5", "text": "El segundo documento traico."},
    {"id": "6", "text": "Este es  redes neuronales."},
]


""" collection.add(
    documents=[
        "This is a document about machine learning",
        "This is another document about data science",
        "A third document about artificial intelligence"
    ],
    metadatas=[
        {"source": "test1"},
        {"source": "test2"},
        {"source": "test3"}
    ],
    ids=[
        "id1",
        "id2",
        "id3"
    ]
) """



# Inicializar un modelo de Sentence Transformer para obtener embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Función para listar todos los documentos de una colección
def list_documents(client, collection_name):
    collection = client.get_or_create_collection(collection_name)
    documents = collection.get()  # Obtener todos los documentos
    return documents

# Función para insertar documentos en la base de datos
def add_documents(client, collection_name, documents):
    # Crear o acceder a una colección
    collection = client.get_or_create_collection(name=collection_name)
    
    # Crear embeddings para los textos
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts).tolist()  # Convierte los embeddings a listas
    
    # Insertar los documentos en la colección solo si no existen
    for doc in documents:
        # Comprobar si el documento ya está en la base de datos
        existing_doc = collection.get(ids=[doc["id"]])
        if existing_doc["documents"]:
            print(f"El documento con ID {doc['id']} ya existe, no se agregará de nuevo.")
        else:
            collection.add(
                documents=[doc["text"]],
                metadatas=[{"source": "manual"}],
                ids=[doc["id"]],
                embeddings=[embeddings[documents.index(doc)]]
            )
            print(f"Documento con ID {doc['id']} agregado.")

# Función para eliminar un documento de la base de datos de forma persistente
def delete_document(client, collection_name, doc_id):
    # Acceder a la colección
    collection = client.get_collection(collection_name)
    
    # Eliminar el documento por su ID
    collection.delete(ids=[doc_id])
    print(f"Documento con ID {doc_id} eliminado.")

# Función para realizar una consulta (simulando una búsqueda por texto)
def query_documents(client, collection_name, query_text):
    collection = client.get_collection(collection_name)
    
    # Generar el embedding para la consulta
    query_embedding = model.encode([query_text]).tolist()
    
    # Realizar una búsqueda de similitud
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    return results

# Nombre de la colección
collection_name = "documentos_ai"

documents = list_documents(client, collection_name)

# Añadir documentos solo si no existen
add_documents(client, collection_name, documents)

# Realizar una consulta
query_text = "aprendizaje automático"
results = query_documents(client, collection_name, query_text)

# Mostrar resultados de la consulta
print("Resultados de la consulta:")
for result in results["documents"]:
    print(result)

# Eliminar un documento (ID = "2")
delete_document(client, collection_name, "2")

# Verificar la eliminación
print("\nResultados después de eliminar el documento con ID = 2:")
results_after_deletion = query_documents(client, collection_name, query_text)
for result in results_after_deletion["documents"]:
    print(result)
