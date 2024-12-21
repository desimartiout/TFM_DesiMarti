
# Directorio donde se encuentran los archivos JSON
import os
from config.global_config import RAGAS_FILE_PATH


json_directory = RAGAS_FILE_PATH  # Cambia esto por el path de tu directorio


# Filtrar archivos JSON mayores a 8 bytes
json_files = [
    f for f in os.listdir(json_directory)
    if f.endswith('.json') and os.path.getsize(os.path.join(json_directory, f)) > 10
]

print(json_files)