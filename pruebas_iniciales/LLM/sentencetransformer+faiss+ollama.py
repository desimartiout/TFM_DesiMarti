
#pip install langchain openai faiss-cpu
#pip install -U langchain-community

from sentence_transformers import SentenceTransformer
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import JSONLoader
from langchain.chains import RetrievalQA
#from langchain.llms import Ollama
from langchain_ollama.llms import OllamaLLM
from langchain.schema import Document

# Paso 1: Cargar el JSON en un formato adecuado
data = {
    "id": "1",
    "text": "subvención y entrega dineraria sin contraprestación ofrecida por Ayuntamiento de Gandia (Gandia) con impacto en la COMUNIDAD VALENCIANA, ofrecida para personas físicas que no desarrollan actividad económica cuya finalidad es el acceso a la vivienda y fomento de la edificación.",
    "json_data": {
        "id": 992327,
        "organo": {
            "nivel1": "GANDIA",
            "nivel2": "AYUNTAMIENTO DE GANDIA",
            "nivel3": ""
        },
        "sedeElectronica": "https://gandia.sedelectronica.es/",
        "codigoBDNS": "790767",
        "fechaRecepcion": "2024-10-14T15:57:09+02:00",
        "instrumentos": [
            {
                "descripcion": "SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN"
            }
        ],
        "tipoConvocatoria": "Concurrencia competitiva - canónica",
        "presupuestoTotal": 100000,
        "mrr": False,
        "descripcion": "2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.",
        "tiposBeneficiarios": [
            {
                "descripcion": "PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"
            }
        ],
        "sectores": [
            {
                "descripcion": "OTROS SERVICIOS",
                "codigo": "S"
            }
        ],
        "regiones": [
            {
                "descripcion": "ES52 - COMUNIDAD VALENCIANA"
            }
        ],
        "fechaInicioSolicitud": "2024-10-31T00:00:00+01:00",
        "fechaFinSolicitud": "2024-11-15T00:00:00+01:00"
    }
}

# Convertimos el JSON en un documento Langchain
document = Document(
    page_content=data["text"],
    metadata=data["json_data"]
)

""" # Paso 2: Crear una base de datos vectorial con FAISS
documents = [document]
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings) """

# Paso 2: Crear una base de datos vectorial con FAISS usando embeddings open source
documents = [document]
#model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo open source para embeddings
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')  # Modelo open source para embeddings

# Generamos embeddings manualmente
texts = [doc.page_content for doc in documents]
embeddings = model.encode(texts)  # Generar embeddings para la lista de textos

# Crear una lista de tuplas (texto, embedding) para `text_embeddings`
text_embeddings = list(zip(texts, embeddings))

# Utilizar `FAISS.from_embeddings` con los parámetros correctos
db = FAISS.from_embeddings(text_embeddings=text_embeddings, embedding=model.encode)

# Paso 3: Crear el modelo de lenguaje Ollama y el sistema de Recuperación QA
llm = OllamaLLM(model="llama3.1")

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever()
)

# Paso 4: Realizar una consulta
pregunta = "¿Qué ayudas están disponibles para personas físicas que no desarrollan actividad económica en la Comunidad Valenciana?"

respuesta = qa_chain.run(pregunta)

# Mostrar la respuesta
print(f"Respuesta: {respuesta}")
