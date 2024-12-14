
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, SemanticSimilarity
from ragas import evaluate

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import SingleTurnSample, EvaluationDataset
from ragas.run_config import RunConfig
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

OLLAMA_MODEL_NAME_RAGAS_LLM = "llamaAyudas:latest"
OLLAMA_MODEL_NAME_RAGAS_EMBED = "llamaAyudas:latest"

my_run_config = RunConfig(max_workers=64, timeout=60)
evaluator_llm = LangchainLLMWrapper(ChatOllama(model=OLLAMA_MODEL_NAME_RAGAS_LLM))
evaluator_embeddings = LangchainEmbeddingsWrapper(OllamaEmbeddings(model=OLLAMA_MODEL_NAME_RAGAS_EMBED))


# Sample 1
sample1 = SingleTurnSample(
    user_input="What is the capital of Germany?",
    retrieved_contexts=["Berlin is the capital and largest city of Germany."],
    response="The capital of Germany is Berlin.",
    reference="Berlin",
)

# Sample 2
sample2 = SingleTurnSample(
    user_input="Who wrote 'Pride and Prejudice'?",
    retrieved_contexts=["'Pride and Prejudice' is a novel by Jane Austen."],
    response="'Pride and Prejudice' was written by Jane Austen.",
    reference="Jane Austen",
)

# Sample 3
sample3 = SingleTurnSample(
    user_input="What's the chemical formula for water?",
    retrieved_contexts=["Water has the chemical formula H2O."],
    response="The chemical formula for water is H2O.",
    reference="H2O",
)

dataset = EvaluationDataset(samples=[sample1, sample2, sample3])

eval_dataset = EvaluationDataset.from_hf_dataset(dataset)

metrics = [
    LLMContextRecall(llm=evaluator_llm), 
    FactualCorrectness(llm=evaluator_llm), 
    Faithfulness(llm=evaluator_llm),
    SemanticSimilarity(embeddings=evaluator_embeddings)
]
results = evaluate(dataset=eval_dataset, metrics=metrics)

df = results.to_pandas()
print(df.head())