#https://neo4j.com/developer-blog/knowledge-graph-rag-application/

#Neo4j Environment Setup

from langchain_community.graphs import Neo4jGraph

url = "bolt://localhost:7687"
username ="neo4j"
password = ""
graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)

#Dataset

import requests
import_url = "https://gist.githubusercontent.com/tomasonjo/08dc8ba0e19d592c4c3cde40dd6abcc3/raw/e90b0c9386bf8be15b199e8ac8f83fc265a2ac57/microservices.json"
import_query = requests.get(import_url).json()['query']
graph.query(
    import_query
)


#Neo4j Vector index

import os
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain_openai import OpenAIEmbeddings

os.environ['OPENAI_API_KEY'] = "sk-"

vector_index = Neo4jVector.from_existing_graph(
    OpenAIEmbeddings(),
    url=url,
    username=username,
    password=password,
    index_name='tasks',
    node_label="Task",
    text_node_properties=['name', 'description', 'status'],
    embedding_node_property='embedding',
)

response = vector_index.similarity_search(
    "How will RecommendationService be updated?"
)
print(response[0].page_content)

from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

vector_qa = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(), chain_type="stuff", retriever=vector_index.as_retriever())

vector_qa.invoke(
    {"query": "How will recommendation service be updated?"}
)

vector_qa.invoke(
    {"query": "How many open tickets there are?"}
)

graph.query(
    "MATCH (t:Task {status:'open'}) RETURN count(*)"
)

#Graph Cypher search

from langchain.chains import GraphCypherQAChain

graph.refresh_schema()

cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm = ChatOpenAI(temperature=0, model_name='gpt-4'),
    qa_llm = ChatOpenAI(temperature=0), graph=graph, verbose=True,
)

cypher_chain.invoke(
    {"query": "How many open tickets there are?"}
)


##Knowledge graph agent

from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain import hub


tools = [
    Tool(
        name="Tasks",
        func=vector_qa.invoke,
        description="""Useful when you need to answer questions about descriptions of tasks.
        Not useful for counting the number of tasks.
        Use full question as input.
        """,
    ),
    Tool(
        name="Graph",
        func=cypher_chain.invoke,
        description="""Useful when you need to answer questions about microservices,
        their dependencies or assigned people. Also useful for any sort of
        aggregation like counting the number of tasks, etc.
        Use full question as input.
        """,
    ),
]

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
agent = create_openai_functions_agent(
    ChatOpenAI(temperature=0, model_name='gpt-4'), tools, prompt
)
# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "Which team is assigned to maintain PaymentService?"})
print(response)

response = agent_executor.invoke({"input": "Which tasks have optimization in their description?"})
print(response)