import asyncio
from ragas import SingleTurnSample
from transformers import AutoModelForCausalLM

from ragas import SingleTurnSample
from ragas.llms import LangchainLLMWrapper
from langchain_ollama import ChatOllama
from ragas.metrics import LLMContextPrecisionWithoutReference

async def main():

    # Definir el ejemplo con contextos recuperados y de referencia
    evaluator_llm = LangchainLLMWrapper(ChatOllama(model="llamaAyudas:latest"))
    context_precision = LLMContextPrecisionWithoutReference(llm=evaluator_llm)

    sample = SingleTurnSample(
        user_input="Where is the Eiffel Tower located?",
        response="The Eiffel Tower is located in Paris.",
        retrieved_contexts=["The Eiffel Tower is located in Paris."], 
    )


    score_cp = await context_precision.single_turn_ascore(sample)

    print(f"Context Recall Score: {score_cp}")

# Ejecutar el programa asincrónico
asyncio.run(main())