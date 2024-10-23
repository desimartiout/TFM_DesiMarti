#https://huggingface.co/blog/getting-started-with-embeddings

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import chromadb

# Step 1: Cargar el modelo de embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Puedes probar modelos más grandes si tu GPU lo soporta

# Textos de ejemplo
sentences = [
    "La inteligencia artificial está cambiando el mundo.",
    "El aprendizaje profundo es una rama del machine learning.",
    "FAISS permite búsquedas eficientes en grandes volúmenes de datos.",
    "ChromaDB facilita el almacenamiento y gestión de embeddings.",
    "Las GPUs aceleran el procesamiento de modelos de lenguaje."
]

# Generar los embeddings de las frases
embeddings = model.encode(sentences)

# Step 2: Almacenamiento en FAISS (usando GPU)
# Crear un índice FAISS que use la GPU
d = embeddings.shape[1]  # Dimensión de los embeddings
index = faiss.IndexFlatL2(d)  # L2 es la distancia euclidiana, puedes usar otras métricas como Cosine si prefieres
gpu_res = faiss.StandardGpuResources()  # Gestión de recursos de GPU
gpu_index = faiss.index_cpu_to_gpu(gpu_res, 0, index)  # Transferir el índice a la GPU

# Convertir los embeddings a formato numpy
embeddings = np.array(embeddings)

# Agregar los embeddings al índice
gpu_index.add(embeddings)

# Step 3: Almacenamiento de metadatos en ChromaDB
# Crear un cliente de ChromaDB y una colección
client = chromadb.Client()
collection = client.create_collection("embeddings_collection")

# Agregar documentos (frases) y embeddings a ChromaDB
collection.add(
    documents=sentences,          # Los textos originales
    embeddings=embeddings.tolist(),  # Convertimos los embeddings a lista
    ids=[str(i) for i in range(len(sentences))]  # IDs únicos para cada frase
)

# Step 4: Realizar una búsqueda en FAISS
# Buscar las 3 frases más cercanas a la primera frase (índice 0)
D, I = gpu_index.search(embeddings[:1], k=3)  # 'D' contiene las distancias, 'I' los índices

# Mostrar los resultados de la búsqueda
print("Indices de los resultados más cercanos:", I)
print("Distancias de los resultados más cercanos:", D)

# Obtener las frases correspondientes desde ChromaDB
result_docs = collection.get(ids=[str(idx) for idx in I[0]])
print("Frases más cercanas:")
for doc in result_docs['documents']:
    print(doc)

# Step 5: Realizar una consulta por contenido en ChromaDB
# Consultar por embeddings similares al embedding de la primera frase
query_result = collection.query(
    query_embeddings=[embeddings[0]],
    n_results=3
)

# Mostrar los resultados de la consulta
print("\nConsulta ChromaDB:")
for result in query_result['documents']:
    print(result)




""" from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama2",
    temperature=0,
    # other params...
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "Sistema",
            "Tu eres un Asistente virtual que ayuda a contestar a las dudas de los usuarios en vase al contenido que se te pasa por parámetro",
        ),
        ("contenido", "{result}"),
    ]
)

chain = prompt | llm
ai_msg = chain.invoke(
    {
        "contenido": "I love programming.",
    }
)
print(ai_msg) """


