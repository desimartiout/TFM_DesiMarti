

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
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

from ragas import EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness
from datasets import load_dataset
from ragas import evaluate

dataset = load_dataset("explodinggradients/amnesty_qa", "english_v3")

samples = []
for row in dataset["eval"]:
    sample = SingleTurnSample(
        user_input=row["user_input"],
        reference=row["reference"],
        response=row["response"],
        retrieved_contexts=row["retrieved_contexts"],
    )
    samples.append(sample)
    break

eval_dataset = EvaluationDataset(samples=samples)
metric = Faithfulness()

# information found here: https://docs.ragas.io/en/latest/howtos/customisations/bring-your-own-llm-or-embs.html
langchain_llm = ChatOllama(model="llama2:latest")
langchain_embeddings = OllamaEmbeddings(model="llama2:latest")

result = evaluate(eval_dataset,
                  metrics=[metric], llm=langchain_llm,embeddings=langchain_embeddings)

print(result)
