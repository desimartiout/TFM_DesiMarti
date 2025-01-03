from datetime import datetime
from itertools import product
import json
import pandas as pd
from config.faiss.faiss_config import METADATA_FILE_FAISS
from config.global_config import OPENAI_MODEL_NAME, RAGAS_FILE_PATH_QUESTIONS
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from ragas.testset import TestsetGenerator
from langchain_community.document_loaders import DataFrameLoader
from ragas.testset.transforms.extractors.llm_based import NERExtractor
from ragas.testset.transforms.splitters import HeadlineSplitter
from ragas.run_config import RunConfig
from ragas.testset.persona import Persona

# Tu cadena JSON
# data = {"0": "\nDetalle de la convocatoria de ayuda o  subvenci\u00f3n: 804000\nEnlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/804000\n\u00d3rgano, comunidad, autonom\u00eda, provincia o ayuntamiento convocante: DONOSTIA/SAN SEBASTI\u00c1N - AYUNTAMIENTO DE DONOSTIA/SAN SEBASTI\u00c1N\nFecha de recepci\u00f3n: 2024-12-18T15:35:54+01:00\nTipo de ayuda: SUBVENCI\u00d3N Y ENTREGA DINERARIA SIN CONTRAPRESTACI\u00d3N \nTipo de convocatoria: Concesi\u00f3n directa - can\u00f3nica\nPresupuesto total: 357000 Euros\nDescripci\u00f3n: Acuerdo de la Junta de Gobierno Local de fecha 3 de diciembre de 2024, por el que se aprueba la convocatoria y bases reguladoras de ayudas econ\u00f3micas para el acceso de personas sin hogar a centros hosteleros y selecci\u00f3n de dichos centros hosteleros.\nTipos de beneficiarios: PERSONAS F\u00cdSICAS QUE NO DESARROLLAN ACTIVIDAD ECON\u00d3MICA, PYME Y PERSONAS F\u00cdSICAS QUE DESARROLLAN ACTIVIDAD ECON\u00d3MICA\nSectores involucrados: ACTIVIDADES SANITARIAS Y DE SERVICIOS SOCIALES\nRegi\u00f3n de impacto: ES212 - Gipuzkoa\nFinalidad: Servicios Sociales y Promoci\u00f3n Social\nBases reguladoras: Convocatoria y bases reguladoras de ayudas econ\u00f3micas para el acceso de personas sin hogar a centros hosteleros y selecci\u00f3n de dichos centros hosteleros.\nPublicaci\u00f3n en diario oficial: S\u00ed\nEstado de convocatoria abierta: No\nInicio de convocatoria: Desde el d\u00eda siguiente al de la publicaci\u00f3n del extracto en el BOG\nFin de convocatoria: \n", "1": "\nDetalle de la convocatoria de ayuda o  subvenci\u00f3n: 803990\nEnlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/803990\n\u00d3rgano, comunidad, autonom\u00eda, provincia o ayuntamiento convocante: DONOSTIA/SAN SEBASTI\u00c1N - AYUNTAMIENTO DE DONOSTIA/SAN SEBASTI\u00c1N\nFecha de recepci\u00f3n: 2024-12-18T15:02:10+01:00\nTipo de ayuda: SUBVENCI\u00d3N Y ENTREGA DINERARIA SIN CONTRAPRESTACI\u00d3N \nTipo de convocatoria: Concesi\u00f3n directa - can\u00f3nica\nPresupuesto total: 850000 Euros\nDescripci\u00f3n: Acuerdo de la Junta de Gobierno Local de fecha 3 de diciembre de 2024, por el que se aprueba la convocatoria y bases reguladoras de ayudas de apoyo al Plan de Trabajo Compartido para el a\u00f1o 2025.\nTipos de beneficiarios: PERSONAS F\u00cdSICAS QUE NO DESARROLLAN ACTIVIDAD ECON\u00d3MICA\nSectores involucrados: ACTIVIDADES SANITARIAS Y DE SERVICIOS SOCIALES\nRegi\u00f3n de impacto: ES212 - Gipuzkoa\nFinalidad: Servicios Sociales y Promoci\u00f3n Social\nBases reguladoras: Convocatoria y bases reguladoras de ayudas de apoyo al Plan de Trabajo Compartido para el a\u00f1o 2025\nPublicaci\u00f3n en diario oficial: S\u00ed\nEstado de convocatoria abierta: No\nInicio de convocatoria: Desde el d\u00eda siguiente al de la publicaci\u00f3n del extracto en el BOG\nFin de convocatoria: \n", "2": "\nDetalle de la convocatoria de ayuda o  subvenci\u00f3n: 803988\nEnlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/803988\n\u00d3rgano, comunidad, autonom\u00eda, provincia o ayuntamiento convocante: BIGASTRO - AYUNTAMIENTO DE BIGASTRO\nFecha de recepci\u00f3n: 2024-12-18T14:55:11+01:00\nTipo de ayuda: SUBVENCI\u00d3N Y ENTREGA DINERARIA SIN CONTRAPRESTACI\u00d3N \nTipo de convocatoria: Concurrencia competitiva - can\u00f3nica\nPresupuesto total: 10000 Euros\nDescripci\u00f3n: Convocatoria y Bases Ayudas al Estudio Universitario 2024/2025 del Ayuntamiento de Bigastro\nTipos de beneficiarios: PERSONAS F\u00cdSICAS QUE NO DESARROLLAN ACTIVIDAD ECON\u00d3MICA\nSectores involucrados: EDUCACI\u00d3N\nRegi\u00f3n de impacto: ES521 - Alicante / Alacant\nFinalidad: Educaci\u00f3n\nBases reguladoras: Convocatoria y Bases Ayudas al Estudio Universitario 2024/2025 del Ayuntamiento de Bigastro\nPublicaci\u00f3n en diario oficial: S\u00ed\nEstado de convocatoria abierta: No\nInicio de convocatoria: aproximadamente\nFin de convocatoria: finaliza\n", "3": "\nDetalle de la convocatoria de ayuda o  subvenci\u00f3n: 803987\nEnlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/803987\n\u00d3rgano, comunidad, autonom\u00eda, provincia o ayuntamiento convocante: ARCHIDONA - AYUNTAMIENTO DE ARCHIDONA\nFecha de recepci\u00f3n: 2024-12-18T14:48:55+01:00\nTipo de ayuda: SUBVENCI\u00d3N Y ENTREGA DINERARIA SIN CONTRAPRESTACI\u00d3N \nTipo de convocatoria: Concurrencia competitiva - can\u00f3nica\nPresupuesto total: 600 Euros\nDescripci\u00f3n: Resoluci\u00f3n_de Alcald\u00eda_n\u00fam 2024-1614 de 18 de diciembre. Aprobar Bases Reguladoras y efectuar Convocatoria Concurso Cartel Anunciador Carnaval 2025. Archidona\nTipos de beneficiarios: PERSONAS F\u00cdSICAS QUE NO DESARROLLAN ACTIVIDAD ECON\u00d3MICA\nSectores involucrados: Actividades de creaci\u00f3n, art\u00edsticas y espect\u00e1culos\nRegi\u00f3n de impacto: ES617 - M\u00e1laga\nFinalidad: Cultura\nBases reguladoras: Resoluci\u00f3n_de Alcald\u00eda_n\u00fam 2024-1614 de 18 de diciembre. Aprobar Bases Reguladoras y efectuar Convocatoria Concurso Cartel Anunciador Carnaval 2025. Archidona\nPublicaci\u00f3n en diario oficial: S\u00ed\nEstado de convocatoria abierta: No\nInicio de convocatoria: Desde el d\u00eda siguiente a la publicaci\u00f3n del extracto de la convocatoria en el BOPMA\nFin de convocatoria: \n"}

import asyncio

from config.ragas.ragas_config import RAGAS_DATASET_EVAL_SIZE
from ragas_eval.utils import nombre_fichero_ragas_questions

async def generar_dataset_ragas(data):
    # Convertir en DataFrame
    df = pd.DataFrame(list(data.items()), columns=["id", "content"])
    print(df)

    # Crear el loader con las columnas que necesitas
    loader = DataFrameLoader(df, page_content_column="content")
    docs = loader.load()

    personas = [
        Persona(
            name="persona normal",
            role_description="Una persona que busca ayudas y subvenciones del gobierno de España",
        ),
    ]

    generator_llm = LangchainLLMWrapper(ChatOpenAI(model=OPENAI_MODEL_NAME))
    generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())   #model=OPENAI_MODEL_NAME

    from ragas.testset.synthesizers.single_hop.specific import (
        SingleHopSpecificQuerySynthesizer,
    )

    distribution = [
        (SingleHopSpecificQuerySynthesizer(llm=generator_llm), 1.0),
    ]

    # Lo configuramos para que prepare las preguntas en español
    for query, _ in distribution:
        prompts = await query.adapt_prompts("spanish", llm=generator_llm)
        query.set_prompts(**prompts)

    generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings,persona_list=personas)
    # dataset = generator.generate_with_langchain_docs(docs, testset_size=10,)

    transforms = [HeadlineSplitter(), NERExtractor()]
    dataset = generator.generate_with_langchain_docs(
        docs[:],
        testset_size=RAGAS_DATASET_EVAL_SIZE,
        transforms=transforms,
        query_distribution=distribution,
    )

    df = dataset.to_pandas()

    ruta_fichero = nombre_fichero_ragas_questions()

    #Guardamos el dataset
    df.to_csv(ruta_fichero, index=False, quoting=1, quotechar='"', sep=";") 

async def mi_funcion_asincrona():
    #Cargamos la bdvectorial con todas las ayudas
    fichero = METADATA_FILE_FAISS
    try:
        with open(fichero, "r", encoding="utf-8") as file:
            data = json.load(file)

            #Generamos el dataset de evaluación a partir de los datos almacenados.
            await generar_dataset_ragas(data)

    except FileNotFoundError:
        print(f"Error: El archivo '{fichero}' no existe.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

    
async def main():
    resultado = await mi_funcion_asincrona()

asyncio.run(main())