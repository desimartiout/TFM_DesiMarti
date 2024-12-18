#https://huggingface.co/blog/getting-started-with-embeddings

import chromadb
import json
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.create_collection("subvenciones")  # Crea o usa una colección existente
#model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo de embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Puedes probar modelos más grandes si tu GPU lo soporta


# Ejemplo de datos
data = [
    {
        "id": "1", 
        "text": "subvención y entrega dineraria sin contraprestación ofrecida por Ayuntamiento de Gandia (Gandia) con impacto en la COMUNIDAD VALENCIANA, ofrecida para personas físicas que no desarrollan actividad económica cuya finalidad es el acceso a la vivienda y fomento de la edificación. El título es '2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda'", 
        "json_data": json.dumps({"id":992327,"organo":{"nivel1":"GANDIA","nivel2":"AYUNTAMIENTO DE GANDIA","nivel3":""},"sedeElectronica":"https://gandia.sedelectronica.es/","codigoBDNS":"790767","fechaRecepcion":"2024-10-14T15:57:09+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":100000,"mrr":False,"descripcion":"2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"OTROS SERVICIOS","codigo":"S"}],"regiones":[{"descripcion":"ES52 - COMUNIDAD VALENCIANA"}],"descripcionFinalidad":"Acceso a la vivienda y fomento de la edificación","descripcionBasesReguladoras":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","urlBasesReguladoras":"www.bop.es","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"2024-10-31T00:00:00+01:00","fechaFinSolicitud":"2024-11-15T00:00:00+01:00","textInicio":"","textFin":"","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144216,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241011_Certificat_punt 4 Aprobación convocatoria ayuda alquiler residencia habitual, facilitar acceso a la vivienda. Exp. 35295-2024.pdf","long":344807,"datMod":"2024-10-14T18:15:02.000+02:00","datPublicacion":"2024-10-14T18:15:02.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."})
    },
    {
        "id": "2", 
        "text": "subvención y entrega dineraria sin contraprestación ofrecida por AYUNTAMIENTO DE VILLA DE MAZO (VILLA DE MAZO) con impacto en La Palma, ofrecida para PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA cuya finalidad es INDUSTRIA Y ENERGÍA. El título es 'SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024'", 
        "json_data": json.dumps({"id":992284,"organo":{"nivel1":"VILLA DE MAZO","nivel2":"AYUNTAMIENTO DE VILLA DE MAZO","nivel3":""},"sedeElectronica":"WWW.SEDELECTRONICA.VILLADEMAZO.ES","codigoBDNS":"790724","fechaRecepcion":"2024-10-14T14:24:36+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":70000,"mrr":False,"descripcion":"SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"SUMINISTRO DE ENERGÍA ELÉCTRICA, GAS, VAPOR Y AIRE ACONDICIONADO","codigo":"D"}],"regiones":[{"descripcion":"ES707 - La Palma"}],"descripcionFinalidad":"Industria y Energía","descripcionBasesReguladoras":"BASES GENERALES REGULADORAS DE LA CONCESION DE SUBVENCIONES EN REGIMEN DE CONCURRENCIA COMPETITIVA EN EL AYUNTAMIENTO DE VILLA DE MAZO (BOP SANTA CRUZ DE TFE 108 DE FECHA 06/09/2024)","urlBasesReguladoras":"https://www.bopsantacruzdetenerife.es/bopsc2/index.php","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"","fechaFinSolicitud":"","textInicio":"A PARTIR DEL DIA SIGUIENTE DE LA PUBLICACION DEL EXTRACTO DE LA CONVOCATORIA EN EL BOP de S/C TFE.","textFin":"QUINCE DIAS HABILES A PARTIR DE LA FECHA DE INICIO","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144134,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241014_Resolución_Decreto de Alcaldía _ Decreto de Presidencia _RESOLUCIONES ALCALDIA 2024 2024-1055 [APROBACIÓN DE LA CONVOCATORIA]_compressed (1).pdf","long":318170,"datMod":"2024-10-14T15:15:03.000+02:00","datPublicacion":"2024-10-14T15:15:03.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."})
    }
] 

""" # Ejemplo de datos (texto y JSON)
data = [
    {
        "id": "1", 
        "text": "Convocatoria de ayudas para proyectos de innovación tecnológica.", 
        "json_data": json.dumps({
            "organo": "MINISTERIO DE CIENCIA E INNOVACIÓN",
            "tipoConvocatoria": "Concurrencia competitiva",
            "presupuestoTotal": 500000,
            "sectores": [{"descripcion": "INNOVACIÓN TECNOLÓGICA"}]
        })
    },
    {
        "id": "2", 
        "text": "Subvenciones para la rehabilitación de edificios en zonas rurales.", 
        "json_data": json.dumps({
            "organo": "MINISTERIO DE TRANSPORTES",
            "tipoConvocatoria": "Concesión directa",
            "presupuestoTotal": 2000000,
            "sectores": [{"descripcion": "REHABILITACIÓN"}]
        })
    },
    {
        "id": "3", 
        "text": "Ayudas para la investigación y desarrollo en el sector energético.", 
        "json_data": json.dumps({
            "organo": "MINISTERIO DE TRANSICIÓN ECOLÓGICA",
            "tipoConvocatoria": "Concurrencia competitiva",
            "presupuestoTotal": 1000000,
            "sectores": [{"descripcion": "ENERGÍA"}]
        })
    }
] """

# Insertamos los documentos en la colección de ChromaDB con el JSON como metadatos
for item in data:
    embedding = model.encode(item['text'])
    collection.add(
        ids=[item['id']],  # Proporcionamos el ID único
        documents=[item['text']],  # El texto de los documentos
        embeddings=[embedding.tolist()],  # Convertimos el embedding en lista
        metadatas=[{"json_data": item['json_data']}]  # Metadatos con el JSON
    )

# Pregunta del usuario
query = "¿Qué subvenciones hay sobre investigación?"

# Generamos el embedding de la consulta
query_embedding = model.encode(query)

# Consultamos en ChromaDB
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=1  # Número de resultados que queremos obtener
)

context = ""
# Mostramos los resultados junto con el JSON asociado
for i, result in enumerate(results['documents'][0]):
    metadata = json.loads(results['metadatas'][0][i]['json_data'])  # Recuperamos el JSON del metadato
    """ print(f"Resultado {i+1}:")
    print(f"Texto: {result}")
    print(f"JSON: {json.dumps(metadata, indent=4)}") """

    context += f"Texto: {result}\n"
    context += f"Detalles adicionales: {json.dumps(metadata, indent=4)}\n\n"

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
            "You are a Virtual assistant to help users to ask questions about aid and subsidies in Spanish State, you must ask in spanish languaje.",
        ),
        ("human", "{input}"),
    ]
)

#ValueError: Unexpected message type: Sistema. Use one of 'human', 'user', 'ai', 'assistant', or 'system'

queryContext = f"Con el siguiente contexto: {context}. {query}" 

chain = prompt | llm
ai_msg = chain.invoke(
    {
        "input": "{queryContext}",
    }
)
print(ai_msg)
#print(ai_msg.content)

""" messages = [
    (
        "system",
        "You are a Virtual assistant to help users to ask questions about aid and subsidies in Spanish State, you must ask in spanish languaje.",
    ),
    ("human", "¿Qué subvenciones hay en investigación?"),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content) """