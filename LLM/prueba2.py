#https://python.langchain.com/docs/integrations/chat/ollama/

from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama2",
    temperature=0,
    # other params...
)


from langchain_core.messages import AIMessage

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to Spanish. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)