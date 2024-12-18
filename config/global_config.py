import os

####################################################################################################
#                               SELECCION TIPO MODELO Y EMBEDDINGS
####################################################################################################
#CADENAS A UTILIZAR PARA ASIGNAR EL TIPO DE MODELO A LA CONSTANTE LLM_MODELO_SELECCIONADO
LLM_TIPOMODELO_OLLAMA = "OLLAMA"
LLM_TIPOMODELO_OPENAI = "OPENAI"
#Constantes para seleccionar el tipo de BD Vectorial a utilizar
BD_VECTORIAL_CHROMADB = "CHROMADB"
BD_VECTORIAL_FAISS = "FAISS"


# CONFIGURA AQUI - CONFIGURACIÓN DEL MODELO A UTILIZAR OLLAMA (requiere su instalación en local) o OPENAI (Requiere tener una API KEY de OPENAI)
LLM_MODELO_SELECCIONADO = LLM_TIPOMODELO_OPENAI
# CONFIGURA AQUI - CONFIGURACIÓN DEL MODELO A UTILIZAR CHROMADB o FAISS
TIPO_BD_VECTORIAL = BD_VECTORIAL_FAISS

# MODELO EMBEDDINGS
SENTENCE_TRANSFORMER = "paraphrase-multilingual-MiniLM-L12-v2"                      # otras opciones "all-MiniLM-L6-v2", "paraphrase-multilingual-mpnet-base-v2" #--> EMBEDDING_DIMENSION = 768
EMBEDDING_DIMENSION = 384                                                           # Otras opciones 768
####################################################################################################
#                                  CONFIGURACIÓN CHROMADB
####################################################################################################
CHROMA_COLLECTION_NAME = "subvenciones"
CHROMA_PERSIST_PATH = "./chromadb/"
CHROMA_NUMDOCUMENTS = 5
CHROMA_SIMILARITY_THRESHOLD = 0.8

####################################################################################################
#                                     CONFIGURACIÓN OLLAMA
####################################################################################################
OLLAMA_MODEL_NAME = "llamaAyudas:latest"        # otras opciones "llama3.2:1b", "llama3.1", ...
OLLAMA_TEMPERATURE = 0.9

####################################################################################################
#                                     CONFIGURACIÓN OPENAI
####################################################################################################
OPENAI_MODEL_NAME = "gpt-4o-mini"               # otras opciones "gpt-3.5-turbo", "gpt-4o", ...

####################################################################################################
#                       CONFIGURACIÓN DE LA APLICACIÓN - TOCAR CON CUIDADO
####################################################################################################

# Logging
LOG_FILE_PATH = "/logs/"  # File path for the application log file
EVAL_SAVE = "1"   # Indica que guarda los resultados de las búsquedas en JSON para luevo poder evaluarlos con RAGAS
RAGAS_FILE_PATH = os.getcwd() + "/ragas_eval/datasets/"
RAGAS_FILE_PATH_QUESTIONS = os.getcwd() + "/ragas_eval/questions/"


####################################################################################################
#                                   CONFIGURACIÓN DE LA WEB
####################################################################################################
URL_WEB = "https://huggingface.co/spaces/DesiMarti/TFMCienciaDatos"
LOGO_URL_LARGE = "images/LogoLargo.png"
LOGO_URL_SMALL = "images/LogoCorto.png"
HUMAN_ICON = "images/user.png"

if LLM_MODELO_SELECCIONADO == LLM_TIPOMODELO_OLLAMA:
    AI_ICON = "images/ollama.png"
else:
    AI_ICON = "images/openai.png"