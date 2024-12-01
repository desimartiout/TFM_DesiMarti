#EMBEDDING_MODEL_PATH = "microsoft/mpnet-base"  # OR Path of local eg. "embedding_model/"" or the name of SentenceTransformer model eg. "sentence-transformers/all-mpnet-base-v2" from Hugging Face
#EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#paraphrase-multilingual-mpnet-base-v2
ASSYMETRIC_EMBEDDING = False  # Flag for asymmetric embedding
#EMBEDDING_DIMENSION = 768  # Embedding model settings
EMBEDDING_DIMENSION = 384  # Embedding model settings
TEXT_CHUNK_SIZE = 300  # Maximum number of characters in each text chunk for

""" OLLAMA_MODEL_NAME = (
    "llama3.2:1b"  # Name of the model used in Ollama for chat functionality
) """

OLLAMA_MODEL_NAME = (
    "llama3.1"  # Name of the model used in Ollama for chat functionality
)
OLLAMA_TEMPERATURE=0.7

####################################################################################################
# Dont change the following settings
####################################################################################################

# Logging
LOG_FILE_PATH = "logs/app.log"  # File path for the application log file
# OpenSearch settings
OPENSEARCH_HOST = "localhost"  # Hostname for the OpenSearch instance
OPENSEARCH_PORT = 9200  # Port number for OpenSearch
OPENSEARCH_INDEX = "documents"  # Index name for storing documents in OpenSearch
PROMPT_TEMPLATE = """
            Eres un asistente chat (chatbot) para ayudar obtener ingformación de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario para encontrar las subvenciones que necesite el usuario en base a sus criterios de búsqueda.
            * Deberás de identificar las oportunidades de ayudas y subvenciones.
            * Proporciona detalles el organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Ofrece consejos sobre cómo mejorar mi aplicación y aumentar mis posibilidades de éxito.
            * Cuando te pregunten por las ayudas y subvenciones centrate en la información que te proporciona el contexto.

            * Es importante que los resultados sean precisos y actualizados.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.

            <context>
            {context}
            </context>

            Question: {input}
            """


# CHROMADB

CHROMA_COLLECTION_NAME = "subvenciones"
CHROMA_PERSIST_PATH = "./store/"

SENTENCE_TRANSFORMER = "all-MiniLM-L6-v2"

# MOCK OBJECTS
MOCK_IDS=["795795", "795802", "795828"]
MOCK_DOCCUMENTS=[
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
MOCK_METADATAS=[
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795795"},
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795802"},
   {"source": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/795828"}
  ]
