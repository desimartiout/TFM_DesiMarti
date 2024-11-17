import json
from string import Template
import requests
import os

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
    url = f"https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias?numConv={elemento['numeroConvocatoria']}&vpd=GE"  # Cambia la URL base según corresponda
    #https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias?numConv=790767&vpd=GE

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

        # Plantilla de texto
        """ plantilla_texto = 
        Número de Ayuda / subvención: ${codigoBDNS}
        Órgano: ${organo_nivel1} - ${organo_nivel2}
        Sede Electrónica: ${sedeElectronica}
        Código BDNS: ${codigoBDNS}
        Fecha de Recepción: ${fechaRecepcion}
        Instrumento: ${instrumentos_descripcion}
        Tipo de Convocatoria: ${tipoConvocatoria}
        Presupuesto Total: ${presupuestoTotal}€
        Descripción: ${descripcion}
        Finalidad: ${descripcionFinalidad}
        Reglamento Aplicable: ${reglamento_descripcion}
        Documento Asociado: ${documento_nombre}
        Advertencia Legal: ${advertencia}
        """

        plantilla_texto = """
        Número de Ayuda / subvención: ${codigoBDNS}
        Órgano: ${organo_nivel1}
        Sede Electrónica: ${sedeElectronica}
        Código BDNS: ${codigoBDNS}
        """

        archivo_destino = os.path.join(carpeta_destino, f"{elemento['numeroConvocatoria']}.txt")
        with open(archivo_destino, 'w', encoding='utf-8') as archivo:
            resultado = aplicar_plantilla(json_data, plantilla_texto)
            archivo.write(resultado)
        
        print(f"Datos guardados en {archivo_destino}")
        
    except requests.RequestException as e:
        print(f"Error al descargar el JSON para ID {elemento['inumeroConvocatoria']}: {e}")
    except json.JSONDecodeError:
        print(f"Error al decodificar el JSON descargado para ID {elemento['numeroConvocatoria']}.")

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
    """Lee el JSON y descarga y guarda datos para cada elemento de 'content'."""
    datos = leer_json(file_path)
    if datos and "content" in datos:
        for elemento in datos["content"]:
            descargar_y_guardar_json_por_id(elemento, carpeta_destino)

# Ejemplo de uso
file_path = f'C:/Users/desim/Documents/GitHub/build_your_local_RAG_system_desi/scrapping/listado.json'
carpeta_destino = os.path.expanduser('C:/Users/desim/Documents/GitHub/build_your_local_RAG_system_desi/scrapping/Documentos')
procesar_json(file_path, carpeta_destino)
