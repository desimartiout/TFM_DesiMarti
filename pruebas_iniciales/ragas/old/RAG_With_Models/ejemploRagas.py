

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

from ragas.run_config import RunConfig
my_run_config = RunConfig(max_workers=64, timeout=60)

from ragas import EvaluationDataset, SingleTurnSample
from ragas.metrics import Faithfulness
from datasets import load_dataset
from ragas import evaluate
from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings

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

eval_dataset = EvaluationDataset(samples=samples)
metric = Faithfulness()

langchain_llm = ChatOllama(model="llama3.2:1b")
langchain_embeddings = OllamaEmbeddings(model="llama3.2:1b")
result = evaluate(dataset=eval_dataset,
                  metrics=[metric], llm=langchain_llm,embeddings=langchain_embeddings)

print(result)