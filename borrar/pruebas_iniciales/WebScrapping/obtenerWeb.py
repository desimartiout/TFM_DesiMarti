#pip install requests beautifulsoup4 transformers faiss-cpu

#Instalar torch con soporte CUDA
#pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModel
import torch
import faiss
#pip install lxml requests
from lxml import html
import requests

# 1. Web Scraping para obtener datos
def scrape_website(url):
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Aquí podemos ajustar según la estructura HTML de la página
        #paragraphs = soup.find_all('p')
        #text = " ".join([p.get_text() for p in paragraphs])

        text = print(response.content)

        # Parsear el contenido HTML
        tree = html.fromstring(response.content)

        ## Usar XPath para seleccionar el elemento (enlace 'a')
        #element = tree.xpath('/html/body/app-root/main/app-convocatoria/div[1]/mat-accordion/mat-expansion-panel/div/div/div/div[1]/div[2]/div[2]/a')

        ## Verificar si se encontró el elemento y luego imprimir su texto o atributo href
        #if element:
        #    print("Texto del enlace:", element[0].text_content())  # Texto del enlace
        #    print("URL del enlace:", element[0].get('href'))       # URL del enlace
        #else:
        #    print("Elemento no encontrado")

        return text
    else:
        return None

# 2. Convertir el texto en embeddings usando un modelo de lenguaje
def get_embeddings(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    return embeddings

# 3. Almacenar los embeddings en una base de datos vectorial (FAISS)
def store_in_faiss(embeddings_list):
    d = embeddings_list[0].shape[0]  # Dimensión de los vectores
    index = faiss.IndexFlatL2(d)     # Usamos L2 (distancia euclidiana)
    index.add(np.array(embeddings_list))  # Añadir los embeddings al índice
    return index

# 4. Ejemplo completo
if __name__ == "__main__":
    #url = "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/790767"  # URL de la web que quieres scrapear
    url = "https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias?numConv=790767&vpd=GE"  # URL de la web que quieres scrapear
    
    text = scrape_website(url)
    
    #if text:
    #    # Cargar el modelo de lenguaje y tokenizer
    #    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    #    model = AutoModel.from_pretrained("bert-base-uncased")
    #    
    #    # Obtener el embedding del texto
    #    embeddings = get_embeddings(text, tokenizer, model)
    #    
    #    # Crear una lista de embeddings (en un caso real, scrapeamos más de una página)
    #    embeddings_list = [embeddings]  # Aquí sería una lista de varios embeddings

    #    # Almacenar los embeddings en FAISS
    #    index = store_in_faiss(embeddings_list)
        
    #    print("Embeddings almacenados en FAISS.")
    #else:
    #    print("No se pudo obtener contenido de la página.")


##Comprobar lo almacenado en la base de datos vectorial
#def search_in_faiss(index, query_embedding, k=5):
#    D, I = index.search(np.array([query_embedding]), k)  # Buscar los k vectores más cercanos
#    return I, D

## Ejemplo de búsqueda
#query = "Concurrencia competitiva"
#query_embedding = get_embeddings(query, tokenizer, model)
#result_ids, distances = search_in_faiss(index, query_embedding)
#print(f"Resultados más cercanos: {result_ids}")

