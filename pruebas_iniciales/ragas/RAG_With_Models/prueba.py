

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

""" {'question': 'Which private companies in the Americas are the largest GHG emitters according to the Carbon Majors database?',
 'ground_truths': ['The largest private companies in the Americas that are the largest GHG emitters according to the Carbon Majors database are ExxonMobil, Chevron, and Peabody.'],
 'answer': 'According to the Carbon Majors database, the largest private companies in the Americas that are the largest GHG emitters are:\n\n1. Chevron Corporation (United States)\n2. ExxonMobil Corporation (United States)\n3. ConocoPhillips Company (United States)\n4. BP plc (United Kingdom, but with significant operations in the Americas)\n5. Royal Dutch Shell plc (Netherlands, but with significant operations in the Americas)\n6. Peabody Energy Corporation (United States)\n7. Duke Energy Corporation (United States)\n8. TotalEnergies SE (France, but with significant operations in the Americas)\n9. BHP Group Limited (Australia, but with significant operations in the Americas)\n10. Rio Tinto Group (United Kingdom/Australia, but with significant operations in the Americas)\n\nPlease note that the rankings may change over time as new data becomes available.',
 'contexts': ['The private companies responsible for the most emissions during this period, according to the database, are from the United States: ExxonMobil, Chevron and Peabody.\nThe largest emitter amongst state-owned companies in the Americas is Mexican company Pemex, followed by Venezuelan company Petróleos de Venezuela, S.A.']} """

amnesty_qa['eval'].to_json("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/ragas/RAG_With_Models/data/amnesty_qa_eval.json")
""" amnesty_qa['validation'].to_json("/data/amnesty_qa_validation.json")
amnesty_qa['test'].to_json("/data/amnesty_qa_test.json")
 """
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