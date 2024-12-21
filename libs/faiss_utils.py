import os
import yaml
import faiss
import numpy as np
import json
import logging
from sentence_transformers import SentenceTransformer
from datetime import datetime
from config.faiss.faiss_config import INDEX_FILE_FAISS, METADATA_FILE_FAISS, LOG_FILE_PATH_FAISS, MODELO_EMBED_FAISS

# Modelo para embeddings
modelo = SentenceTransformer(MODELO_EMBED_FAISS)

def setup_logging() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
    ruta_log = ruta_actual + LOG_FILE_PATH_FAISS

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}_1.log")

    # print(f"Ruta: {log_file_path}")

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

def cargar_indice_y_metadatos():
    """Carga el índice FAISS y los metadatos si existen. Si no, los crea."""
    # print(INDEX_FILE_FAISS)
    # print(METADATA_FILE_FAISS)
    if os.path.exists(INDEX_FILE_FAISS) and os.path.exists(METADATA_FILE_FAISS):
        index = faiss.read_index(INDEX_FILE_FAISS)
        with open(METADATA_FILE_FAISS, "r", encoding='utf-8') as f:
            metadatos = json.load(f)
    else:
        # Crear índice vacío
        index = faiss.IndexFlatL2(384)  # Dimensión por defecto de all-MiniLM-L6-v2
        metadatos = {}
    return index, metadatos

def guardar_indice_y_metadatos(index, metadatos):
    """Guarda el índice FAISS y los metadatos en disco."""
    faiss.write_index(index, INDEX_FILE_FAISS)
    with open(METADATA_FILE_FAISS, "w", encoding='utf-8') as f:
        json.dump(metadatos, f, ensure_ascii=False, indent=4)
    print("Índice y metadatos guardados correctamente.")

def agregar_documento(documento):
    """Agrega nuevos documentos al índice FAISS y actualiza los metadatos."""
    # Cargar índice y metadatos existentes
    index, metadatos = cargar_indice_y_metadatos()

    # Procesar nuevos documentos
    textos = [documento]
    embeddings = modelo.encode(textos)
    
    # Añadir nuevos embeddings al índice
    index.add(embeddings)

    # Actualizar metadatos
    nuevo_id_base = len(metadatos)-1  # Continuar desde el último ID

    metadatos[nuevo_id_base + 1] = documento

    # Guardar los cambios
    guardar_indice_y_metadatos(index, metadatos)

def realizar_consulta_old(consulta, k=2):
    """Realiza una consulta en el índice FAISS y devuelve los resultados."""
    # Cargar índice y metadatos
    index, metadatos = cargar_indice_y_metadatos()

    # Generar embedding para la consulta
    consulta_embedding = modelo.encode([consulta])

    # Buscar los K resultados más cercanos
    distancias, indices = index.search(consulta_embedding, k)

    logging.info("\nResultados de la búsqueda: realizar_consulta_old")
    for i, indice in enumerate(indices[0]):
        if indice != -1:
            # print(f"- Documento {metadatos[str(indice)]['id']} (distancia: {distancias[0][i]}):")
            logging.info(f"- Documento {metadatos[str(indice)]} (distancia: {distancias[0][i]}):")
            # print(f"  {metadatos[str(indice)]['texto']}")

def realizar_consulta(consulta, k=2):
    """Realiza una consulta en el índice FAISS y devuelve los resultados."""
    # Cargar índice y metadatos
    index, metadatos = cargar_indice_y_metadatos()

    # Generar embedding para la consulta
    consulta_embedding = modelo.encode([consulta])

    # Buscar los K resultados más cercanos
    distancias, indices = index.search(consulta_embedding, k)

    documents = []

    logging.info("\nResultados de la búsqueda: realizar_consulta")
    for i, indice in enumerate(indices[0]):
        if indice != -1:
            documents.append(metadatos[str(indice)])
    
    logging.info(f"Documentos: {len(documents)}")
    return documents

# Método para consultar en la base de datos vectorial
def consultaFaiss(query_text, top_k):
    logger.info(f"SEARCH FAISS - query_text: {query_text}")
    # Cargar índice y metadatos
    index, metadatos = cargar_indice_y_metadatos()

    # Generar embedding para la consulta
    consulta_embedding = modelo.encode([query_text])

    # Buscar los K resultados más cercanos
    distancias, indices = index.search(consulta_embedding, top_k)

    documents = []

    contexto = ""

    logger.info(f"SEARCH FAISS - results:")
    for i, indice in enumerate(indices[0]):
        if indice != -1:
            logging.info(f"- Documento {metadatos[str(indice)]} (distancia: {distancias[0][i]}):")
            documents.append(metadatos[str(indice)])
            contexto += f"{metadatos[str(indice)]}\n"

    logger.info(f"SEARCH FAISS - Contexto {contexto}:")

    return contexto

def obtener_todos_documentos():
    # Cargar índice y metadatos
    index, metadatos = cargar_indice_y_metadatos()
    
    documents = []

    # Recuperamos todos los documentos basados en los índices obtenidos
    for i in range(0,index.ntotal):
        documents.append(metadatos[str(i)])

    return documents

# # Ejemplo de uso
# directory_path = "./scrapping/Documentos"  # Cambia esta ruta al directorio que contiene tus archivos YAML
# yaml_files_data = cargarDocumentosYaml(directory_path)

# print(f"Archivos: {len(yaml_files_data)}")
# # Imprime el contenido de los archivos leídos
# for file_data in yaml_files_data:
#     print(f"Archivo: {file_data['filename']}")
#     # print(f"Contenido: {file_data['content']}")
#     paragraph = yaml_to_paragraph(file_data['content'])
#     agregar_documentos2(paragraph)

# Realizar consulta
# realizar_consulta("¿que ayudas hay en Valencia?", k=5)