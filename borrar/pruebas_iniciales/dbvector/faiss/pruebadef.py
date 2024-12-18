import faiss
import json
from sentence_transformers import SentenceTransformer

# 1. Crear representaciones vectoriales de los documentos
modelo = SentenceTransformer("all-MiniLM-L6-v2")  # Modelo para embeddings

documentos = [
    {"id": 1, "texto": "El gobierno anuncia nuevas ayudas para viviendas."},
    {"id": 2, "texto": "Se abre el plazo de solicitud para subvenciones agrícolas."},
    {"id": 3, "texto": "Se plazo de solicitud para subvenciones agrícolas."},
    {"id": 4, "texto": "Se abre de solicitud para subvenciones agrícolas."},
    {"id": 5, "texto": "Se abre el plazo para subvenciones agrícolas."},
    {"id": 6, "texto": "Se abre el plazo de solicitud ."},
    {"id": 7, "texto": "Se abre el plazo de solicitud para subvenciones viviendas viviendas."}
]

# Generar los embeddings
textos = [doc["texto"] for doc in documentos]
embeddings = modelo.encode(textos)

# 2. Crear el índice FAISS
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)  # L2 = Distancia euclidiana
index.add(embeddings)  # Añadir los embeddings al índice

# Asociar metadatos a los IDs (FAISS solo almacena los vectores)
metadatos = {i: documentos[i] for i in range(len(documentos))}

# 3. Guardar el índice y los metadatos en disco
faiss.write_index(index, "mi_indice_faiss.index")
with open("metadatos.json", "w") as f:
    json.dump(metadatos, f)

print("Índice y metadatos guardados correctamente.")

# 4. Recuperar el índice y los metadatos
index = faiss.read_index("mi_indice_faiss.index")
with open("metadatos.json", "r") as f:
    metadatos = json.load(f)

print("Índice y metadatos cargados correctamente.")

# 5. Realizar una consulta
consulta = "¿Hay subvenciones disponibles para viviendas?"
consulta_embedding = modelo.encode([consulta])

# Buscar los K resultados más cercanos
K = 2  # Número de resultados más cercanos
distancias, indices = index.search(consulta_embedding, K)

print("\nResultados de la búsqueda:")
for i, indice in enumerate(indices[0]):
    if indice != -1:
        print(f"- Documento {metadatos[str(indice)]['id']} (distancia: {distancias[0][i]}):")
        print(f"  {metadatos[str(indice)]['texto']}")
