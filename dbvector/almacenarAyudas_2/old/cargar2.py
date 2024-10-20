#pip install -r requirements.txt

from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

from langchain.text_splitter import RecursiveCharacterTextSplitter

import os

#os.environ["OPENAI_API_KEY"] = "..."

def get_vector_store():
   persistent_index_path = "./db/vectorestore/"

   if os.path.exists( persistent_index_path ): 
      vectorstore = VectorstoreIndexCreator()
      vectorstore = vectorstore.vectorstore_cls(
         persist_directory=persistent_index_path, 
         embedding_function=vectorstore.embedding
      )

      return VectorStoreIndexWrapper(vectorstore=vectorstore)

   dbdata = """
Disponemos de estos datos de vehículos:

[
{ "color": "rojo", "ruedas": 3, "tipo": "terrestre" },
{ "color": "amarillo", "ruedas": 2, "tipo": "terrestre" },
{ "color": "verde", "ruedas": 3, "tipo": "terrestre" },
{ "color": "blanco", "ruedas": 0, "tipo": "acuatico" },
{ "color": "blanco", "ruedas": 0, "tipo": "terrestre" }
]
   """
       
   char_text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0) 
   docs = char_text_splitter.create_documents( [ dbdata ] )

   os.makedirs( persistent_index_path, exist_ok=True )
   index = VectorstoreIndexCreator( vectorstore_kwargs={"persist_directory": persistent_index_path} ).from_documents( docs )
   index.vectorstore.persist()

   return index

index = get_vector_store()

result = index.query( "De que color es el vehículo con 3 ruedas y de tipo terreste?" )
print( "\n-----------------------------------\n" )
print( result )

result = index.query( "De que colores son los vehículos terrestres?" )
print( "\n-----------------------------------\n" )
print( result )

result = index.query( "De que colores son los vehículos acuaticos?" )
print( "\n-----------------------------------\n" )
print( result )

result = index.query( "Quantos vehículos terrestres hay?" )
print( "\n-----------------------------------\n" )
print( result )