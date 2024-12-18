
import argparse
from ragas_eval.utils import setup_logging_ragas
from libs.chat import buscar_cadena
from config.global_config import OLLAMA_TEMPERATURE, CHROMA_NUMDOCUMENTS, RAGAS_FILE_PATH_QUESTIONS

def hacer_consulta(prompt: str) -> str:
    return buscar_cadena(prompt,num_results=CHROMA_NUMDOCUMENTS,temperature=OLLAMA_TEMPERATURE,chat_history=[])

def main():
    # Ejemplos de llamadas
    # hacer_consulta("¿Qué ayudas hay en Murcia?")
    # hacer_consulta("¿Qué ayudas hay en Barcelona?")

    setup_logging_ragas()

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Script para busquedas masivas desatendidas.")
    parser.add_argument(
        "filename", 
        type=str, 
        help="Nombre del archivo de texto con las preguntas (debe estar en el directorio /ragas_eval/questions)"
    )

    # Parsear los argumentos
    args = parser.parse_args()
    fichero = RAGAS_FILE_PATH_QUESTIONS + args.filename

    try:
        # Leer el archivo línea a línea
        with open(fichero, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                print(f"Línea {line_number}: {line.strip()}")
                hacer_consulta(line.strip())

    except FileNotFoundError:
        print(f"Error: El archivo '{fichero}' no existe.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == "__main__":
    main()