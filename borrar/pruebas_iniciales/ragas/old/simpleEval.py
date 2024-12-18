
""" #LLM Based Context Precision

from ragas import SingleTurnSample
from ragas.metrics import LLMContextPrecisionWithReference

context_precision = LLMContextPrecisionWithReference(llm="llamaAyudas:latest")

sample = SingleTurnSample(
    user_input="Where is the Eiffel Tower located?",
    reference="The Eiffel Tower is located in Paris.",
    retrieved_contexts=["The Eiffel Tower is located in Paris."], 
)

await context_precision.single_turn_ascore(sample) """


#Non LLM Based Context Precision

import asyncio
from ragas import SingleTurnSample
from ragas.llms import LlamaIndexLLMWrapper
from ragas.metrics import NonLLMContextPrecisionWithReference, NonLLMContextRecall, NoiseSensitivity, ResponseRelevancy, FaithfulnesswithHHEM
from transformers import AutoModelForCausalLM, AutoTokenizer

async def main():

    # Definir el ejemplo con contextos recuperados y de referencia
    sample = SingleTurnSample(
        retrieved_contexts=["The Eiffel Tower is located in Paris."], 
        reference_contexts=["Paris is the capital of France.", "The Eiffel Tower is one of the most famous landmarks in Paris."]
    )
    context_precision = NonLLMContextPrecisionWithReference()
    score_cp = await context_precision.single_turn_ascore(sample)
    print(f"Context Precision Score: {score_cp}")

    context_recall = NonLLMContextRecall()
    score_cr = await context_recall.single_turn_ascore(sample)
    print(f"Context Recall Score: {score_cr}")

    llm = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B")

    """ # Pass the model instance to NoiseSensitivity
    noise_sensitivity = NoiseSensitivity(llm=llm) 
    sample = SingleTurnSample(
        user_input="What is the Life Insurance Corporation of India (LIC) known for?",
        response="The Life Insurance Corporation of India (LIC) is the largest insurance company in India, known for its vast portfolio of investments. LIC contributes to the financial stability of the country.",
        reference="The Life Insurance Corporation of India (LIC) is the largest insurance company in India, established in 1956 through the nationalization of the insurance industry. It is known for managing a large portfolio of investments.",
        retrieved_contexts=[
                "The Life Insurance Corporation of India (LIC) was established in 1956 following the nationalization of the insurance industry in India.",
                "LIC is the largest insurance company in India, with a vast network of policyholders and huge investments.",
                "As the largest institutional investor in India, LIC manages substantial funds, contributing to the financial stability of the country.",
                "The Indian economy is one of the fastest-growing major economies in the world, thanks to sectors like finance, technology, manufacturing etc."
            ]
        )
    score_ns = await noise_sensitivity.single_turn_ascore(sample)
    print(f"Context Recall Score: {score_ns}") """

    """ response_relevancy = ResponseRelevancy(llm="llamaAyudas:latest")    #Requiere LLM
    sample = SingleTurnSample(
            user_input="When was the first super bowl?",
            response="The first superbowl was held on Jan 15, 1967",
            retrieved_contexts=[
                "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
            ]
        )
    score_rr = await response_relevancy.single_turn_ascore(sample)
    print(f"Response Relevance Score: {score_rr}")

    sample = SingleTurnSample(
            user_input="When was the first super bowl?",
            response="The first superbowl was held on Jan 15, 1967",
            retrieved_contexts=[
                "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
            ]
        )
    my_device = "cuda:0"
    my_batch_size = 10

    faithfulness = FaithfulnesswithHHEM(device=my_device, batch_size=my_batch_size,llm="llamaAyudas:latest")
    #faithfulness = FaithfulnesswithHHEM(str="generate",llm="llamaAyudas:latest")
    scorer_f = await faithfulness.single_turn_ascore(sample)
    print(f"Faithfulness Score: {scorer_f}") """

# Ejecutar el programa asincrónico
asyncio.run(main())



