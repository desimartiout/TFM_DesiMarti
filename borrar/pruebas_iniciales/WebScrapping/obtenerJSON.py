import json
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

import os

# Establecer la variable de entorno para evitar el error
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# JSON de ejemplo (sustituir por tu JSON)
data = {
    "id": 992327,
    "organo": {
        "nivel1": "GANDIA",
        "nivel2": "AYUNTAMIENTO DE GANDIA",
        "nivel3": None
    },
    "descripcion": "2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual...",
    "descripcionFinalidad": "Acceso a la vivienda y fomento de la edificación"
}

# 1. Convertir el campo "descripcion" en embeddings usando BERT
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
model = AutoModel.from_pretrained("bert-base-uncased")

def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embeddings

# Convertimos la descripción en embedding
text = data["descripcion"]
embedding = get_embedding(text, tokenizer, model)

# 2. Crear un índice FAISS y almacenar el embedding
dimension = embedding.shape[0]  # La dimensión del embedding
index = faiss.IndexFlatL2(dimension)  # Índice FAISS usando L2 como métrica
index.add(np.array([embedding]))  # Añadimos el embedding al índice

# Guardar la referencia al JSON (puedes usar el campo 'id' como referencia)
json_references = [data["id"]]

print(f"Embedding almacenado con referencia al JSON ID: {data['id']}")

# 3. Ejemplo de búsqueda en la base de datos vectorial
def search(query_text, k=1):
    query_embedding = get_embedding(query_text, tokenizer, model)
    D, I = index.search(np.array([query_embedding]), k)  # Buscar el k embedding más cercano
    closest_index = I[0][0]  # Índice del embedding más cercano
    closest_json_id = json_references[closest_index]  # Recuperar el ID del JSON
    return closest_json_id

# Ejemplo de búsqueda
query = "ayudas para alquiler de viviendas"
result_id = search(query)
print(f"********")
print(f"El ID del JSON más relevante es: {result_id}")
