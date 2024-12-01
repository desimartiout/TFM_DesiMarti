import chromadb
from chromadb.config import Settings

from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document

from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings

#Deprecated
#from langchain.embeddings import HuggingFaceEmbeddings
#from langchain.llms import Ollama

from chromadb.config import Settings

persist_directory = "./store/chromadb"

# Initialize the Chroma client with the persistence directory
chroma_client = chromadb.Client(Settings(
    persist_directory=persist_directory
))

# Crear o cargar una colección
collection = chroma_client.get_or_create_collection(name="ayudas")

# Configuración de embeddings usando un modelo Hugging Face (puedes cambiarlo según tu preferencia)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def listardocumentos(vector_store,collection):
    # Recuperar documentos de FAISS
    vector_store = FAISS.load_local("store/faiss_index", embedding_model, allow_dangerous_deserialization=True)
    
    print("Documentos en FAISS:")
    for doc in vector_store.similarity_search("subvenciones", k=10):
        print(doc.page_content)

    # Recuperar documentos de ChromaDB
    collection = chroma_client.get_collection("ayudas")
    print("\nDocumentos en ChromaDB:")
    for doc in collection.get()["documents"]:
        print(doc)

def buscar_en_documentos(vector_store,collection,query):

    # Búsqueda en FAISS
    faiss_results = vector_store.similarity_search(query, k=2)
    print("Resultados de búsqueda en FAISS:")
    for res in faiss_results:
        print(res.page_content)

    # Búsqueda en ChromaDB
    query_embedding = embedding_model.embed_query(query)
    chroma_results = collection.query(query_embeddings=[query_embedding], n_results=2)

    print("\nResultados de búsqueda en ChromaDB:")
    for res in chroma_results["documents"]:
        print(res[0])

    """     # Ampliar la respuesta con Ollama
    llm = Ollama(model="llama", base_url="http://localhost:11434")
    context = "\n".join([doc.page_content for doc in faiss_results])
    response = llm(f"Usando esta información: {context}\nResponde: ¿Qué ayudas públicas están disponibles para vivienda?")
    print("\nRespuesta del modelo LLM:")
    print(response) """

    # Paso 3: Crear el modelo de lenguaje Ollama y el sistema de Recuperación QA
    # Crea una instancia del modelo Ollama
    #llm = Ollama(model="llama3.2:1b", temperature=0.7)
    llm = OllamaLLM(model="llama3.2:1b", temperature=0.7)

    #Basada en el resultado de FAISS
    context = "\n".join([doc.page_content for doc in faiss_results])

    #Basada en el resultado de ChromaDB
    respuesta = llm(f"Usando esta información: {context}\nResponde: ¿Qué ayudas públicas están disponibles para vivienda?")

    # Imprimir la respuesta
    print(f"Respuesta: {respuesta}")
    


# Simulación de documentos para subir al índice
documents = [
    Document(page_content="""Convocatoria de ayuda o  subvención: 795795
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795795
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: MURCIA - AYUNTAMIENTO DE MURCIA
    Enlace / url a sede electrónica presentación ayuda: https://sede.murcia.es/areas?idCategoria=10004
    Fecha de recepción: 2024-11-08T14:18:10+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 205000 Euros
    Descripción: 2024_Conc_Costes explotación taxis adaptados_2024 049 4411 47906_100217_795795
    Tipos de beneficiarios: PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: Otro transporte terrestre de pasajeros
    Región de impacto: ES62 - REGION DE MURCIA
    Finalidad: Subvenciones al transporte
    Bases reguladoras: ORDENANZA GENERAL DE SUBVENCIONES Y PREMIOS DEL AYUNTAMIENTO DE MURCIA
    URL Bases Reguladoras: https://www.borm.es/services/anuncio/ano/2023/numero/843/pdf
    Publicación en diario oficial: Sí
    Estado de convocatoria abierta: No
    Fecha de inicio de solicitudes: 2024-11-15T00:00:00+01:00
    Fecha de fin de solicitudes: 2024-11-28T00:00:00+01:00
    Inicio de convocatoria: Plazo inicia el 1º dia hábil siguiente a la publicación del extracto en el BORM
    Fin de convocatoria: 10 días desde el día siguiente a la publicación del extracto en el BORM
    Reglamento: 
    Otros documentos de la convocatoria: 
    Descripción: PUBLICACION EN EL BORM, Nombre: PUBLICACION_BORM.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159031 , 
    Descripción: Texto en castellano de la convocatoria, Nombre: Certificado_[2024_049_000185]_-_Copia_autentica_(1).pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159030 """),
    Document(page_content="""Convocatoria de ayuda o  subvención: 795802
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795802
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: CHICLANA DE LA FRONTERA - AYUNTAMIENTO DE CHICLANA DE LA FRONTERA
    Enlace / url a sede electrónica presentación ayuda: https://www.chiclana.es
    Fecha de recepción: 2024-11-08T14:30:52+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 22000 Euros
    Descripción: CONVOCATORIA PÚBLICA DE SUBVENCIONES DE SALUD EJERCICIO 2024.
    Tipos de beneficiarios: PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA, PERSONAS JURÍDICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: Prestación de servicios a la comunidad en general
    Región de impacto: ES61 - ANDALUCIA
    Finalidad: Sanidad
    Bases reguladoras: CONVOCATORIA SUBVENCIONES DELEGACIÓN DE SALUD 2024.
    URL Bases Reguladoras: https://www.chiclana.es
    Publicación en diario oficial: Sí
    Estado de convocatoria abierta: No
    Fecha de inicio de solicitudes: 
    Fecha de fin de solicitudes: 
    Inicio de convocatoria: DÍA SIGUIENTE AL DE SU PUBLICACIÓN EN EL B.O.P. DE CÁDIZ
    Fin de convocatoria: TREINTA DÍAS NATURALES SIGUIENTE AL DE SU PUBLICACIÓN
    Reglamento: 
    Otros documentos de la convocatoria: 
    Descripción: Texto en castellano de la convocatoria, Nombre: CSV-2024_JuntaGobiernoLocal_Sanidad_2.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795802/document/1156556 """),
    Document(page_content="""Convocatoria de ayuda o  subvención: 795828
    Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795828
    Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: FERNÁN-NÚÑEZ - AYUNTAMIENTO DE FERNÁN-NÚÑEZ
    Enlace / url a sede electrónica presentación ayuda: 
    Fecha de recepción: 2024-11-08T15:03:45+01:00
    Tipo de ayuda: SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN 
    Tipo de convocatoria: Concurrencia competitiva - canónica
    Presupuesto total: 53464 Euros
    Descripción: SUBVENCIONES A ENTIDADES LOCALES SIN ÁNIMO DE LUCRO PARA EL AÑO 2024
    Tipos de beneficiarios: PERSONAS JURÍDICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA
    Sectores involucrados: EDUCACIÓN, OTROS SERVICIOS
    Región de impacto: ES613 - Córdoba
    Finalidad: Cultura
    Bases reguladoras: Extracto de la convocatoria de subvenciones a entidades locales sin ánimo de lucro de Fernán Núñez
    URL Bases Reguladoras: https://bop.dipucordoba.es/visor-pdf/26-02-2019/BOP-A-2019-475.pdf
    Publicación en diario oficial: Sí
    Estado de convocatoria abierta: No
    Fecha de inicio de solicitudes: 
    Fecha de fin de solicitudes: 
    Inicio de convocatoria: Día siguiente a la  la publicacion en el BOP
    Fin de convocatoria: 10 días hábiles
    Reglamento: 
    Otros documentos de la convocatoria: 
    Descripción: Bases reguladoras de la subvenciones a entidades locales sin animo de lucro 2024, Nombre: Bases Reguladoras Convocatoria Subvenciones sin animo de lucro2024.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795828/document/1156590 , 
    Descripción: Documento de la convocatoria en español, Nombre: Extracto de la Convocatoria subvenciones sin ánimo de lucro 2024.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795828/document/1156584 """),
]

# Crear un vectorstore con FAISS
vector_store = FAISS.from_documents(documents, embedding_model)

# Guardar el índice FAISS localmente
vector_store.save_local("store/faiss_index")

for i, doc in enumerate(documents):
    collection.add(
        documents=[doc.page_content],
        metadatas=[{"source": "documento_inicial"}],
        ids=[f"doc_{i}"]
    )

print("Documentos subidos a FAISS y ChromaDB.")


listardocumentos(vector_store, collection)

buscar_en_documentos(vector_store, collection, "ayudas públicas para vivienda")