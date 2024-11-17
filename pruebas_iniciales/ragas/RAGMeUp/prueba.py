import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from typing import Any, List, Optional
from datasets import Dataset
from ragas.llms import LlamaIndexLLMWrapper
from ragas.embeddings import LlamaIndexEmbeddingsWrapper
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas import evaluate

# Set environment variable for CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = "6"

# Define custom LLM class
class Qwen_LLM:
    tokenizer: AutoTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, mode_name_or_path: str):
        print("Loading model from local path...")
        self.tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, use_fast=False)
        self.model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, torch_dtype=torch.bfloat16, device_map="auto")
        self.model.generation_config = GenerationConfig.from_pretrained(mode_name_or_path)
        print("Model loaded successfully")

    def __call__(self, prompt: str, stop: Optional[List[str]] = None, **kwargs: Any):
        messages = [{"role": "user", "content": prompt}]
        input_ids = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        model_inputs = self.tokenizer([input_ids], return_tensors="pt").to('cuda')
        generated_ids = self.model.generate(model_inputs.input_ids, max_new_tokens=512)
        generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)]
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response

# Initialize custom LLM
mode_path = "<path_to_your_model>"
llm = Qwen_LLM(mode_name_or_path=mode_path)

# Initialize custom embeddings
embedding_model_dir = "<path_to_your_embedding_model>"
embedding_model_kwargs = {'device': 'cuda'}
encode_kwargs = {'normalize_embeddings': True}
embedding_model = HuggingFaceBgeEmbeddings(
    model_name=embedding_model_dir,
    model_kwargs=embedding_model_kwargs,
    encode_kwargs=encode_kwargs,
    query_instruction="为这个句子生成表示以用于检索相关文章："
)

# Wrap custom LLM and embeddings with LlamaIndex wrappers
llm = LlamaIndexLLMWrapper(llm)
embedding_model = LlamaIndexEmbeddingsWrapper(embedding_model)

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
score = evaluate(dataset, metrics=[faithfulness, answer_relevancy, context_precision, context_recall], llm=llm, embeddings=embedding_model)
print(score.to_pandas())