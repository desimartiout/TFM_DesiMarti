# 📝 TFM Desiderio Martí Alcaraz - Grado en Ciencia de Datos (UOC - Universitat Oberta de Catalunya).

Bienvenido al Chatbot especializado en búsqueda de ayudas y subvenciones públicas del Gobierno de España basado en RAG con LLMs locales.

Puedes acceder a la web desplegada en HuggingFace Spaces en la ruta https://huggingface.co/spaces/DesiMarti/TFMCienciaDatos o bien puedes clonar el repositorio y ejecutarla en local

### 🌟 Características principales
- **Consultas bd vectoriales:** Uso de búsquedas vectoriales con Chromadb.
- **Scrapping** Puedes ejecutar comandos de scrapping de información de ayudas públicas.
- **LLM** Búsqueda de información en documentos mediante el uso de bases de datos vectoriales utilizando un LLM local con OLlama u OPENAI.
- **Evaluación del modelo** Puedes evaluar el modelo bien usando OLlama u OPENAI.

### 🚀 Como comenzar
1. Clonar el repositorio: `git clone https://github.com/desimartiout/TFM_DesiMarti.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar los ficheros de configuración que se encuentran en la carpeta `/config` el fichero principal es `global_config.py` (EMBEDDINGS, BD_VECTORIAL y LLM son los principales)
4. Ejecutar la aplicación Streamlit: `streamlit run Inicio.py`

## 📘 OLLAMA

### Ollama instalar modelo en local desde línea de comando on ollama
`ollama pull llama3.2:1b`

Si queremos hacer una copia del modelo para no trabajar directamente sobre el descargado lo podemos hacer así
`ollama cp llamaAyudas:latest`

### Arrancar el modelo con OLlama
`ollama run llamaAyudas:latest`

## 📘 OPENAI

Debes tener configurada la clave de entorno `OPENAI_API_KEY` o bien modificar el código para especificarla mediante este comando

`import openai`
`openai.api_key = TU_OPENAI_API_KEY`

# 📘 Web Chatbot
- Directorio de logs: `/logs/`
- Fichero de configuración: `src/constants.py`

### Instalar dependencias: 
Desde la ruta raiz del proyecto ejecutar el compando `pip install -r requirements.txt`

### Configuración


### Ejecutar la aplicación Streamlit

Desde la ruta raiz del proyecto ejecutar el comando `streamlit run Inicio.py`

# 📘 Web Scrapping de la web de ayudas
- Directorio: `/scrapping/`
- Directorio de logs: `/scrapping/logs/`
- Fichero de configuración: `/config/scrapping_config.py`

### Configuración
Aquí se especifican las rutas del API de la web de ayudas, los directorios de logs y donde se almacenan los documentos y la plantilla YAML para transformar el JSON resultado de la llamada a un formato más entendible

Se puede tambier especificar los parámetros para la llamada al API

`PAGE_SIZE:` Tamaño de resultados por página

`TOTAL_PAGES:` Número total de páginas a procesar

### Ejecución

`python.exe obtenerDatos.py`

# 📘 Scripts de utilidades

## Generar datasets de preguntas

Este fichero se genera mediante el script `python.exe generar_dataset_sintetico.py`

### Generar dataset sintético con preguntas prefijadas

Este fichero se genera mediante el script `python.exe generar_dataset_ragas.py`

### Generar dataset sintético con RAGAS

## Búsquedas desatendidas

### Ejecución de búsquedas desatendidas en base a un fichero de preguntas manual

`python.exe buscar_batch.py preguntas1.txt`

Nota: preguntas1.txt es un fichero de texto plano con una por cada una de las líneas (debe estar en el directorio `/ragas_eval/questions/`).

El proceso lo que hace es coger cada línea simular la búsqueda con el chat, obtener el resultado del LLM y almacenar los resultados en el dataset de evaluación de datos para posteriormente poder evaluar el sistema.

### Ejecución de búsquedas desatendidas en base a un fichero de evaluación csv generado a partir de RAGAS

`python.exe buscar_batch_ragas.py dataset_ragas_2024_12_21_13_43_20_ragas_results.csv`

Nota: preguntas1.txt es un fichero csv generado mediante el script `python.exe generar_dataset_ragas.py` comentado anteriormente.

# 📘  RAGAS - Evaluar el modelo

### Configuración
- Directorio: `/ragas_eval/`
- Directorio de logs: `/ragas_eval/logs/`
- Fichero de configuración: `/config/ragas_config.py`

Elegir el LLM a utilizar en la evaluación OPENAI / OLLAMA

`RAGAS_LLM_SELECCIONADO = RAGAS_LLM_TIPOMODELO_OPENAI / RAGAS_LLM_TIPOMODELO_OLLAMA`

Los nombres de los modelos deben estar especificados en estas constantes

`RAGAS_OPENAI_MODEL_NAME = "gpt-3.5-turbo"`

`RAGAS_OLLAMA_MODEL_NAME = "llamaAyudas:latest"`

### Ejecución

Desde la ruta raiz del proyecto ejecutar el comando

`python.exe evaluar.py 2024_12_14_ragas.json`

Nota: El fichero a evaluar debe estar en el directorio `/ragas_eval/datasets/`

Esto genera un fichero csv en el directorio `/ragas_eval/results/` con los resultados de la evaluación cuyo nombre contiene la fecha y hora de la evaluación, por ejemplo 2024_12_09_19_38_39_ragas_results.csv

El formato del fichero es este:

`"user_input";"retrieved_contexts";"response";"reference";"context_recall";"factual_correctness";"faithfulness";"semantic_similarity";"answer_relevancy";"context_precision"`

Campos con datos a evaluar 

`"user_input";"retrieved_contexts";"response";"reference"` 

Campos resultado de la evaluación

`"context_recall";"factual_correctness";"faithfulness";"semantic_similarity";"answer_relevancy";"context_precision"`

### 📘 URL Referencias 

**Web desplegada en HuggingFace Spaces** (https://huggingface.co/spaces/DesiMarti/TFMCienciaDatos)

**Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas** (https://www.pap.hacienda.gob.es/bdnstrans/)

**Hugging Face** https://huggingface.co/

**Streamlit** (https://streamlit.io/)

**RAGAS** (https://docs.ragas.io/)

**FAISS** (https://ai.meta.com/tools/faiss/)

**CHROMA DB** (https://www.trychroma.com/)

## Licencia

Este proyecto está licenciado bajo la **Licencia de Creative Commons Reconocimiento-NoComercial-SinObraDerivada 3.0 España**.

[![Licencia Creative Commons](https://i.creativecommons.org/l/by-nc-nd/3.0/es/88x31.png)](https://creativecommons.org/licenses/by-nc-nd/3.0/es/)

Para más detalles, consulta la licencia completa en [Creative Commons](https://creativecommons.org/licenses/by-nc-nd/3.0/es/).

