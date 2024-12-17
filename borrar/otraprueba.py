import faiss
import json

# Guardar índice y metadatos
index = faiss.IndexFlatL2(128)
metadatos = {0: "vector_1", 1: "vector_2"}

faiss.write_index(index, "mi_indice_faiss.index")
with open("metadatos.json", "w") as f:
    json.dump(metadatos, f)

# Recuperar índice y metadatos
index = faiss.read_index("mi_indice_faiss.index")
with open("metadatos.json", "r") as f:
    metadatos = json.load(f)