#EMBEDDING_MODEL_PATH = "microsoft/mpnet-base"  # OR Path of local eg. "embedding_model/"" or the name of SentenceTransformer model eg. "sentence-transformers/all-mpnet-base-v2" from Hugging Face
#EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
#EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
#EMBEDDING_MODEL_PATH = "all-MiniLM-L6-v2"
ASSYMETRIC_EMBEDDING = False  # Flag for asymmetric embedding
#EMBEDDING_DIMENSION = 768  # Embedding model settings
EMBEDDING_DIMENSION = 384  # Embedding model settings
TEXT_CHUNK_SIZE = 300  # Maximum number of characters in each text chunk for

""" OLLAMA_MODEL_NAME = (
    "llama3.2:1b"  # Name of the model used in Ollama for chat functionality
) """

""" OLLAMA_MODEL_NAME = (
    "llama3.1"  # Name of the model used in Ollama for chat functionality
) """

OLLAMA_MODEL_NAME = "llamaAyudas:latest"
OLLAMA_TEMPERATURE = 0.9


URL_WEB = "https://www.desimarti.es"
LOGO_URL_LARGE = "images/LogoLargo.png"
LOGO_URL_SMALL = "images/LogoCorto.png"

HUMAN_ICON = "images/user.png"
AI_ICON = "images/gpt.png"
#Web hacer logo https://www.design.com/maker/logo/helping-hand-charity-heart-2930187?text=Ayuda.Me&colorPalette=blue&isVariation=True

####################################################################################################
# Dont change the following settings
####################################################################################################

# Logging
LOG_FILE_PATH = "./logs/applog.txt"  # File path for the application log file
# OpenSearch settings
OPENSEARCH_HOST = "localhost"  # Hostname for the OpenSearch instance
OPENSEARCH_PORT = 9200  # Port number for OpenSearch
OPENSEARCH_INDEX = "documents"  # Index name for storing documents in OpenSearch
PROMPT_TEMPLATE = """
            Eres un asistente chat (chatbot) para ayudar obtener información de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario para encontrar las subvenciones que necesite el usuario en base a sus criterios de búsqueda.
            * Proporciona detalles del organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Sofo ofrece información a partir del Contexto proporcionado.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.

            ----
            Contexto:
                {context}
            ....

            Pregunta: 
                {input}
            """


# CHROMADB
CHROMA_COLLECTION_NAME = "subvenciones"
CHROMA_PERSIST_PATH = "./chromadb/"
CHROMA_NUMDOCUMENTS = 3

SENTENCE_TRANSFORMER = "all-MiniLM-L6-v2"

# MOCK OBJECTS
MOCK_IDS=["795795", "795802", "795828"]

MOCK_DOCUMENTS=[
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


CHATBOT_WELLCOME = """
**Bienvenido al Chatbot de Ayudas y Subvenciones Públicas 👋**  
Este chatbot está diseñado para facilitarte la búsqueda de información sobre **ayudas** y **subvenciones** en España.  
Con un lenguaje sencillo y ejemplos prácticos, podrás encontrar la información que necesitas de manera rápida y eficiente.

#### **¿Cómo utilizar este chatbot?**
1. **Describe tu necesidad o interés**: Puedes preguntar sobre ayudas específicas o hacer consultas más generales.
2. **Filtra la información**: Usa términos como región, sector, tipo de beneficiario o palabra clave para precisar tu búsqueda.
3. **Recibe resultados claros**: Obtendrás información detallada sobre las ayudas disponibles, como su descripción, fechas clave y enlaces relevantes.

#### **Ejemplos básicos de consulta**
- **Por región**:  
  _"¿Qué ayudas están disponibles en la Comunidad Valenciana?"_
- **Por sector**:  
  _"¿Hay subvenciones para el sector agrícola?"_
- **Por tipo de beneficiario**:  
  _"¿Existen ayudas para PYMES en Madrid?"_
- **Por palabras clave**:  
  _"Busco subvenciones para mejora de viviendas."_

#### **Consejos útiles**
- Sé lo más específico posible para obtener resultados más relevantes.  
- Si no encuentras lo que buscas, prueba combinando criterios:  
  _"Ayudas en Andalucía para autónomos en el sector tecnológico."_

---
**¡Empieza ahora!** Escribe tu primera consulta y verás qué fácil es de usar.
"""

CHATBOT_INTRO = """
##### **Recordatorio: Uso del Chatbot de Ayudas y Subvenciones**  
- **Describe tu necesidad**: Pregunta por ayudas específicas o generales.  
    Ej.: _"¿Qué ayudas hay en Madrid para autónomos?"_  
- **Usa filtros**: Región, sector, tipo de beneficiario o palabras clave.  
    Ej.: _"Subvenciones para innovación tecnológica."_  
- **Sé específico**: Combina criterios para resultados más relevantes.  
    Ej.: _"Ayudas en Andalucía para pymes agrícolas."_  

**¡Prueba ahora y encuentra lo que necesitas!**
"""


TEXTO_AVISOLEGAL = """
**⚠️ Aviso importante ⚠️**

El presente asistente ha sido diseñado para proporcionar información basada en datos obtenidos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas <a href='https://www.pap.hacienda.gob.es/bdnstrans/GE/es/inicio'>(url acceso)</a> de la Intervención General de la Administración del Estado del 🏛️ Gobierno de España 🏛️. 

ℹ️ La Internvención General del Estado **NO apoya ni patrocina** este asistente, siendo agena a la existencia del mismo ℹ️.

**Descargo de responsabilidad**

A pesar de los esfuerzos realizados para garantizar la precisión y actualidad de la información proporcionada, no podemos garantizar que dicha información sea siempre completa, precisa o libre de errores.

El usuario reconoce que la información suministrada por el asistente puede contener imprecisiones, omisiones o errores, y se compromete a verificar la exactitud y validez de la información antes de tomar cualquier decisión basada en ella.

El uso del asistente es bajo el propio riesgo del usuario. En ningún caso nos hacemos responsables de los posibles errores, perjuicios o daños que puedan derivarse del uso o de la interpretación incorrecta de la información proporcionada, incluyendo pero no limitándose a decisiones de carácter administrativo, legal, financiero o de cualquier otro tipo.

Se recomienda encarecidamente al usuario que consulte con un experto o recurra a las fuentes oficiales para confirmar cualquier información relevante antes de actuar en base a la misma.

***Fecha de última actualización de los datos de las ayudas: 15/12/2024 a las 23:45 horas.***
"""

ESTILOS = """
    <style>
    /* Main background and text colors */
    body { background-color: #f0f8ff; color: #002B5B; }
    .sidebar .sidebar-content { background-color: #00233A; color: white; padding: 20px; border-right: 2px solid #003d5c; }
    .sidebar h2, .sidebar h4 { color: white; }
    .block-container { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1); }
    .footer-text { font-size: 1.1rem; font-weight: bold; color: black; text-align: center; margin-top: 10px; }
    .stButton button { background-color: #118ab2; color: white; border-radius: 5px; padding: 10px 20px; font-size: 16px; }
    .stButton button:hover { background-color: #07a6c2; color: white; }
    h1, h2, h3, h4 { color: #00233A; }
    .stChatMessage { background-color: #C8E1F0; color: #00233A; padding: 10px; border-radius: 5px; margin-bottom: 10px; }
    .stChatMessage.user { background-color: #118ab2; color: white; }
    </style>
    """

ESTILOS_INICIO = """
  <style>
  /* Main background and text colors */
  body {
      background-color: #f0f8ff;  /* Light cyan background */
      color: #002B5B;  /* Dark blue text for readability */
  }
  .sidebar .sidebar-content {
      background-color: #00233A;  /* Dark cyan sidebar background */
      color: white;
      padding: 20px;
      border-right: 2px solid #003d5c;  /* Darker border */
  }
  .sidebar h2, .sidebar h4 {
      color: white;  /* White text for sidebar headings */
  }
  .block-container {
      background-color: white;  /* White content background */
      border-radius: 10px;
      padding: 20px;
      box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);  /* Subtle shadow for modern look */
  }

  /* Center content inside columns */
  .stColumn {
      text-align: center;
  }
  /* Style for the centered and bold footer text */
  .footer-text {
      font-size: 1.1rem;
      font-weight: bold;
      color: black;
      text-align: center;
      margin-top: 10px;
  }
  /* Style buttons to look modern and attractive */
  .stButton button {
      background-color: #118ab2;
      color: white;
      border-radius: 5px;
      border: none;
      padding: 10px 20px;
      font-size: 16px;
      box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
  }
  .stButton button:hover {
      background-color: #07a6c2;
      color: white;
  }
  /* Headings inside the main page */
  h1, h2, h3, h4 {
      color: #00233A;
  }
  </style>
  """