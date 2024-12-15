import logging
import time
import json
from string import Template
import requests
import os
from collections import defaultdict
from utils import setup_logging_scrap
from constantes import URL_CONVOCATORIA, URL_CONVOCATORIA_POST, TEMPLATE_DOC, URL_BASE_API, RUTA_DESTINO_DOCUMENTOS, PAGE_SIZE, TOTAL_PAGES

import sys
from pathlib import Path

# Añadir el directorio padre a sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from libs.chromadb_utils import cargarDocumento

def descargar_y_guardar_json_por_id(elemento, carpeta_destino):
    """Descarga el JSON de una URL usando el id del elemento y lo guarda en una carpeta destino."""
    url = URL_CONVOCATORIA + f"{elemento['numeroConvocatoria']}" + URL_CONVOCATORIA_POST  # Cambiamos la URL base según corresponda

    try:
        logging.info(url)
        response = requests.get(url)
        response.raise_for_status()  # Genera una excepción para códigos de error HTTP
        json_data = response.json()
        
        # Crear la carpeta si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        numConvocatoria = elemento['numeroConvocatoria']
        
        # Guardar el JSON descargado en un archivo
        archivo_destino = os.path.join(carpeta_destino, f"{numConvocatoria}.json")
        with open(archivo_destino, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        logging.info(f"Datos guardados en {archivo_destino}")

        json_aplanado = aplanar_json(json_data)
        archivo_destino_aplanado = os.path.join(carpeta_destino, f"{numConvocatoria}_aplanado.json")
        with open(archivo_destino_aplanado, 'w', encoding='utf-8') as f:
            json.dump(json_aplanado, f, ensure_ascii=False, indent=4)
            
        logging.info(f"Datos guardados en {archivo_destino_aplanado}")

        # Generar texto en yaml
        formatted_text = convert_json_to_yaml(json_aplanado, TEMPLATE_DOC)
        logging.info(formatted_text)
        archivo_destino = os.path.join(carpeta_destino, f"{numConvocatoria}.yaml")
        if formatted_text!= None:
            with open(archivo_destino, 'w', encoding='utf-8') as archivo:        
                archivo.write(formatted_text)
            logging.info(f"Datos guardados en {archivo_destino}")

        logging.info(f"Vamos a cargar el documento en chromadb {numConvocatoria}")

        cargarDocumento(formatted_text,json_aplanado,numConvocatoria)

        logging.info("Documento cargado correctamente")
        
    except requests.RequestException as e:
        logging.error(f"Error al descargar el JSON para ID {numConvocatoria}: {e}")
    except json.JSONDecodeError:
        logging.error(f"Error al decodificar el JSON descargado para ID {numConvocatoria}.")


# Función para convertir `None` en vacío
def safe_value(value):
    if value is None:
        return ""
    elif isinstance(value, bool):
        return "Sí" if value else "No"
    return value

def safe_value_inner(data, value, field):
    if data.get(value, {}) is None:
        return ""
    return data.get(value, {}).get("descripcion")

def aplanar_json(data):
    return defaultdict(
        str,  # Devuelve cadena vacía si falta alguna clave
        {
            "id": safe_value(data.get("id")),
            "organo_nivel1": safe_value(data.get("organo", {}).get("nivel1")),
            "organo_nivel2": safe_value(data.get("organo", {}).get("nivel2")),
            "sedeElectronica": safe_value(data.get("sedeElectronica")),
            "codigoBDNS": safe_value(data.get("codigoBDNS")),
            "fechaRecepcion": safe_value(data.get("fechaRecepcion")),
            "instrumentos": ", ".join(
                safe_value(i.get("descripcion")) for i in data.get("instrumentos", [])
            ),
            "tipoConvocatoria": safe_value(data.get("tipoConvocatoria")),
            "presupuestoTotal": safe_value(data.get("presupuestoTotal")),
            "descripcion": safe_value(data.get("descripcion")),
            "tiposBeneficiarios": ", ".join(
                safe_value(t.get("descripcion"))
                for t in data.get("tiposBeneficiarios", [])
            ),
            "sectores": ", ".join(
                safe_value(s.get("descripcion")) for s in data.get("sectores", [])
            ),
            "regiones": ", ".join(
                safe_value(r.get("descripcion")) for r in data.get("regiones", [])
            ),
            "descripcionFinalidad": safe_value(data.get("descripcionFinalidad")),
            "descripcionBasesReguladoras": safe_value(
                data.get("descripcionBasesReguladoras")
            ),
            "urlBasesReguladoras": safe_value(data.get("urlBasesReguladoras")),
            "sePublicaDiarioOficial": safe_value(data.get("sePublicaDiarioOficial")),
            "abierto": safe_value(data.get("abierto")),
            "fechaInicioSolicitud": safe_value(data.get("fechaInicioSolicitud")),
            "fechaFinSolicitud": safe_value(data.get("fechaFinSolicitud")),
            "textInicio": safe_value(data.get("textInicio")),
            "textFin": safe_value(data.get("textFin")),
            "reglamento": safe_value(
                safe_value_inner(data,"reglamento","descripcion")
            ),
            "documentos": ", ".join(
                f"\nDescripción: {safe_value(d.get('descripcion'))}, "
                f"Nombre: {safe_value(d.get('nombreFic'))}, "
                f"Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/{safe_value(data.get('codigoBDNS'))}/document/{safe_value(d.get('id'))} "
                for d in data.get("documentos", [])
            ),
        },
    )

# def convert_json_to_dict(json_aplanado)
#     return {
#         "id": data["id"],
#         "organo_nivel1": data["organo_nivel1"],
#         "organo_nivel2": data["organo_nivel2"],
#         "sedeElectronica": data["sedeElectronica"] if data["sedeElectronica"] else None,
#         "codigoBDNS": data["codigoBDNS"],
#         "fechaRecepcion": data["fechaRecepcion"],
#         "instrumentos": data["instrumentos"],
#         "tipoConvocatoria": data["tipoConvocatoria"],
#         "presupuestoTotal": data["presupuestoTotal"],
#         "descripcion": data["descripcion"],
#         "tiposBeneficiarios": data["tiposBeneficiarios"],
#         "sectores": data["sectores"],
#         "regiones": data["regiones"],
#         "descripcionFinalidad": data["descripcionFinalidad"],
#         "descripcionBasesReguladoras": data["descripcionBasesReguladoras"],
#         "urlBasesReguladoras": data["urlBasesReguladoras"],
#         "sePublicaDiarioOficial": data["sePublicaDiarioOficial"],
#         "abierto": data["abierto"],
#         "fechaInicioSolicitud": data["fechaInicioSolicitud"],
#         "fechaFinSolicitud": data["fechaFinSolicitud"],
#         "textInicio": data["textInicio"] if data["textInicio"] else None,
#         "textFin": data["textFin"] if data["textFin"] else None,
#         "reglamento": data["reglamento"] if data["reglamento"] else None,
#         "documentos": data["documentos"].strip() if data["documentos"] else None,
#     }
    

# Función para procesar el JSON y convertirlo a Yaml
def convert_json_to_yaml(json_aplanado, template):
    return template.format_map(json_aplanado)

def aplicar_plantilla(datos_json, plantilla_texto):
    """Aplica una plantilla de texto a un JSON, sustituyendo las variables."""
    try:
        # Descomponer el JSON para extraer los valores necesarios
        """ datos = {
            "id": datos_json.get("id", ""),
            "organo_nivel1": datos_json.get("organo", {}).get("nivel1", ""),
            "sedeElectronica": datos_json.get("sedeElectronica", ""),
            "codigoBDNS": datos_json.get("codigoBDNS", ""),
            "fechaRecepcion": datos_json.get("fechaRecepcion", ""),
            "instrumentos_descripcion": datos_json.get("instrumentos", [{}])[0].get("descripcion", "") if datos_json.get("instrumentos") else "",
            "tipoConvocatoria": datos_json.get("tipoConvocatoria", ""),
            "presupuestoTotal": datos_json.get("presupuestoTotal", ""),
            "descripcion": datos_json.get("descripcion", ""),
            "descripcionFinalidad": datos_json.get("descripcionFinalidad", ""),
            "reglamento_descripcion": datos_json.get("reglamento", {}).get("descripcion", ""),
            "documento_nombre": datos_json.get("documentos", [{}])[0].get("nombreFic", "") if datos_json.get("documentos") else "",
            "advertencia": datos_json.get("advertencia", "")
        } """

        datos = {
            "id": datos_json.get("id", ""),
            "organo_nivel1": datos_json.get("organo", {}).get("nivel1", ""),
            "sedeElectronica": datos_json.get("sedeElectronica", ""),
            "codigoBDNS": datos_json.get("codigoBDNS", "")
        }
        
        # Crear el template
        template = Template(plantilla_texto)
        # Rellenar el template con los datos extraídos
        resultado = template.substitute(datos)
        return resultado
    except KeyError as e:
        logging.error(f"Error: la clave {e} no está en el JSON.")
    except Exception as ex:
        logging.error(f"Ocurrió un error: {ex}")

def fetch_all_elements(base_url, page_size, carpeta_destino):
    """
    Descarga todos los elementos de la API usando paginación.

    :param base_url: URL base de la API.
    :param page_size: Número de elementos por página.
    :return: Lista con todos los elementos obtenidos.
    """
    all_elements = []
    page = 0
    total_pages = TOTAL_PAGES

    while page < total_pages:
        # Construir la URL de la página actual
        url = f"{base_url}&page={page}&pageSize={page_size}"
        
        try:
            # Hacer la solicitud
            response = requests.get(url)
            response.raise_for_status()  # Lanza una excepción si hay un error HTTP
            
            datos = response.json()

            if datos and "content" in datos:
                for elemento in datos["content"]:
                    descargar_y_guardar_json_por_id(elemento, carpeta_destino)
                    time.sleep(0.2)

            # Añadir los elementos de la página actual a la lista
            all_elements.extend(datos.get("content", []))
            

            # Actualizar el total de páginas si está disponible
            tot = datos.get("totalPages", 0)
            logging.info(f"Total de páginas {tot}")
            #total_pages = tot
            
            logging.info(f"Página {page + 1}/{total_pages} descargada. {len(datos.get('content', []))} elementos.")

        except requests.exceptions.RequestException as e:
            logging.error(f"Error al procesar la página {page}: {e}")
            break

        # Incrementar el número de página para la siguiente iteración
        page += 1

        # Pausa para evitar saturar el servidor en las sucesivas llamadas a las páginas
        time.sleep(1)

    return all_elements

if __name__ == "__main__":

    setup_logging_scrap()

        # Descargar todos los elementos
    elements = fetch_all_elements(URL_BASE_API, PAGE_SIZE, RUTA_DESTINO_DOCUMENTOS)

    # Guardar o procesar los elementos
    logging.info(f"Se han descargado {len(elements)} elementos en total.")

    # Opcional: Guardar los datos en un archivo JSON
    import json
    with open(f"{RUTA_DESTINO_DOCUMENTOS}\datosDescargados.json", "w", encoding="utf-8") as f:
        json.dump(elements, f, ensure_ascii=False, indent=4)

    logging.info("Datos guardados en 'datos.json'.")
