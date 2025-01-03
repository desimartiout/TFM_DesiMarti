import argparse
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from config.ragas.ragas_config import RAGAS_FILE_PATH_RESULTS
from ragas_eval.utils import setup_logging_ragas


def main():

    setup_logging_ragas()

    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(description="Script para mostrar los resultados de evaluación de RAGAS.")
    parser.add_argument(
        "filename", 
        type=str, 
        help="Nombre del archivo CSV con los resultados de la evaluación con RAGAS (debe estar en el directorio /ragas_eval/results)"
    )

    # Parsear los argumentos
    args = parser.parse_args()
    fichero = RAGAS_FILE_PATH_RESULTS + args.filename

    print(fichero)
     # Intentar abrir el archivo CSV con diferentes encodings
    try:
        # Cargar el CSV
        df = pd.read_csv(fichero, delimiter=';',quotechar='"')

        # Eliminar filas donde la columna 'response' sea "No tengo resultados"
        df_filtered = df[df['response'] != 'No tengo resultados.']

        # Comparar el número de filas antes y después
        print(f"Filas originales: {len(df)}")
        print(f"Filas después de la eliminación: {len(df_filtered)}")

        df = df_filtered

        # Ver las primeras filas para asegurarnos de que se cargó correctamente
        print(df.head())

        # Convertir las métricas a formato numérico (si es necesario)
        # "context_recall";"factual_correctness"
        # metrics = ['faithfulness', 'semantic_similarity', 'answer_relevancy', 'context_precision']
        metrics = ['context_recall','factual_correctness','faithfulness', 'semantic_similarity', 'answer_relevancy', 'context_precision']
        df[metrics] = df[metrics].apply(pd.to_numeric, errors='coerce')

        # Verificar que la conversión se haya realizado correctamente
        print(df[metrics].describe())

        # Análisis descriptivo
        summary = df[metrics].describe()
        print(summary)

        # Crear un gráfico de bigotes para cada métrica
        plt.figure(figsize=(12, 6))

        for i, metric in enumerate(metrics, 1):
            plt.subplot(3, 2, i)
            sns.boxplot(x=df[metric])
            plt.title(f'Boxplot de {metric}')

        plt.tight_layout()
        plt.show()

        # Histograma de las métricas
        plt.figure(figsize=(12, 6))

        for i, metric in enumerate(metrics, 1):
            plt.subplot(3, 2, i)
            sns.histplot(df[metric], kde=True)
            plt.title(f'Histograma de {metric}')

        plt.tight_layout()
        plt.show()
        
    except FileNotFoundError:
        print(f"Error: El archivo '{fichero}' no existe.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

if __name__ == "__main__":
    main()