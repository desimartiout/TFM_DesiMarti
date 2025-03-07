from itertools import product

from config.ragas.ragas_config import  RAGAS_FILE_PATH_QUESTIONS
from ragas_eval.utils import nombre_fichero_sintetico_questions

# Listas base para generar las preguntas
regiones = ["Murcia", "Cataluña", "Madrid", "Valencia", "Barcelona", "San Juan de Alicante", "Castellón", "Paiporta"]
sectores = ["Agricultura", "ganadería", "Industria", "tecnológica", "Salud", "bienestar","Educación", "formación", "Construcción", "vivienda", "Energías renovables", "Transporte", "logística", "Industria manufacturera","Turismo", "hostelería","Arte", "cultura","Comercio", "distribución","Sector financiero","Servicios sociales","Innovación", "desarrollo","Medio ambiente", "sostenibilidad","Pesca", "acuicultura","Automoción", "movilidad sostenible","Ciencias", "tecnología espacial","Industria alimentaria","Telecomunicaciones", "medios digitales"]
tipos_beneficiarios = [
    "PYME",
    "Autónomos",
    "Personas físicas",
    "Grandes empresas",
    "Startups",
    "Asociaciones sin ánimo de lucro",
    "Entidades públicas",
    "Comunidades de vecinos",
    "Agricultores y ganaderos",
    "Cooperativas",
    "Fundaciones",
    "Estudiantes",
    "Investigadores",
    "Emprendedores",
    "Personas en situación de vulnerabilidad",
    "ONGs",
    "Administraciones locales",
    "Centros educativos",
    "Pequeñas y medianas empresas del sector tecnológico",
    "Personas mayores o jubilados"
]

organismos_emisores = [
    "Diputación de Alicante",
    "Ayuntamiento de Barcelona",
    "Gobierno de Andalucía",
    "Consejería de Educación de Madrid",
    "Ministerio de Industria, Comercio y Turismo",
    "Diputación de Valencia",
    "Ayuntamiento de Sevilla",
    "Junta de Extremadura",
    "Gobierno de Canarias",
    "Gobierno de Castilla y León",
    "Diputación de Málaga",
    "Consejería de Sanidad de Galicia",
    "Ayuntamiento de Bilbao",
    "Gobierno Vasco",
    "Consejo Insular de Mallorca",
    "Gobierno de Aragón",
    "Cabildo de Tenerife",
    "Consejería de Agricultura de La Rioja",
    "Ministerio para la Transición Ecológica y el Reto Demográfico",
    "Consejería de Fomento de Castilla-La Mancha"
]
palabras_clave = ["mejora de viviendas", "eficiencia energética", "innovación empresarial", "DANA"]

# Plantillas para cada tipo de pregunta
plantillas = {
    "región": "¿Qué ayudas hay disponibles en {item}?",
    "sector": "¿Hay subvenciones para el sector {item}?",
    "tipo_beneficiario": "¿Existen ayudas para {item} en alguna región?",
    "organismo": "¿Qué ayudas hay de {item}?",
    "palabras_clave": "Busco subvenciones para {item}."
}

# Generación de preguntas por categoría
preguntas = []

for region in regiones:
    preguntas.append(plantillas["región"].format(item=region))

for sector in sectores:
    preguntas.append(plantillas["sector"].format(item=sector))

for tipo in tipos_beneficiarios:
    preguntas.append(plantillas["tipo_beneficiario"].format(item=tipo))

for organismo in organismos_emisores:
    preguntas.append(plantillas["organismo"].format(item=organismo))

for palabra in palabras_clave:
    preguntas.append(plantillas["palabras_clave"].format(item=palabra))


ruta_fichero = nombre_fichero_sintetico_questions()
# Guardar las preguntas en un archivo TXT
with open(ruta_fichero, "w", encoding="utf-8") as file:
    file.write("\n".join(preguntas))

print(f"Archivo {ruta_fichero} generado con éxito.")