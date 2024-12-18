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

from config.ragas.ragas_config import RAGAS_OLLAMA_MODEL_NAME, RAGAS_FILE_PATH, RAGAS_LLM_MODELO_SELECCIONADO, RAGAS_LLM_SELECCIONADO, RAGAS_LLM_TIPOMODELO_OPENAI, RAGAS_OPENAI_MODEL_NAME

from ragas_eval.utils import setup_logging_ragas, write_eval_to_csv

from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity, AnswerRelevancy, ContextPrecision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# import warnings
# warnings.filterwarnings("ignore", category=RuntimeWarning, message="Event loop is closed")

def main():

    #  C:/Users/desim/anaconda3/envs/faiss_env/python.exe c:/Users/desim/Documents/GitHub/TFM_DesiMarti/ragas_eval/evaluar.py 2024_12_09_ragas.json

    setup_logging_ragas()

    parser = argparse.ArgumentParser(description="Script para configurar fichero de evaluación.")
    parser.add_argument(
        "json_eval_file",  # Argumento posicional obligatorio
        type=str,
        help="Nombre del fichero json a evaluar. (Debe estar en la carpeta datasets)",
    )
    
    # Parsear los argumentos
    args = parser.parse_args()

    logging.info("Fichero a evaluar:" + args.json_eval_file)

    fichero = RAGAS_FILE_PATH + args.json_eval_file

    if os.path.isfile(fichero):
        
        # Leer el JSON desde un archivo local
        with open(RAGAS_FILE_PATH + args.json_eval_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Crear un DatasetDict para simular la estructura de Hugging Face
        amnesty_qa = DatasetDict({
            "eval": Dataset.from_list(data) 
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

        logging.info("Evaluamos con: " + RAGAS_LLM_SELECCIONADO)
        if RAGAS_LLM_SELECCIONADO==RAGAS_LLM_TIPOMODELO_OPENAI:
            evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=RAGAS_LLM_MODELO_SELECCIONADO))
            evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

            metrics = [
                LLMContextRecall(llm=evaluator_llm), 
                FactualCorrectness(llm=evaluator_llm), 
                Faithfulness(llm=evaluator_llm),
                SemanticSimilarity(embeddings=evaluator_embeddings),
                AnswerRelevancy(embeddings=evaluator_embeddings),
                ContextPrecision(llm=evaluator_llm)
            ]
            result = evaluate(dataset=eval_dataset, metrics=metrics)

        else:
            metric = Faithfulness()

            from ragas.metrics import (
                answer_relevancy,
                faithfulness,
                context_recall,
                context_precision
            )

            langchain_llm = ChatOllama(model=RAGAS_LLM_MODELO_SELECCIONADO)
            langchain_embeddings = OllamaEmbeddings(model=RAGAS_LLM_MODELO_SELECCIONADO)

            my_run_config = RunConfig(max_workers=64, timeout=60)

            result = evaluate(eval_dataset,
                            metrics=[
                    faithfulness,
                    answer_relevancy,
                    context_recall,context_precision], llm=langchain_llm,embeddings=langchain_embeddings,run_config=my_run_config)

        df = result.to_pandas()
        print(df.head())

        logging.info(result.to_pandas())
        write_eval_to_csv(result.to_pandas())
        logging.info("Evaluación del modelo realizada correctamente")
        print("Proceso completado")

    else:
        print("El fichero " + fichero + " no ha sido encontrado.")

if __name__ == "__main__":
    main()