import os
import csv
import sys
import logging
from pandas import DataFrame
from datetime import datetime

from config.scrapping_config import SCRAP_FILE_PATH_LOG

def setup_logging_scrap() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    # ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
    ruta_log = SCRAP_FILE_PATH_LOG

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}.log")

    logging.basicConfig(
        filename=log_file_path,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
        encoding="utf-8"
    )