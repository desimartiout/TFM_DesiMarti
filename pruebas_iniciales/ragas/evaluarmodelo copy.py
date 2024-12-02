import os
import torch
from datasets import Dataset
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate
from langchain_ollama import ChatOllama
from ragas import evaluate
from langchain_ollama import OllamaEmbeddings


# information found here: https://docs.ragas.io/en/latest/howtos/customisations/bring-your-own-llm-or-embs.html
langchain_llm = ChatOllama(model="llamaAyudas:latest")
langchain_embeddings = OllamaEmbeddings(model="llamaAyudas:latest")

# Define dataset
data_samples = {
    'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
    'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
    'contexts': [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'], 
                 ['The Green Bay Packers...Green Bay, Wisconsin.', 'The Packers compete...Football Conference']],
    'ground_truth': ['The first superbowl was held on January 15, 1967', 'The New England Patriots have won the Super Bowl a record six times']
}
dataset = Dataset.from_dict(data_samples)

# Evaluate using custom LLM and embeddings
score = evaluate(dataset, metrics=[answer_relevancy, context_precision, context_recall], llm=langchain_llm, embeddings=langchain_embeddings)
print(score.to_pandas())