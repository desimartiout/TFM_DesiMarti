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

### 📘 Web Scrapping de web de ayudas
Ejecutar .....


### 📘 Instalar ragas
Ejecutar ....

### 📘 Referencias
**Streamlit** (https://streamlit.io/)
**RAGAS** (https://docs.ragas.io/)
**CHROMA DB** (https://www.trychroma.com/)