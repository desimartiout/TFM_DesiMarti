#https://github.com/tomasonjo/blogs/blob/master/llm/neo4j_llama_multimodal.ipynb

#Multimodal RAG pipeline with LlamaIndex and Neo4j
#Retrieve and combine information from text and images to generate an accurate response with multimodal LLMs

#Comandos en consola
#!pip install llama_index neo4j torch torchvision git+https://github.com/openai/CLIP.git beautifulsoup4
#!wget https://github.com/tomasonjo/blog-datasets/raw/main/articles.zip
#!unzip articles.zip

import os
from bs4 import BeautifulSoup, NavigableString
from llama_index.indices.multi_modal.base import MultiModalVectorStoreIndex
from llama_index.vector_stores import Neo4jVectorStore
from llama_index import StorageContext, Document
from llama_index.schema import ImageDocument
from llama_index.node_parser import SimpleNodeParser
from llama_index.multi_modal_llms.openai import OpenAIMultiModal
import tiktoken
import seaborn as sns
import requests
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO

os.environ["OPENAI_API_KEY"] = "sk-"
NEO4J_URI="bolt://localhost:7687"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="12345678"

def process_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Find the required section
    content_section = soup.find("section", {"data-field": "body", "class": "e-content"})

    if not content_section:
        return "Section not found."

    sections = []
    current_section = {"header": "", "content": "", "source": file_path.split("/")[-1]}
    images = []
    header_found = False

    for element in content_section.find_all(recursive=True):
        if element.name in ["h1", "h2", "h3", "h4"]:
            if header_found and (current_section["content"].strip()):
                sections.append(current_section)
            current_section = {
                "header": element.get_text(),
                "content": "",
                "source": file_path.split("/")[-1],
            }
            header_found = True
        elif header_found:
            if element.name == "pre":
                current_section["content"] += f"```{element.get_text().strip()}```\n"
            elif element.name == "img":
                img_src = element.get("src")
                img_caption = element.find_next("figcaption")
                caption_text = img_caption.get_text().strip() if img_caption else ""
                images.append(ImageDocument(image_url=img_src))
            elif element.name in ["p", "span", "a"]:
                current_section["content"] += element.get_text().strip() + "\n"

    if current_section["content"].strip():
        sections.append(current_section)

    return images, sections

all_documents = []
all_images = []

# Directory to search in (current working directory)
directory = os.getcwd()

# Walking through the directory
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".html"):
            # Update the file path to be relative to the current directory
            images, documents = process_html_file(os.path.join(root, file))
            all_documents.extend(documents)
            all_images.extend(images)

text_docs = [Document(text=el.pop("content"), metadata=el) for el in all_documents]
print(f"Text document count: {len(text_docs)}")
print(f"Image document count: {len(all_images)}")



text_store = Neo4jVectorStore(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name="text_collection",
    node_label="Chunk",
    embedding_dimension=1536
)

image_store = Neo4jVectorStore(
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name="image_collection",
    node_label="Image",
    embedding_dimension=512

)
storage_context = StorageContext.from_defaults(vector_store=text_store)

# Takes 10 min without GPU / 1 min with GPU on Google collab
index = MultiModalVectorStoreIndex.from_documents(
    text_docs + all_images, storage_context=storage_context, image_vector_store=image_store
)

#Multimodal RAG pipeline

from llama_index.prompts import PromptTemplate
from llama_index.query_engine import SimpleMultiModalQueryEngine

openai_mm_llm = OpenAIMultiModal(
    model="gpt-4-vision-preview", max_new_tokens=1500
)


qa_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)
qa_tmpl = PromptTemplate(qa_tmpl_str)

query_engine = index.as_query_engine(
    multi_modal_llm=openai_mm_llm, text_qa_template=qa_tmpl
)

query_str = "How do vector RAG application work?"
response = query_engine.query(query_str)
print(response)

def plot_images(image_urls):
    images_shown = 0
    plt.figure(figsize=(25, 15))
    for img_url in image_urls:
        try:
            response = requests.get(img_url)
            response.raise_for_status()  # Raise an error for bad status codes
            image = Image.open(BytesIO(response.content))

            plt.subplot(1, 3, images_shown + 1)  # Layout adjusted for 3 images
            plt.imshow(image)
            plt.xticks([])
            plt.yticks([])

            images_shown += 1
            if images_shown >= 4:  # Break after displaying 3 images
                break
        except Exception as e:
            print(f"Error loading image {img_url}: {e}")

plot_images([n.node.image_url for n in response.metadata["image_nodes"]])