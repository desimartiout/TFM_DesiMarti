

"""
Evaluating RAG using Llama 3
https://www.youtube.com/watch?v=Ts2wDG6OEko

Github
https://github.com/mosh98/RAG_With_Models/blob/main/evaluation/RAGAS%20DEMO.ipynb

 https://github.com/mosh98/RAG_With_Models/blob/main/evaluation/RAGAS%20DEMO.ipynb
!pip install dataset
!pip install ragas
!pip install langchain
!pip install langchain_community
!pip install nltk
 """

import os
import logging
import argparse

#1. Prepare Dataset
from datasets import Dataset, DatasetDict
import pandas as pd
import json
#from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from ragas import evaluate
#from langchain_community.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from ragas.metrics import Faithfulness
from ragas import EvaluationDataset, SingleTurnSample

from ragas.run_config import RunConfig

from constantes import OLLAMA_MODEL_NAME_RAGAS_LLM, OLLAMA_MODEL_NAME_RAGAS_EMBED, RAGAS_FILE_PATH
from utils import setup_logging_ragas, write_eval_to_txt

def main():

    # python script.py --log_file mi_log.log

    my_run_config = RunConfig(max_workers=64, timeout=60)

    setup_logging_ragas()

    parser = argparse.ArgumentParser(description="Script para configurar logging con un archivo específico.")
    parser.add_argument(
        "json_eval_file",  # Argumento posicional obligatorio
        type=str,
        help="Nombre del fichero json a evaluar. (Debe estar en la ruta datasets)",
    )
    
    # Parsear los argumentos
    args = parser.parse_args()

    logging.info("Fichero a evaluar:" + args.json_eval_file)

    fichero = RAGAS_FILE_PATH + args.json_eval_file

    if os.path.isfile(fichero):
        
        # Leer el JSON desde un archivo local
        with open(RAGAS_FILE_PATH + args.json_eval_file, "r") as file:
            data = json.load(file)

        # Crear un DatasetDict para simular la estructura de Hugging Face
        amnesty_qa = DatasetDict({
            "eval": Dataset.from_list(data)  # Puedes cambiar "eval" por el nombre adecuado
        })

        # Seleccionar un subconjunto de los datos
        amnesty_subset = amnesty_qa["eval"].select(range(1))

        # Convertir el Dataset completo a un DataFrame de Pandas
        amnesty_df = amnesty_qa["eval"].to_pandas()

        samples = []
        for row in amnesty_qa["eval"]:
            sample = SingleTurnSample(
                user_input=row["user_input"],
                reference=row["reference"],
                response=row["response"],
                retrieved_contexts=[context for context in row["retrieved_contexts"]],
            )
            samples.append(sample)

        eval_dataset = EvaluationDataset(samples=samples)
        metric = Faithfulness()

        #2. Initialize model
        from ragas.metrics import (
            answer_relevancy,
            faithfulness,
            context_recall,
            context_precision
        )

        # information found here: https://docs.ragas.io/en/latest/howtos/customisations/bring-your-own-llm-or-embs.html
        langchain_llm = ChatOllama(model=OLLAMA_MODEL_NAME_RAGAS_LLM)
        langchain_embeddings = OllamaEmbeddings(model=OLLAMA_MODEL_NAME_RAGAS_EMBED)

        result = evaluate(eval_dataset,
                        metrics=[
                faithfulness,
                answer_relevancy,
                context_recall,context_precision], llm=langchain_llm,embeddings=langchain_embeddings,run_config=my_run_config)
        # logging.info(result.to_pandas())
        logging.info(result.to_pandas())
        write_eval_to_txt(result.to_pandas())
        logging.info("Evaluación del modelo realizada correctamente")
        print("Proceso completado")

    else:
        print("El fichero " + fichero + " no ha sido encontrado.")

if __name__ == "__main__":
    main()