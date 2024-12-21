
import argparse

import pandas as pd
from libs.utils import limpia_cadena
from ragas_eval.utils import setup_logging_ragas
from libs.chat import buscar_cadena
from config.global_config import OLLAMA_TEMPERATURE, CHROMA_NUMDOCUMENTS, RAGAS_FILE_PATH_QUESTIONS

def hacer_consulta(prompt: str,reference: str) -> str:
    return buscar_cadena(prompt,reference,num_results=CHROMA_NUMDOCUMENTS,temperature=OLLAMA_TEMPERATURE,chat_history=[])

def main():
    # Ejemplos de llamadas
    # hacer_consulta("¿Qué ayudas hay en Murcia?")
    # hacer_consulta("¿Qué ayudas hay en Barcelona?")

    setup_logging_ragas()

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Script para busquedas masivas desatendidas basadas en datasets de RAGAS.")
    parser.add_argument(
        "filename", 
        type=str, 
        help="Nombre del archivo CSV con las preguntas generadas por RAGAS previamente (debe estar en el directorio /ragas_eval/questions)"
    )

    # Parsear los argumentos
    args = parser.parse_args()
    fichero = RAGAS_FILE_PATH_QUESTIONS + args.filename

    print(fichero)
     # Intentar abrir el archivo CSV con diferentes encodings
    try:
        # Intentamos con utf-8
        df = pd.read_csv(fichero, delimiter=";",quotechar='"', encoding="utf-8")
        for index, row in df.iterrows():
            user_input = row['user_input']
            # reference_contexts = row['reference_contexts']
            reference = row['reference']
            # print(f"{user_input} - {reference}")

            hacer_consulta(limpia_cadena(user_input),reference)
            # print("------")
        
    except FileNotFoundError:
        print(f"Error: El archivo '{fichero}' no existe.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == "__main__":
    main()