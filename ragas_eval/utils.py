import os
import csv
import json
import logging

from pandas import DataFrame

from datetime import datetime

from constantes import RAGAS_FILE_PATH, RAGAS_FILE_PATH_RESULTS, RAGAS_FILE_PATH_LOG

def setup_logging_ragas() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
    ruta_log = ruta_actual + RAGAS_FILE_PATH_LOG

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}.log")

    logging.basicConfig(
        filename=log_file_path,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

def write_to_json(user_input: str, response: str, retrieved_contexts: list, reference: str) -> None:
    """
    Escribe una entrada en un archivo JSON con los datos proporcionados.
    
    :param user_input: Pregunta del usuario.
    :param response: Respuesta generada.
    :param retrieved_contexts: Lista de contextos recuperados.
    :param reference: Texto de referencia.
    """

    # Crear el nombre del archivo con la fecha
    ragas_file_path = nombre_fichero_ragas_eval()

    # Si el archivo existe, cargarlo; de lo contrario, iniciar una lista vacía
    if os.path.isfile(ragas_file_path):
        with open(ragas_file_path, mode="r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []

    # Crear el diccionario con los datos
    entry = {
        "user_input": user_input,
        "reference": reference,
        "response": response,
        "retrieved_contexts": retrieved_contexts,
    }
    
    # Agregar la nueva entrada
    data.append(entry)
    
    # Escribir los datos actualizados en el archivo
    with open(ragas_file_path, mode="w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def nombre_fichero_ragas_eval() -> str:
    """
    Devuelve el nombre del fichero de evaluación donde se alacenarán los datos.
    """
    current_date = datetime.now().strftime("%Y_%m_%d")

    # Crear el nombre del archivo con la fecha
    ragas_file_path = os.path.join(RAGAS_FILE_PATH, f"{current_date}_ragas.json")
    
    return ragas_file_path

def write_eval_to_txt(eval_results: DataFrame) -> None:

    ragas_file_path_res = nombre_fichero_ragas_eval_results()
    logging.info(ragas_file_path_res)
    logging.info(eval_results)

    eval_results.to_csv(ragas_file_path_res,sep=";", index=False, quoting=1, quotechar='"')

def nombre_fichero_ragas_eval_results() -> str:
    """
    Devuelve el nombre del fichero de evaluación donde se alacenarán los datos.
    """
    current_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    # Crear el nombre del archivo con la fecha
    ragas_file_path = os.path.join(RAGAS_FILE_PATH_RESULTS, f"{current_date}_ragas_results.csv")
    
    return ragas_file_path

def write_to_csv(user_input: str, response: str, retrieved_contexts: str, reference: str) -> None:
    """
    Escribe una fila en un archivo CSV con los datos proporcionados.
    
    :param user_input: Texto ingresado por el usuario.
    :param response: Respuesta generada.
    :param retrieved_contexts: Contextos recuperados.
    :param reference: Referencia adicional.
    """

    # Crear el nombre del archivo con la fecha
    file_path = nombre_fichero_ragas_eval()

    # Verificar si el archivo existe
    file_exists = os.path.isfile(file_path)
    
    # Abrir el archivo en modo de escritura
    with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        
        # Escribir la cabecera si el archivo es nuevo
        if not file_exists:
            writer.writerow(["user_input", "response", "retrieved_contexts", "reference"])
        
        # Escribir la fila con los datos
        writer.writerow([user_input, response, retrieved_contexts, reference])
