# 📝 TFM Desiderio Martí Alcaraz - Grado en Ciencia de Datos de Universitat Oberta de Catalunya.

Bienvenido al Chatbot especializado en búsqueda de ayudas y subvenciones úblicas del Gobierno de España basado en RAG con LLMs locales.

### 🌟 Características principales
- **Local LLM** Búsqueda de información en documentos mediante el uso de bases de datos vectoriales y LLM local.
- **Consultas híbridas con OpenSearch:** Uso de búsquedas tradicionales junto con búsquedas semánticas con OpenSearch.

### 🚀 Como comenzar
1. Clonar el repositorio: `git clone https://github.com/JAMwithAI/build_your_local_RAG_system.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar fichero de parámetros en `constants.py` para elegir el modelo de embeddings y las configuraciones de OpenSearch.
4. Ejecutar la aplicación Streamlit: `streamlit run welcome.py`


pip show rapidfuzz  --> Ver versiones de librerías

### 📘 Descargar imágenes de docket de OpenSearch y arrancarlas

docker run -d --name opensearch -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "DISABLE_SECURITY_PLUGIN=true" opensearchproject/opensearch:2.11.0
docker run -d --name opensearch-dashboards -p 5601:5601 --link opensearch:opensearch -e "OPENSEARCH_HOSTS=http://opensearch:9200" -e "DISABLE_SECURITY_DASHBOARDS_PLUGIN=true" opensearchproject/opensearch-dashboards:2.11.0

### Abrir dashboard de OpenSearch
http://localhost:5601/app/home

### Crear el pipeline para la búsqueda híbrida
En el dashboard de OpenSearch acceder a Dev tools y ejecutar este comando http

PUT /_search/pipeline/nlp-search-pipeline
{
  "description": "Post processor for hybrid search",
  "phase_results_processors": [
    {
      "normalization-processor": {
        "normalization": {
          "technique": "min_max"
        },
        "combination": {
          "technique": "arithmetic_mean",
          "parameters": {
            "weights": [
              0.3,
              0.7
            ]
          }
        }
      }
    }
  ]
}

### 📘 Instalar Streamlit
pip install streamlit

### 📘 Instalar ragas
pip install ragas

### Ollama instalar modelo desde línea de comando on ollama
ollama pull llama3.2:1b

https://www.reddit.com/r/Rag/comments/1fa994u/evaluate_your_rag_pipeline_with_ragas_agnostic_of/?rdt=44452
https://github.com/AI-Commandos/RAGMeUp

Evaluating RAG using Llama 3
https://www.youtube.com/watch?v=Ts2wDG6OEko

https://github.com/mosh98/RAG_With_Models/blob/main/evaluation/RAGAS%20DEMO.ipynb
---

### Arrancar el modelo con OLlama
ollama run llama3.2:1b



### 📘 Referencias

**Streamlit** (https://streamlit.io/)
**OpenSearch** (https://opensearch.org/)

[**Build a Local LLM-based RAG System for Your Personal Documents - Part 1**](https://jamwithai.substack.com/p/build-a-local-llm-based-rag-system)
[**Build a Local LLM-based RAG System for Your Personal Documents - Part 2: The Guide**](https://jamwithai.substack.com/p/build-a-local-llm-based-rag-system-628)
---