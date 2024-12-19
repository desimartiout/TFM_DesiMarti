import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from config.ragas.ragas_config import RAGAS_FILE_PATH_RESULTS

# Cargar el CSV
df = pd.read_csv(RAGAS_FILE_PATH_RESULTS + '2024_12_19_18_30_47_ragas_results.csv', delimiter=';')

# Eliminar filas donde la columna 'response' sea "No tengo resultados"
df_filtered = df[df['response'] != 'No tengo resultados.']

# Comparar el número de filas antes y después
print(f"Filas originales: {len(df)}")
print(f"Filas después de la eliminación: {len(df_filtered)}")

df = df_filtered

# Ver las primeras filas para asegurarnos de que se cargó correctamente
print(df.head())

# Convertir las métricas a formato numérico (si es necesario)
metrics = ['faithfulness', 'semantic_similarity', 'answer_relevancy', 'context_precision']
df[metrics] = df[metrics].apply(pd.to_numeric, errors='coerce')

# Verificar que la conversión se haya realizado correctamente
print(df[metrics].describe())

# Análisis descriptivo
summary = df[metrics].describe()
print(summary)

# Crear un gráfico de bigotes para cada métrica
plt.figure(figsize=(12, 6))

for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 2, i)
    sns.boxplot(x=df[metric])
    plt.title(f'Boxplot de {metric}')

plt.tight_layout()
plt.show()

# Histograma de las métricas
plt.figure(figsize=(12, 6))

for i, metric in enumerate(metrics, 1):
    plt.subplot(2, 2, i)
    sns.histplot(df[metric], kde=True)
    plt.title(f'Histograma de {metric}')

plt.tight_layout()
plt.show()



# Diagrama de dispersión para ver la relación entre dos métricas
sns.pairplot(df[metrics])
plt.show()

# # Calcular la matriz de correlación
# correlation_matrix = df[metrics].corr()

# # Crear un mapa de calor
# plt.figure(figsize=(8, 6))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
# plt.title('Matriz de Correlación de las Métricas')
# plt.show()