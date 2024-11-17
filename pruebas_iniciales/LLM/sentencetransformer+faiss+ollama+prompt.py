
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
import json

from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    FewShotPromptTemplate,
    PromptTemplate
)

# Paso 1: Cargar el JSON en un formato adecuado

data = [
    {
        "id": "1", 
        "text": "subvención y entrega dineraria sin contraprestación ofrecida por Ayuntamiento de Gandia (Gandia) con impacto en la COMUNIDAD VALENCIANA, ofrecida para personas físicas que no desarrollan actividad económica cuya finalidad es el acceso a la vivienda y fomento de la edificación. El título es '2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda'", 
        "json_data": json.dumps({"id":992327,"organo":{"nivel1":"GANDIA","nivel2":"AYUNTAMIENTO DE GANDIA","nivel3":""},"sedeElectronica":"https://gandia.sedelectronica.es/","codigoBDNS":"790767","fechaRecepcion":"2024-10-14T15:57:09+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":100000,"mrr":False,"descripcion":"2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"OTROS SERVICIOS","codigo":"S"}],"regiones":[{"descripcion":"ES52 - COMUNIDAD VALENCIANA"}],"descripcionFinalidad":"Acceso a la vivienda y fomento de la edificación","descripcionBasesReguladoras":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","urlBasesReguladoras":"www.bop.es","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"2024-10-31T00:00:00+01:00","fechaFinSolicitud":"2024-11-15T00:00:00+01:00","textInicio":"","textFin":"","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144216,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241011_Certificat_punt 4 Aprobación convocatoria ayuda alquiler residencia habitual, facilitar acceso a la vivienda. Exp. 35295-2024.pdf","long":344807,"datMod":"2024-10-14T18:15:02.000+02:00","datPublicacion":"2024-10-14T18:15:02.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."})
    },
    {
        "id": "1", 
        "text": "subvención y entrega dineraria sin contraprestación ofrecida por Ayuntamiento de Gandia (Gandia) con impacto en la COMUNIDAD VALENCIANA, ofrecida para personas físicas que no desarrollan actividad económica cuya finalidad es el acceso a la vivienda y fomento de la edificación. El título es '2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda'", 
        "json_data": json.dumps({"id":1234,"organo":{"nivel1":"GANDIA","nivel2":"AYUNTAMIENTO DE GANDIA","nivel3":""},"sedeElectronica":"https://gandia.sedelectronica.es/","codigoBDNS":"790767","fechaRecepcion":"2024-10-14T15:57:09+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN 2 "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":100000,"mrr":False,"descripcion":"2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"OTROS SERVICIOS","codigo":"S"}],"regiones":[{"descripcion":"ES52 - COMUNIDAD VALENCIANA"}],"descripcionFinalidad":"Acceso a la vivienda y fomento de la edificación","descripcionBasesReguladoras":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","urlBasesReguladoras":"www.bop.es","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"2024-10-31T00:00:00+01:00","fechaFinSolicitud":"2024-11-15T00:00:00+01:00","textInicio":"","textFin":"","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144216,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241011_Certificat_punt 4 Aprobación convocatoria ayuda alquiler residencia habitual, facilitar acceso a la vivienda. Exp. 35295-2024.pdf","long":344807,"datMod":"2024-10-14T18:15:02.000+02:00","datPublicacion":"2024-10-14T18:15:02.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."})
    },
    {
        "id": "2", 
        "text": "subvención y entrega dineraria sin contraprestación ofrecida por AYUNTAMIENTO DE VILLA DE MAZO (VILLA DE MAZO) con impacto en La Palma, ofrecida para PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA cuya finalidad es INDUSTRIA Y ENERGÍA. El título es 'SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024'", 
        "json_data": json.dumps({"id":992284,"organo":{"nivel1":"VILLA DE MAZO","nivel2":"AYUNTAMIENTO DE VILLA DE MAZO","nivel3":""},"sedeElectronica":"WWW.SEDELECTRONICA.VILLADEMAZO.ES","codigoBDNS":"790724","fechaRecepcion":"2024-10-14T14:24:36+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":70000,"mrr":False,"descripcion":"SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"SUMINISTRO DE ENERGÍA ELÉCTRICA, GAS, VAPOR Y AIRE ACONDICIONADO","codigo":"D"}],"regiones":[{"descripcion":"ES707 - La Palma"}],"descripcionFinalidad":"Industria y Energía","descripcionBasesReguladoras":"BASES GENERALES REGULADORAS DE LA CONCESION DE SUBVENCIONES EN REGIMEN DE CONCURRENCIA COMPETITIVA EN EL AYUNTAMIENTO DE VILLA DE MAZO (BOP SANTA CRUZ DE TFE 108 DE FECHA 06/09/2024)","urlBasesReguladoras":"https://www.bopsantacruzdetenerife.es/bopsc2/index.php","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"","fechaFinSolicitud":"","textInicio":"A PARTIR DEL DIA SIGUIENTE DE LA PUBLICACION DEL EXTRACTO DE LA CONVOCATORIA EN EL BOP de S/C TFE.","textFin":"QUINCE DIAS HABILES A PARTIR DE LA FECHA DE INICIO","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144134,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241014_Resolución_Decreto de Alcaldía _ Decreto de Presidencia _RESOLUCIONES ALCALDIA 2024 2024-1055 [APROBACIÓN DE LA CONVOCATORIA]_compressed (1).pdf","long":318170,"datMod":"2024-10-14T15:15:03.000+02:00","datPublicacion":"2024-10-14T15:15:03.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."})
    }
] 

# Convertimos el JSON en un documento Langchain

documents = []
for entry in data:
    doc = Document(
        page_content=entry["text"],
        metadata={"id": entry["id"], "json_data": entry["json_data"]}  # Puedes incluir más metadata si es necesario
    )
    documents.append(doc)

# Paso 2: Crear una base de datos vectorial con FAISS usando embeddings open source
#documents = [document]
model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo open source para embeddings

# Generamos embeddings manualmente
texts = [doc.page_content for doc in documents]
embeddings = model.encode(texts)  # Generar embeddings para la lista de textos

# Crear una lista de tuplas (texto, embedding) para `text_embeddings`
text_embeddings = list(zip(texts, embeddings))

# Utilizar `FAISS.from_embeddings` con los parámetros correctos
db = FAISS.from_embeddings(text_embeddings=text_embeddings, embedding=model.encode)

# Paso 3: Crear el modelo de lenguaje Ollama y el sistema de Recuperación QA
llm = OllamaLLM(model="llama3.1")

from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Crear un mensaje de sistema con instrucciones iniciales
system_template = SystemMessagePromptTemplate.from_template(
    template="Eres un asistente de búsquedas en base al contexto"
)

# Crear un mensaje humano con la consulta del usuario
human_template = HumanMessagePromptTemplate.from_template(
    template="Tengo una pregunta: {pregunta}"
)

# Combinar ambos en un solo prompt utilizando ChatPromptTemplate
chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])

pregunta = "¿Qué ayudas están disponibles en Gandia?"
resultados = db.similarity_search(pregunta, k=1)  # Recuperar los 3 documentos más relevantes
print("---------")
print(resultados)
print("---------")

contexto = "\n".join([doc.page_content for doc in resultados])  # Unir el contenido de los documentos

contexto_promp = {
    "contexto": contexto,
    "pregunta": pregunta
}

prompt_completo = chat_prompt.format(**contexto_promp)
# Mostrar el prompt final
print("*********")
print(prompt_completo)
print("*********")

# Ejemplo de cómo enviar este prompt a un LLM (supongamos que es un LLM basado en Ollama)
respuesta = llm.invoke(prompt_completo)
print(f"Respuesta del modelo: {respuesta}")
