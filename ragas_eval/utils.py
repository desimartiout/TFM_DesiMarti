import os
import csv

import logging
from pandas import DataFrame
from datetime import datetime
from config.ragas.ragas_config import RAGAS_FILE_PATH_RESULTS, RAGAS_FILE_PATH_LOG

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
        encoding="utf-8"
    )

def write_eval_to_csv(eval_results: DataFrame) -> None:

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



# def write_to_csv(user_input: str, response: str, retrieved_contexts: str, reference: str) -> None:
#     """
#     Escribe una fila en un archivo CSV con los datos proporcionados.
    
#     :param user_input: Texto ingresado por el usuario.
#     :param response: Respuesta generada.
#     :param retrieved_contexts: Contextos recuperados.
#     :param reference: Referencia adicional.
#     """

#     # Crear el nombre del archivo con la fecha
#     file_path = nombre_fichero_ragas_eval()

#     # Verificar si el archivo existe
#     file_exists = os.path.isfile(file_path)
    
#     # Abrir el archivo en modo de escritura
#     with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
#         writer = csv.writer(csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        
#         # Escribir la cabecera si el archivo es nuevo
#         if not file_exists:
#             writer.writerow(["user_input", "response", "retrieved_contexts", "reference"])
        
#         # Escribir la fila con los datos
#         writer.writerow([user_input, response, retrieved_contexts, reference])
