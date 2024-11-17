#https://medium.com/@abonia/ollama-and-langchain-run-llms-locally-900931914a46

#from langchain_core.callbacks.manager import CallbackManager
#from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#from langchain_ollama.llms import OllamaLLM

#llm = OllamaLLM(
#    model="mistral", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
#)
#llm("The first man on the summit of Mount Everest, the highest peak on Earth, was ...")

from typing import List
from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from langserve import add_routes
import uvicorn

llama2 = OllamaLLM(model="llama2")
template = PromptTemplate.from_template("Tell me a joke about {topic}.")
chain = template | llama2 | CommaSeparatedListOutputParser()

app = FastAPI(title="LangChain", version="1.0", description="The first server ever!")
add_routes(app, chain, path="/chain")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)


#http://localhost:8000/chain/playground/