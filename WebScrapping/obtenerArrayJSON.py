import json
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

import os

# Establecer la variable de entorno para evitar el error
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# Suponiendo que este es tu array de JSON
data_array = [
    {
        "id": 992327,
        "descripcion": "Convocatoria de ayudas para alquiler...",
        "descripcionFinalidad": "Acceso a la vivienda."
    },
    {
        "id": 992328,
        "descripcion": "Convocatoria de ayudas para mejoras de viviendas...",
        "descripcionFinalidad": "Fomento de la edificación."
    }
]

# Inicializar el tokenizer y modelo
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embeddings

# Inicializar el índice FAISS
index = faiss.IndexFlatL2(768)  # BERT produce embeddings de dimensión 768
json_references = []  # Para almacenar las referencias a los JSON

# Iterar sobre el array de JSON
for item in data_array:
    # Convertir la descripción en un embedding
    embedding = get_embedding(item["descripcion"], tokenizer, model)
    
    # Almacenar el embedding en FAISS
    index.add(np.array([embedding]))
    
    # Guardar la referencia al JSON usando su ID
    json_references.append(item["id"])

print("Embeddings almacenados con las siguientes referencias:", json_references)

# Ejemplo de búsqueda en la base de datos vectorial
def search(query_text, k=1):
    query_embedding = get_embedding(query_text, tokenizer, model)
    D, I = index.search(np.array([query_embedding]), k)  # Buscar el k embedding más cercano
    closest_index = I[0][0]  # Índice del embedding más cercano
    closest_json_id = json_references[closest_index]  # Recuperar el ID del JSON
    return closest_json_id

# Ejemplo de búsqueda
query = "mejoras de viviendas"
result_id = search(query)
print(f"El ID del JSON más relevante es: {result_id}")
