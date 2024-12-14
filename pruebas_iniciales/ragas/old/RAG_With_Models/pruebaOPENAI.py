#1. Prepare Dataset
from datasets import Dataset, DatasetDict
import pandas as pd
import json
from ragas import evaluate
from ragas.metrics import Faithfulness


from ragas.run_config import RunConfig

# increasing max_workers to 64 and timeout to 60 seconds

my_run_config = RunConfig(max_workers=64, timeout=120)

# Leer el JSON desde un archivo local
with open("c:/Users/desim/Documents/GitHub/TFM_DesiMarti/pruebas_iniciales/ragas/RAG_With_Models/data/eval.json", "r") as file:
    data = json.load(file)

# Crear un DatasetDict para simular la estructura de Hugging Face
amnesty_qa = DatasetDict({
    "eval": Dataset.from_list(data)  # Puedes cambiar "eval" por el nombre adecuado
})

# Seleccionar un subconjunto de los datos
amnesty_subset = amnesty_qa["eval"].select(range(1))

# Convertir el Dataset completo a un DataFrame de Pandas
amnesty_df = amnesty_qa["eval"].to_pandas()

# Mostrar resultados
print(amnesty_subset)
print(amnesty_df)

metric = Faithfulness()

result = evaluate(
    dataset=amnesty_subset,
    metrics=[metric],
    run_config=my_run_config,
)

print(result)