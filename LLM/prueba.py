#https://medium.com/@abonia/ollama-and-langchain-run-llms-locally-900931914a46

#from langchain_community.llms import Ollama

#llm = Ollama(model="llama2")

#llm.invoke("Tell me a joke")


from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Question: {question}

Answer: Let's think step by step."""

prompt = ChatPromptTemplate.from_template(template)

#model = OllamaLLM(model="llama3.1")
model = OllamaLLM(model="llama2")

str = model.invoke("Tell me a joke")
print(str)

#chain = prompt | model
#str = chain.invoke({"question": "What is LangChain?"})
#print(str)