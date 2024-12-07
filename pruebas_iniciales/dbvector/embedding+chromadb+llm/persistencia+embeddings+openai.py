import chromadb
import json
from sentence_transformers import SentenceTransformer
from langchain_ollama import OllamaLLM

#https://medium.com/@pierrelouislet/getting-started-with-chroma-db-a-beginners-tutorial-6efa32300902
#Ejemplo básico y para luego dockerizar chromadb

#https://docs.trychroma.com/guides

collection_name = "subvenciones"

client = chromadb.PersistentClient(path="./pruebas_iniciales/dbvector/chromadb/store/")

collection = client.get_or_create_collection(name=collection_name)

ids=["795795", "795802", "795828"]
documents=[
        """Convocatoria de ayuda o  subvención: 795795
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
            Descripción: Texto en castellano de la convocatoria, Nombre: Certificado_[2024_049_000185]_-_Copia_autentica_(1).pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795795/document/1159030 """,
                """Convocatoria de ayuda o  subvención: 795802
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
            Descripción: Texto en castellano de la convocatoria, Nombre: CSV-2024_JuntaGobiernoLocal_Sanidad_2.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795802/document/1156556 """,
            """Convocatoria de ayuda o  subvención: 795828
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
            Descripción: Documento de la convocatoria en español, Nombre: Extracto de la Convocatoria subvenciones sin ánimo de lucro 2024.pdf, Enlace: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatoria/795828/document/1156584 """
  ]
metadatas=[
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795795"},
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795802"},
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795828"}
  ]


# Inicializar un modelo de Sentence Transformer para obtener embeddings
#model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo open source para embeddings

def cargarDocumentos():
    # Generamos embeddings manualmente
    texts = [doc for doc in documents]
    embeddings = model.encode(texts)  # Generar embeddings para la lista de textos

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings
    )
    #Si los ids son iguales los reemplaza

if (collection.count()==0):
    cargarDocumentos()

# Función para realizar una consulta (simulando una búsqueda por texto)
def query_documents(client, collection_name, query_text):
    collection = client.get_collection(collection_name)
    
    # Generar el embedding para la consulta
    query_embedding = model.encode([query_text]).tolist()
    
    # Realizar una búsqueda de similitud
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )
    return results

query_text = "Puedes darme todo el contexto de ayudas en Murcia?"

results = query_documents(client, collection_name, query_text)

contexto = ""

# Mostrar resultados de la consulta
#print("Resultados de la consulta:")
for result in results["documents"]:
    #print(result)
    contexto += f"Texto: {result}\n"

#print(f"Contexto {contexto}:")

model="gpt-3.5-turbo"
temperature=0.7

import openai

# Configurar la clave de API de OpenAI
#openai.api_key = "TU_API_KEY"

def consultaBasica():
    # Consulta básica sin Prompt con GPT-3.5 Turbo
    prompt = f"Usando esta información: {contexto} \n Responde: {query_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente virtual experto en ayudas públicas del gobierno de España. Responde de manera precisa y solo utilizando la información proporcionada."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,  # Similar al parámetro `temperature` en Ollama
    )
    
    respuesta = response.choices[0].message["content"]
    
    # Imprimir la respuesta
    print(f"Prompt: {prompt}")
    print(f"Respuesta: {respuesta}")

#from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
#from langchain_community.chat_models import ChatOpenAI

from langchain_openai import ChatOpenAI

#pip install -U langchain-community

def consultaPrompt():
    # Configurar el modelo de OpenAI con LangChain
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,  # Utiliza la temperatura definida
    )
    
    # Crear el prompt en formato Chat
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Eres un asistente virtual para contestar a ayudas públicas del gobierno de España. Solo responde utilizando la información proporcionada. No inventes información adicional.",
            ),
            ("human", "{input}"),
        ]
    )
    
    queryContext = f"Usando esta información: {contexto}. Responde: {query_text}"

    # Encadenar el prompt con el modelo
    chain = prompt | llm
    ai_msg = chain.invoke({"input": queryContext})
    
    # Imprimir los resultados
    print("-----------------------")
    print(f"queryContext: {queryContext}")
    print("-----------------------")
    print(ai_msg.content)
    print("-----------------------")


#consultaBasica()

consultaPrompt()