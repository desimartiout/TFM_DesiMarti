import os

ruta_raiz = os.getcwd()

#Rutas base de los datasets de evaluación, logs y resultados
RAGAS_FILE_PATH_RESULTS = ruta_raiz + "/ragas_eval/results/"
RAGAS_FILE_PATH_LOG = "/ragas_eval/logs/"
RAGAS_FILE_PATH = ruta_raiz + "/ragas_eval/datasets/"
RAGAS_FILE_PATH_QUESTIONS = ruta_raiz + "/ragas_eval/questions/"

#CADENAS A UTILIZAR PARA ASIGNAR EL TIPO DE MODELO A UTILIZAR PARA LA EVALUACIÓN CUANDO LA METRICA LO NECESITA
RAGAS_LLM_TIPOMODELO_OLLAMA = "OLLAMA"
RAGAS_LLM_TIPOMODELO_OPENAI = "OPENAI"

#RAGAS_OPENAI_MODEL_NAME = "gpt-3.5-turbo"
RAGAS_OPENAI_MODEL_NAME = "gpt-4o-mini"
RAGAS_OLLAMA_MODEL_NAME = "llamaAyudas:latest"

RAGAS_DATASET_EVAL_SIZE = 3

# CONFIGURACIÓN DEL MODELO A UTILIZAR OLLAMA (requiere su instalación en local) o OPENAI (Requiere tener una API KEY de OPENAI)
RAGAS_LLM_SELECCIONADO = RAGAS_LLM_TIPOMODELO_OPENAI

if RAGAS_LLM_SELECCIONADO == RAGAS_LLM_TIPOMODELO_OPENAI:
    RAGAS_LLM_MODELO_SELECCIONADO = RAGAS_OPENAI_MODEL_NAME
else:
    RAGAS_LLM_MODELO_SELECCIONADO = RAGAS_OLLAMA_MODEL_NAME