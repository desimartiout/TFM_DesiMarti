#EMBEDDING_MODEL_PATH = "microsoft/mpnet-base"  # OR Path of local eg. "embedding_model/"" or the name of SentenceTransformer model eg. "sentence-transformers/all-mpnet-base-v2" from Hugging Face
#EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_MODEL_PATH = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
#paraphrase-multilingual-mpnet-base-v2
ASSYMETRIC_EMBEDDING = False  # Flag for asymmetric embedding
EMBEDDING_DIMENSION = 768  # Embedding model settings
TEXT_CHUNK_SIZE = 300  # Maximum number of characters in each text chunk for

""" OLLAMA_MODEL_NAME = (
    "llama3.2:1b"  # Name of the model used in Ollama for chat functionality
) """

OLLAMA_MODEL_NAME = (
    "llama3.1"  # Name of the model used in Ollama for chat functionality
)

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
