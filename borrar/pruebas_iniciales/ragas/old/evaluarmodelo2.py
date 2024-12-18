import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from typing import Any, List, Optional
from datasets import Dataset
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate

import os, sys, pprint
import pandas as pd
import numpy as np
import ragas, datasets

# Libraries to customize ragas critic model.
from ragas.llms import LangchainLLMWrapper
#from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama

# Libraries to customize ragas embedding model.
from langchain_huggingface import HuggingFaceEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper

#pip install 'accelerate>=0.26.0' --> ImportError: Using `low_cpu_mem_usage=True` or a `device_map` requires Accelerate: `pip install 'accelerate>=0.26.0'`

# Set environment variable for CUDA
#os.environ["CUDA_VISIBLE_DEVICES"] = "6"

""" # !python -m pip install ollama
# !ollama pull llama3
import ollama

# Verify details which model you are running.
ollama_llama3 = ollama.list()['models'][0]

# Print the model details.
keys = ['format', 'parameter_size', 'quantization_level']
print(f"MODEL:{ollama.list()['models'][0]['name']}", end=", ")
for key in keys:
    print(f"{str.upper(key)}:{ollama.list()['models'][0]['details'].get(key, 'Key not found in dictionary')}", end=", ")
print(end="\n\n") """

# Initialize custom LLM
mode_path = "llamaAyudas:latest"
ragas_llm = LangchainLLMWrapper(langchain_llm=ChatOllama(model=mode_path))

# Change the default embeddings models to use model on HuggingFace.
embedding_model_dir = "meta-llama/Llama-3.2-1B"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}
embedding_model = HuggingFaceEmbeddings(
    model_name=embedding_model_dir,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
ragas_emb = LangchainEmbeddingsWrapper(embeddings=embedding_model)

#https://github.com/milvus-io/bootcamp/blob/master/bootcamp/workshops/dbta_may_2024/2.%20RAG_basic_eval_langchain.ipynb

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
score = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall], llm=ragas_llm, embeddings=ragas_emb)
print(score.to_pandas())

