# 📝 TFM Desiderio Martí Alcaraz - Grado en Ciencia de Datos (UOC - Universitat Oberta de Catalunya).

Bienvenido al Chatbot especializado en búsqueda de ayudas y subvenciones úblicas del Gobierno de España basado en RAG con LLMs locales.

### 🌟 Características principales
- **Consultas bd vectoriales:** Uso de búsquedas vectoriales con Chromadb.
- **Local LLM** Búsqueda de información en documentos mediante el uso de bases de datos vectoriales y LLM local  con Ollama o OPENAI.

### Ollama instalar modelo en local desde línea de comando on ollama
ollama pull llama3.2:1b

### Arrancar el modelo con OLlama
ollama run llama3.2:1b

### 🚀 Como comenzar
1. Clonar el repositorio: `git clone https://github.com/desimartiout/TFM_DesiMarti.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar fichero de parámetros en `constants.py` para elegir el modelo de embeddings y el modelo de LLM.
4. Ejecutar la aplicación Streamlit: `streamlit run Inicio.py`

### 📘 OPENAI

# SI QUIERES VER SI TIENES LA VARAIBLE DE ENTORNO PUEDES USAR ESTE CÓDIGO
# import os

# # Cargar la clave desde las variables de entorno
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if not openai_api_key:
#     raise ValueError("La clave de OpenAI no está configurada como variable de entorno.")

# # Usar la clave en tu código
# import openai
# openai.api_key = openai_api_key -->

### 📘 Web Scrapping de web de ayudas
Ejecutar .....


### 📘 Instalar ragas
Ejecutar ....

### 📘 Referencias
**Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas** (https://www.pap.hacienda.gob.es/bdnstrans/)
**Streamlit** (https://streamlit.io/)
**RAGAS** (https://docs.ragas.io/)
**CHROMA DB** (https://www.trychroma.com/)