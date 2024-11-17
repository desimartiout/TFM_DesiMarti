

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
from datasets import load_dataset
from langchain_community.chat_models import ChatOllama
from ragas import evaluate
from langchain_community.embeddings import OllamaEmbeddings

# loading the V2 dataset
amnesty_qa = load_dataset("explodinggradients/amnesty_qa", "english_v2",trust_remote_code=True)

amnesty_subset = amnesty_qa["eval"].select(range(2))
amnesty_subset.to_pandas()

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

result = evaluate(amnesty_subset,
                  metrics=[
        context_precision,
        faithfulness,
        answer_relevancy,
        context_recall], llm=langchain_llm,embeddings=langchain_embeddings)


#result = langchain_llm.invoke("Tell me a joke")

print(result)