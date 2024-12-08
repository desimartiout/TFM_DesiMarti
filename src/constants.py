import yaml

# Cargar textos desde un archivo YAML
with open("./locale/es/text.yaml", "r", encoding="utf-8") as file:
    texts = yaml.safe_load(file)

####################################################################################################
#                   CONFIGURACIÓN DB VECTORIAL Y GENERACIÓN EMBEDDINGS
####################################################################################################

EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
#EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
#EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#EMBEDDING_MODEL_PATH = "microsoft/mpnet-base"  # OR Path of local eg. "embedding_model/"" or the name of SentenceTransformer model eg. "sentence-transformers/all-mpnet-base-v2" from Hugging Face
#EMBEDDING_MODEL_PATH = "all-MiniLM-L6-v2"

ASSYMETRIC_EMBEDDING = False  # Flag for asymmetric embedding
EMBEDDING_DIMENSION = 384  # Embedding model settings
#EMBEDDING_DIMENSION = 768  # Embedding model settings
TEXT_CHUNK_SIZE = 300  # Maximum number of characters in each text chunk for

# CHROMADB
CHROMA_COLLECTION_NAME = "subvenciones"
CHROMA_PERSIST_PATH = "./chromadb/"
CHROMA_NUMDOCUMENTS = 3

SENTENCE_TRANSFORMER = "all-MiniLM-L6-v2"

#CADENAS A UTILIZAR PARA ASIGNAR EL TIPO DE MODELO A LA CONSTANTE LLM_MODELO_SELECCIONADO
LLM_TIPOMODELO_OLLAMA = "OLLAMA"
LLM_TIPOMODELO_OPENAI = "OPENAI"

# CONFIGURACIÓN DEL MODELO A UTILIZAR OLLAMA (requiere su instalación en local) o OPENAI (Requiere tener una API KEY de OPENAI)
#LLM_MODELO_SELECCIONADO = LLM_TIPOMODELO_OLLAMA
OLLAMA_MODEL_NAME = "llamaAyudas:latest"
# OLLAMA_MODEL_NAME = (
#     "llama3.2:1b"
# )
# OLLAMA_MODEL_NAME = (
#     "llama3.1"
# )
OLLAMA_TEMPERATURE = 0.9

LLM_MODELO_SELECCIONADO = LLM_TIPOMODELO_OPENAI #--> OPCION CON OPENAI QUE REQUIERE DE TENER LA VARIABLE DE ENTORNO CON EL API KEY DE OPENAI
OPENAI_MODEL_NAME = "gpt-3.5-turbo"     #(en este caso GPT-3.5 Turbo)
# SI QUIERES VER SI TIENES LA VARAIBLE DE ENTORNO PUEDES USAR ESTE CÓDIGO
# import os
# # Cargar la clave desde las variables de entorno
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
#     raise ValueError("La clave de OpenAI no está configurada como variable de entorno.")
# # Usar la clave en tu código
# import openai
# openai.api_key = openai_api_key

####################################################################################################
# CONFIGURACIÓN DE LA APLICACIÓN - TOCAR CON CUIDADO
####################################################################################################

# Logging
LOG_FILE_PATH = "./logs/applog.txt"  # File path for the application log file
# # OpenSearch settings
# OPENSEARCH_HOST = "localhost"  # Hostname for the OpenSearch instance
# OPENSEARCH_PORT = 9200  # Port number for OpenSearch
# OPENSEARCH_INDEX = "documents"  # Index name for storing documents in OpenSearch

####################################################################################################
#                                   TEXTOS
####################################################################################################
PROMPT_TEMPLATE = texts["prompt_template"]  #Template de Ollama
OPENAI_TEMPLATE = texts["openai_template"]  #Template de OPENAI

CHATBOT_WELLCOME = texts["chatbot_wellcome"]
CHATBOT_INTRO = texts["chatbot_intro"]
TEXTO_AVISOLEGAL = texts["texto_avisolegal"]

####################################################################################################
#                                   CONFIGURACIÓN DE LA WEB
####################################################################################################

URL_WEB = "https://www.desimarti.es"
LOGO_URL_LARGE = "images/LogoLargo.png"
LOGO_URL_SMALL = "images/LogoCorto.png"
HUMAN_ICON = "images/user.png"

if LLM_MODELO_SELECCIONADO == LLM_TIPOMODELO_OLLAMA:
    AI_ICON = "images/ollama.png"
else:
    AI_ICON = "images/openai.png"
#Web hacer logo https://www.design.com/maker/logo/helping-hand-charity-heart-2930187?text=Ayuda.Me&colorPalette=blue&isVariation=True

####################################################################################################
#                                   ESTILOS
####################################################################################################

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
    .st-emotion-cache-1c7y2kd {
        flex-direction: row-reverse;
        text-align: right;
        background-color: white;
    }
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

####################################################################################################
#                                   MOCKS PARA PRUEBAS
####################################################################################################

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