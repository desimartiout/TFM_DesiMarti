 #pip install neo4j


from neo4j import GraphDatabase

# Conexión con Neo4j a la base de datos llamada "ejemplo"
class Neo4jDatabase:

    def __init__(self, uri, user, password, database="ejemplo"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    # Función para crear la estructura del JSON en la base de datos
    def store_convocatoria(self, convocatoria):
        with self.driver.session(database=self.database) as session:
            session.write_transaction(self._create_convocatoria, convocatoria)

    # Función Cypher para almacenar la convocatoria en Neo4j
    @staticmethod
    def _create_convocatoria(tx, convocatoria):
        query = '''
        CREATE (c:Convocatoria {id: $id, sedeElectronica: $sedeElectronica, 
                                codigoBDNS: $codigoBDNS, presupuestoTotal: $presupuestoTotal, 
                                tipoConvocatoria: $tipoConvocatoria, 
                                descripcion: $descripcion, 
                                fechaInicioSolicitud: $fechaInicioSolicitud, 
                                fechaFinSolicitud: $fechaFinSolicitud})
        CREATE (o:Organo {nivel1: $nivel1, nivel2: $nivel2})
        CREATE (r:Region {descripcion: $regionDescripcion})
        CREATE (tb:Beneficiario {descripcion: $beneficiarioDescripcion})
        CREATE (c)-[:PERTENECE_A]->(o)
        CREATE (c)-[:AFECTA_REGION]->(r)
        CREATE (c)-[:DIRIGIDO_A]->(tb)
        '''
        tx.run(query,
               id=convocatoria["id"],
               sedeElectronica=convocatoria["sedeElectronica"],
               codigoBDNS=convocatoria["codigoBDNS"],
               presupuestoTotal=convocatoria["presupuestoTotal"],
               tipoConvocatoria=convocatoria["tipoConvocatoria"],
               descripcion=convocatoria["descripcion"],
               fechaInicioSolicitud=convocatoria["fechaInicioSolicitud"],
               fechaFinSolicitud=convocatoria["fechaFinSolicitud"],
               nivel1=convocatoria["organo"]["nivel1"],
               nivel2=convocatoria["organo"]["nivel2"],
               regionDescripcion=convocatoria["regiones"][0]["descripcion"],
               beneficiarioDescripcion=convocatoria["tiposBeneficiarios"][0]["descripcion"])

    # Función para consultar los datos de una convocatoria
    def query_convocatoria(self, convocatoria_id):
        with self.driver.session(database=self.database) as session:
            result = session.read_transaction(self._get_convocatoria, convocatoria_id)
            return result

    # Consulta Cypher para obtener los datos de la convocatoria
    @staticmethod
    def _get_convocatoria(tx, id):
        query = '''
        MATCH (c:Convocatoria {id: $id})-[:PERTENECE_A]->(o:Organo), 
              (c)-[:AFECTA_REGION]->(r:Region), 
              (c)-[:DIRIGIDO_A]->(tb:Beneficiario)
        RETURN c, o, r, tb
        '''
        result = tx.run(query, id=id)
        return result.data()

# Función para transformar el resultado de la consulta a formato JSON
def format_as_json(result):
    convocatoria = result[0]['c']
    organo = result[0]['o']
    region = result[0]['r']
    beneficiario = result[0]['tb']

    return {
        "id": convocatoria["id"],
        "organo": {
            "nivel1": organo["nivel1"],
            "nivel2": organo["nivel2"]
        },
        "sedeElectronica": convocatoria["sedeElectronica"],
        "presupuestoTotal": convocatoria["presupuestoTotal"],
        "tipoConvocatoria": convocatoria["tipoConvocatoria"],
        "descripcion": convocatoria["descripcion"],
        "fechaInicioSolicitud": convocatoria["fechaInicioSolicitud"],
        "fechaFinSolicitud": convocatoria["fechaFinSolicitud"],
        "regiones": [{"descripcion": region["descripcion"]}],
        "tiposBeneficiarios": [{"descripcion": beneficiario["descripcion"]}]
    }

# Ejemplo de JSON a almacenar
convocatoria_json = {
    "id": 992327,
    "organo": {
        "nivel1": "GANDIA",
        "nivel2": "AYUNTAMIENTO DE GANDIA"
    },
    "sedeElectronica": "https://gandia.sedelectronica.es/",
    "codigoBDNS": "790767",
    "presupuestoTotal": 100000,
    "tipoConvocatoria": "Concurrencia competitiva - canónica",
    "descripcion": "2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas...",
    "fechaInicioSolicitud": "2024-10-31T00:00:00+01:00",
    "fechaFinSolicitud": "2024-11-15T00:00:00+01:00",
    "regiones": [
        {"descripcion": "ES52 - COMUNIDAD VALENCIANA"}
    ],
    "tiposBeneficiarios": [
        {"descripcion": "PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}
    ]
}

# Main - Insertar y consultar los datos
if __name__ == "__main__":
    # Conectar con la base de datos "ejemplo" en Neo4j
    db = Neo4jDatabase(uri="bolt://localhost:7687", user="neo4j", password="12345678", database="")

    # Almacenar el JSON en la base de datos
    db.store_convocatoria(convocatoria_json)

    # Consultar la convocatoria y formatearla a JSON
    result = db.query_convocatoria(992327)
    json_data = format_as_json(result)
    
    print("Datos en formato JSON:")
    print(json_data)

    # Cerrar conexión
    db.close()
