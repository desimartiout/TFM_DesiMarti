

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

# increasing max_workers to 64 and timeout to 60 seconds
my_run_config = RunConfig(max_workers=64, timeout=60)


import json

# Leer el JSON desde un archivo local
with open("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/ragas/RAG_With_Models/data/eval.json", "r") as file:
    data = json.load(file)

# Crear un DatasetDict para simular la estructura de Hugging Face
amnesty_qa = DatasetDict({
    "eval": Dataset.from_list(data)  # Puedes cambiar "eval" por el nombre adecuado
})

# Seleccionar un subconjunto de los datos
amnesty_subset = amnesty_qa["eval"].select(range(1))

# Convertir el Dataset completo a un DataFrame de Pandas
amnesty_df = amnesty_qa["eval"].to_pandas()

""" # Mostrar resultados
print("----------")
print(amnesty_subset)
print("----------")
print(amnesty_df)
print("----------") """

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

""" print("----------")
print(samples)
print("----------") """

#2. Initialize model
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision
)

# information found here: https://docs.ragas.io/en/latest/howtos/customisations/bring-your-own-llm-or-embs.html
langchain_llm = ChatOllama(model="llama3.2:3b")
langchain_embeddings = OllamaEmbeddings(model="llama3.2:3b")

result = evaluate(eval_dataset,
                  metrics=[
        faithfulness,
        answer_relevancy,
        context_recall,context_precision], llm=langchain_llm,embeddings=langchain_embeddings,run_config=my_run_config)

print(result)
print("----------")