import os

OLLAMA_MODEL_NAME_LLM = "llamaAyudas:latest"
OLLAMA_MODEL_NAME_EMBED = "llamaAyudas:latest"

#Ruta base donde se almacenan los datasets de evaluación para ragas
RAGAS_FILE_PATH = os.getcwd() + "/ragas_eval/datasets/"
RAGAS_FILE_PATH_RESULTS = os.getcwd() + "/ragas_eval/results/"
RAGAS_FILE_PATH_LOG = "/ragas_eval/logs/"