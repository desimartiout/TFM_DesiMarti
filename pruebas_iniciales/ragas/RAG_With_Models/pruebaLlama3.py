

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


""" {'question': 'Which private companies in the Americas are the largest GHG emitters according to the Carbon Majors database?',
 'ground_truths': ['The largest private companies in the Americas that are the largest GHG emitters according to the Carbon Majors database are ExxonMobil, Chevron, and Peabody.'],
 'answer': 'According to the Carbon Majors database, the largest private companies in the Americas that are the largest GHG emitters are:\n\n1. Chevron Corporation (United States)\n2. ExxonMobil Corporation (United States)\n3. ConocoPhillips Company (United States)\n4. BP plc (United Kingdom, but with significant operations in the Americas)\n5. Royal Dutch Shell plc (Netherlands, but with significant operations in the Americas)\n6. Peabody Energy Corporation (United States)\n7. Duke Energy Corporation (United States)\n8. TotalEnergies SE (France, but with significant operations in the Americas)\n9. BHP Group Limited (Australia, but with significant operations in the Americas)\n10. Rio Tinto Group (United Kingdom/Australia, but with significant operations in the Americas)\n\nPlease note that the rankings may change over time as new data becomes available.',
 'contexts': ['The private companies responsible for the most emissions during this period, according to the database, are from the United States: ExxonMobil, Chevron and Peabody.\nThe largest emitter amongst state-owned companies in the Americas is Mexican company Pemex, followed by Venezuelan company Petróleos de Venezuela, S.A.']} """

# loading the V2 dataset
#amnesty_qa = load_dataset("explodinggradients/amnesty_qa", "english_v3",trust_remote_code=True)
#amnesty_qa['eval'].to_json("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/ragas/RAG_With_Models/data/amnesty_qa_eval.json")
#amnesty_subset = amnesty_qa["eval"].select(range(2))
#amnesty_subset.to_json("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/ragas/RAG_With_Models/data/amnesty_qa_eval1.json")
#amnesty_qa.to_pandas()

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

# Mostrar resultados
print(amnesty_subset)
print(amnesty_df)


#2. Initialize model
from ragas.metrics import (
    answer_relevancy,
    faithfulness,
    context_recall,
    context_precision,
)

# information found here: https://docs.ragas.io/en/latest/howtos/customisations/bring-your-own-llm-or-embs.html
langchain_llm = ChatOllama(model="llama3.2:1b")
langchain_embeddings = OllamaEmbeddings(model="llama3.2:1b")


langchain_embeddings

result = evaluate(amnesty_subset,
                  metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall], llm=langchain_llm,embeddings=langchain_embeddings)

print(result)