import json
from string import Template
import requests
import os
from collections import defaultdict
from constantes import URL_CONVOCATORIA, URL_CONVOCATORIA_POST, TEMPLATE_DOC

def leer_json(file_path):
    """Lee un archivo JSON y devuelve su contenido como un diccionario."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            datos = json.load(file)
        return datos
    except FileNotFoundError:
        print(f"El archivo en la ruta {file_path} no se encontró.")
    except json.JSONDecodeError:
        print(f"Error al decodificar el archivo JSON en la ruta {file_path}.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")


def descargar_y_guardar_json_por_id(elemento, carpeta_destino):
    """Descarga el JSON de una URL usando el id del elemento y lo guarda en una carpeta destino."""
    url = URL_CONVOCATORIA + f"{elemento['numeroConvocatoria']}" + URL_CONVOCATORIA_POST  # Cambiamos la URL base según corresponda

    try:
        print(url)
        response = requests.get(url)
        response.raise_for_status()  # Genera una excepción para códigos de error HTTP
        json_data = response.json()
        
        
        # Crear la carpeta si no existe
        os.makedirs(carpeta_destino, exist_ok=True)
        
        # Guardar el JSON descargado en un archivo
        archivo_destino = os.path.join(carpeta_destino, f"{elemento['numeroConvocatoria']}.json")
        with open(archivo_destino, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        
        print(f"Datos guardados en {archivo_destino}")

        # Generar texto
        formatted_text = safe_format(json_data, TEMPLATE_DOC)
        print(formatted_text)

        archivo_destino = os.path.join(carpeta_destino, f"{elemento['numeroConvocatoria']}.yaml")

        resultado = aplicar_plantilla(json_data, formatted_text)
        if resultado!= None:
            with open(archivo_destino, 'w', encoding='utf-8') as archivo:        
                archivo.write(resultado)
            print(f"Datos guardados en {archivo_destino}")
        
    except requests.RequestException as e:
        print(f"Error al descargar el JSON para ID {elemento['inumeroConvocatoria']}: {e}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el JSON descargado para ID {elemento['numeroConvocatoria']}.")


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


# Función para aplanar y procesar el JSON
def safe_format(data, template):
    flat_data = defaultdict(
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
    return template.format_map(flat_data)

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
        print(f"Error: la clave {e} no está en el JSON.")
    except Exception as ex:
        print(f"Ocurrió un error: {ex}")

def procesar_json(file_path, carpeta_destino):
    """
    Lee el JSON y descarga y guarda datos para cada elemento de 'content'.

    Parámetros:
        file_path (str): Ruta del fichero Json que tiene los documentos a cargar.
        carpeta_destino (str): Ruta de la carpeta de destino donde dejará los documentos yaml.

    Devuelve:
        Nada
    """
    datos = leer_json(file_path)
    if datos and "content" in datos:
        for elemento in datos["content"]:
            descargar_y_guardar_json_por_id(elemento, carpeta_destino)


ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python

# Ejemplo de uso
file_path = f"{ruta_actual}\scrapping\listado2.json"
carpeta_destino = f"{ruta_actual}\scrapping\Documentos"

procesar_json(file_path, carpeta_destino)
