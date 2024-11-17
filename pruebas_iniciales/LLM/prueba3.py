#https://python.langchain.com/docs/integrations/chat/ollama/

from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama2",
    temperature=0,
    # other params...
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Tu eres un asistente traductor que traduce de {input_language} a {output_language}.",
        ),
        ("human", "{input}"),
    ]
)

chain = prompt | llm
ai_msg = chain.invoke(
    {
        "input_language": "Inglés",
        "output_language": "Español",
        "input": "My father is Jhon.",
    }
)
print(ai_msg.content)