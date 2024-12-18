# Importamos librerias
import pickle as pkl
import warnings
import yaml
from pathlib import Path
import logging, os, datetime

# Definimos variables de entorno necesarias

# Ignorar warnings específicos de huggingface_hub
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub.file_download")
warnings.filterwarnings("ignore", category=UserWarning, module="huggingface_hub.file_download")

# # Abrir y leer el archivo YAML de configuración
# with open(Path(os.getenv('PROJECT_ROOT')) / 'config/config.yml', 'r') as file:
#     config = yaml.safe_load(file)

# # Leemos variables de entorno
# PATH_BASE = Path(config['ruta_base'])
# date_today = datetime.datetime.today().strftime("%Y_%m_%d")

INDEX_FAISS = "faiss_index.pkl"
RETRIEVER_FAISS = "faiss_index.pkl"
RUTA_FAISS = "/faiss/"
LOG_FILE_PATH = "/logs/"
OLLAMA_MODEL_NAME = "llamaAyudas:latest"
FAISS_SENTENCE_TRANSFORMER = "paraphrase-multilingual-MiniLM-L12-v2"

def setup_logging() -> None:
    current_date = datetime.now().strftime("%Y-%m-%d")
    ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
    ruta_log = ruta_actual + LOG_FILE_PATH

    # Crear el nombre del archivo con la fecha
    log_file_path = os.path.join(ruta_log, f"{current_date}.log")

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


class carga():
    """
       Clase que gestiona la carga de una base de datos vectorial de FAISS.

       Esta clase está diseñada para inicializar y poblar una base de datos FAISS
       utilizando datos vectoriales que se extraen de archivos CSV. Estos archivos
       CSV son descargados y preparados por un módulo de obtención de datos externo.

       Métodos:
           cargar_db_Vectorial(self,): Carga un archivo pkl desde la ruta especificada.
           getRetriver(self): Inicializa el Retriver de FAISS.
           inialize_retriever(self,): Realiza toda la logica de la carga
       """

    def __init__(self):
        self.ruta_db = RUTA_FAISS
        logger.debug(f'Leemos la configuracion Ruta de la Base de datos: {self.ruta_db}')
        self.cargar_db_Vectorial()

    def cargar_db_Vectorial(self):
        """
        Carga la base de datos vectorial partiendo de los parámetros obtenidos del fichero de configuración
        :return:
        """
        try:
            with open(self.ruta_db / Path(INDEX_FAISS), 'rb') as archivo:
                self.vector_index = pkl.load(archivo)
        except Exception as e:
            logger.error(f'Un Error se produjo al intentar leer la base de datos de embbedings vector Index: {e}')

        try:
            with open(self.ruta_db / Path(RETRIEVER_FAISS), 'rb') as archivo:
                self.retriever = pkl.load(archivo)
        except Exception as e:
            logger.error(f'Un Error se produjo al intentar guardar la base de datos de embbedings tipo retriever: {e}')

    def getRetriver(self):
        """
        Devuelve el Retreiver que se incluirá en la cadena de blockchain del proyecto OEPIA
        :return: retreiver FAISS
        """
        return self.retriever

    def inialize_retriever(self):
        """
        Ejecuta en el orden adevcuado todos los métodos para obtener el retreiver FAISS
        :return: retreiver FAISS
        """
        self.cargar_db_Vectorial()
        return self.getRetriver()


if __name__ == '__main__':
    """
    Método principal para probar la clase aisladamente.
    """
    BDVect = carga()
    retriever = BDVect.getRetriver()