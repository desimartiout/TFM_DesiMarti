import os
import yaml
import faiss
import json
from sentence_transformers import SentenceTransformer


# Modelo para embeddings
modelo = SentenceTransformer("all-MiniLM-L6-v2")  

# Rutas de archivos para índice y metadatos
INDEX_FILE = "/faiss/mi_indice_faiss.index"
METADATA_FILE = "/faiss/metadatos.json"

def cargar_indice_y_metadatos():
    """Carga el índice FAISS y los metadatos si existen. Si no, los crea."""
    if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(METADATA_FILE, "r") as f:
            metadatos = json.load(f)
    else:
        # Crear índice vacío
        index = faiss.IndexFlatL2(384)  # Dimensión por defecto de all-MiniLM-L6-v2
        metadatos = {}
    return index, metadatos

def guardar_indice_y_metadatos(index, metadatos):
    """Guarda el índice FAISS y los metadatos en disco."""
    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "w") as f:
        json.dump(metadatos, f)
    print("Índice y metadatos guardados correctamente.")

def agregar_documentos(nuevos_documentos):
    """Agrega nuevos documentos al índice FAISS y actualiza los metadatos."""
    # Cargar índice y metadatos existentes
    index, metadatos = cargar_indice_y_metadatos()

    # Procesar nuevos documentos
    textos = [doc["texto"] for doc in nuevos_documentos]
    embeddings = modelo.encode(textos)

    # Añadir nuevos embeddings al índice
    index.add(embeddings)

    # Actualizar metadatos
    nuevo_id_base = len(metadatos)  # Continuar desde el último ID
    for i, doc in enumerate(nuevos_documentos):
        metadatos[nuevo_id_base + i] = doc

    # Guardar los cambios
    guardar_indice_y_metadatos(index, metadatos)
    print(f"{len(nuevos_documentos)} documentos añadidos correctamente.")

def agregar_documentos2(documento):
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

def realizar_consulta(consulta, k=2):
    """Realiza una consulta en el índice FAISS y devuelve los resultados."""
    # Cargar índice y metadatos
    index, metadatos = cargar_indice_y_metadatos()

    # Generar embedding para la consulta
    consulta_embedding = modelo.encode([consulta])

    # Buscar los K resultados más cercanos
    distancias, indices = index.search(consulta_embedding, k)

    print("\nResultados de la búsqueda:")
    for i, indice in enumerate(indices[0]):
        if indice != -1:
            # print(f"- Documento {metadatos[str(indice)]['id']} (distancia: {distancias[0][i]}):")
            print(f"- Documento {metadatos[str(indice)]} (distancia: {distancias[0][i]}):")
            # print(f"  {metadatos[str(indice)]['texto']}")

def yaml_to_paragraph(yaml_data):
    try:
        data = yaml.safe_load(yaml_data)
    except Exception as e:
        print(f'Error al parsear el yaml: {e}')
    
    # Extraemos y construimos el párrafo
    paragraph = (
        f"ayuda {data.get('Detalle de la convocatoria de ayuda o  subvención')}: "
        f"{data.get('Tipo de ayuda', 'Tipo de ayuda no especificada')} de {data.get('Órgano, comunidad, autonomía, provincia o ayuntamiento convocante')}, "
        f" destinada {data.get('Finalidad', 'un propósito no especificado')}, presupuesto {data.get('Presupuesto total', 'no indicado')} euros. "
        f" dirigida {data.get('Tipos de beneficiarios', 'beneficiarios no especificados')} sector {data.get('Sectores involucrados', 'sector no indicado')} "
        f" región {data.get('Región de impacto', 'región no especificada')}. "
        f" convocatoria {data.get('Tipo de convocatoria', 'tipo no indicado')} "
        f"{'No está abierta' if not data.get('Estado de convocatoria abierta', False) else 'Está abierta'}"
    )

    return paragraph

def cargarDocumentosYaml(directory_path):
    """
    Recorre todos los archivos YAML en un directorio, lee su contenido
    y devuelve una lista de diccionarios con los datos.

    Args:
        directory_path (str): Ruta del directorio que contiene los archivos YAML.

    Returns:
        list: Lista de diccionarios con el contenido de los archivos YAML.
    """
    yaml_data_list = []

    # Recorre todos los archivos del directorio
    for filename in os.listdir(directory_path):
        if filename.endswith(".yaml") or filename.endswith(".yml"):  # Verifica si es un archivo YAML
            file_path = os.path.join(directory_path, filename)
            
            # Lee el contenido del archivo YAML
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    yaml_content = yaml.safe_load(file)
                    yaml_string = yaml.dump(yaml_content, default_flow_style=False, allow_unicode=True)
                    print(f"yaml_string {yaml_string}")
                    yaml_data_list.append({'filename': filename, 'content': yaml_string})
            except Exception as e:
                print(f"Error al leer el archivo {filename}: {e}")
    
    return yaml_data_list

# Ejemplo de uso
if __name__ == "__main__":
    # # Agregar documentos nuevos
    # nuevos_documentos = [
    #     {"id": 1, "texto": "El gobierno anuncia nuevas ayudas para viviendas."},
    #     {"id": 2, "texto": "Se abre el plazo de solicitud para subvenciones agrícolas."}
    # ]
    # agregar_documentos(nuevos_documentos)

    # # Agregar más documentos
    # nuevos_documentos = [
    #     {"id": 3, "texto": "Subvenciones disponibles para empresas tecnológicas."},
    #     {"id": 4, "texto": "Nueva convocatoria de ayudas al emprendimiento juvenil."}
    # ]
    # agregar_documentos(nuevos_documentos)

    cadena1 ="""Detalle de la convocatoria de ayuda o subvención: 802597
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/802597
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: VIMIANZO - AYUNTAMIENTO DE VIMIANZO
    Enlace / url a sede electrónica presentación ayuda: 
    Fecha de recepción: 2024-12-12T13:32:59+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 16000 Euros
    Descripción: BASES REGULADORAS DE LA CONVOCATORIA DE SUBVENCIONES PARA EL FOMENTO DE ACTIVIDADES CULTURALES Y SOCIALES DEL AÑO 2024 MEDIANTE CONCURRENCIA COMPETITIVA
    Tipos de beneficiarios: PERSONAS JURÍDICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: ACTIVIDADES ARTÍSTICAS, RECREATIVAS Y DE ENTRETENIMIENTO
    Región de impacto: ES111 - A Coruña
    Finalidad: Cultura
    Bases reguladoras: BASES REGULADORAS DA CONVOCATORIA ORDINARIA DE SUBVENCIÓNS PARA O FOMENTO DE ACTIVIDADES CULTURAIS E SOCIAIS DO ANO 2024 MEDIANTE CONCORRENCIA COMPETITIVA
    URL Bases Reguladoras: https://bop.dacoruna.gal/bopportal/publicado/2024/12/11/2024_0000008806.pdf
    Publicación en diario oficial: Sí
    Estado de convocatoria abierta: No
    Fecha de inicio de solicitudes: 
    Fecha de fin de solicitudes: 
    Inicio de convocatoria: DESDE EL DÍA SIGUIENTE A LA PUBLICACIÓN DEL ESTRACTO EN EL BOP
    Fin de convocatoria: DIEZ DÍAS HÁBILES A CONTAR DESDE EL DÍA SIGUIENTE A LA PUBLICACIÓN DEL EXTRACTO EN EL BOP
    Reglamento: 
    Otros documentos de la convocatoria: 
    Descripción: Documento de la convocatoria en lengua cooficial, Nombre: 2024_SUBV CULTURAL.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/802597/document/1175695 , 
    Descripción: Documento de la convocatoria en español, Nombre: 2024_SUBV CULTURAL.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/802597/document/1175691
    """

    cadena2 ="""Detalle de la convocatoria de ayuda o  subvención: 802040
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/802040
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: CABILDO INSULAR DE FUERTEVENTURA - CABILDO INSULAR DE FUERTEVENTURA
    Enlace / url a sede electrónica presentación ayuda: 
    Fecha de recepción: 2024-12-11T09:41:55+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 1200000 Euros
    Descripción: Convocatoria Pública de Subvenciones Genéricas, en régimen de concurrencia competitiva, en materia de ganadería, Línea 4: Subvenciones para el fomento de la recría ganadera de Fuerteventura, del Cabildo Insular de Fuerteventura, anualidad 2024
    Tipos de beneficiarios: PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: AGRICULTURA, GANADERÍA, SILVICULTURA Y PESCA
    Región de impacto: ES704 - Fuerteventura
    Finalidad: Agricultura, Pesca y Alimentación
    Bases reguladoras: BASES REGULADORAS para la tramitación y concesión de subvenciones en materia de agricultura, ganadería y pesca de Fuerteventura
    URL Bases Reguladoras: https://www.boplaspalmas.net/boletines/2024/18-09-24/18-09-24.pdf
    Publicación en diario oficial: Sí
    Estado de convocatoria abierta: No
    Fecha de inicio de solicitudes: 
    Fecha de fin de solicitudes: 
    Inicio de convocatoria: AL DIA SIGUIENTE DE LA PUBLICACIÓN DEL EXTRACTO DE LA CONVOCATORIA EN EL BOLETÍN
    Fin de convocatoria: 10 DÍAS DESPUÉS DE SU PUBLICACIÓN
    Reglamento: 
    Otros documentos de la convocatoria: 
    Descripción: Texto en castellano de la convocatoria, Nombre: CONVOCATORIA_DE_SUBVENCIONES_EN_MATERIA_DE_GANADERÍA._LINEA_4_FOMENTO_DE_LA_RECRÍA_GANADERA.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/802040/document/1174297 
    """

    # agregar_documentos2("El gobierno anuncia nuevas ayudas para viviendas.")
    # agregar_documentos2("Nueva convocatoria de ayudas al emprendimiento juvenil.")
    # agregar_documentos2(cadena1)
    # agregar_documentos2(cadena2)

    # Ejemplo de uso
    yaml_text = """
    Detalle de la convocatoria de ayuda: 802040
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/802040
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: CABILDO INSULAR DE FUERTEVENTURA - CABILDO INSULAR DE FUERTEVENTURA
    Fecha de recepción: 2024-12-11T09:41:55+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 1200000 Euros
    Descripción: Convocatoria Pública de Subvenciones Genéricas, en régimen de concurrencia competitiva, en materia de ganadería, 
    Línea 4: Subvenciones para el fomento de la recría ganadera de Fuerteventura, del Cabildo Insular de Fuerteventura, anualidad 2024
    Tipos de beneficiarios: PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: AGRICULTURA, GANADERÍA, SILVICULTURA Y PESCA
    Región de impacto: ES704 - Fuerteventura
    Finalidad: Agricultura, Pesca y Alimentación
    URL Bases Reguladoras: https://www.boplaspalmas.net/boletines/2024/18-09-24/18-09-24.pdf
    Estado de convocatoria abierta: No
    Inicio de convocatoria: AL DIA SIGUIENTE DE LA PUBLICACIÓN DEL EXTRACTO DE LA CONVOCATORIA EN EL BOLETÍN
    Fin de convocatoria: 10 DÍAS DESPUÉS DE SU PUBLICACIÓN
    """

    # Convertimos el YAML a párrafo
    # paragraph = yaml_to_paragraph(yaml_text)
    # agregar_documentos2(paragraph)


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
    realizar_consulta("¿que ayudas hay en Valencia?", k=5)
