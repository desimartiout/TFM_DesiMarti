from collections import defaultdict

# JSON completo
""" data = {
    "id": 997270,
    "organo": {
        "nivel1": "ARAGÓN",
        "nivel2": "FUNDACIÓN ARAGÓN EMPRENDE",
        "nivel3": None
    },
    "sedeElectronica": "www.aragonemprende.com",
    "codigoBDNS": "795710",
    "fechaRecepcion": "2024-11-08T12:32:00+01:00",
    "instrumentos": [
        {"descripcion": "SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}
    ],
    "tipoConvocatoria": "Concurrencia competitiva - canónica",
    "presupuestoTotal": 750000,
    "mrr": False,
    "descripcion": "Ayudas al impulso de iniciativas de desarrollo empresarial en el medio rural de Aragón.",
    "descripcionLeng": None,
    "tiposBeneficiarios": [
        {"descripcion": "PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA"}
    ],
    "sectores": [
        {"descripcion": "ACTIVIDADES ADMINISTRATIVAS Y SERVICIOS AUXILIARES", "codigo": "N"},
        {"descripcion": "ACTIVIDADES PROFESIONALES, CIENTÍFICAS Y TÉCNICAS", "codigo": "M"},
        {"descripcion": "HOSTELERÍA", "codigo": "I"},
        {"descripcion": "INDUSTRIA MANUFACTURERA", "codigo": "C"}
    ],
    "regiones": [{"descripcion": "ES24 - ARAGON"}],
    "descripcionFinalidad": "Otras actuaciones de carácter económico",
    "descripcionBasesReguladoras": "Aprobación de las bases reguladoras para la concesión de ayudas al impulso de iniciativas de desarrollo empresarial en el medio rural de Aragón y su convocatoria.",
    "urlBasesReguladoras": "pendiente de publicación",
    "sePublicaDiarioOficial": True,
    "abierto": False,
    "fechaInicioSolicitud": None,
    "fechaFinSolicitud": None,
    "textInicio": "Día siguiente a la publicación ",
    "textFin": "Diez días desde la publicación ",
    "ayudaEstado": None,
    "urlAyudaEstado": None,
    "fondos": [],
    "reglamento": {"descripcion": "REG (UE) 2023/2831 de minimis, General", "orden": None},
    "objetivos": [],
    "sectoresProductos": [],
    "documentos": [
        {
            "id": 1156285,
            "descripcion": "Documento de la convocatoria en español",
            "nombreFic": "CSV3P0E2Q50FE1E0XFIL BASES REGULADORAS Y CONVOCATORIA AYUDAS EMPRESA MEDIO RURAL CON CARGO AL FCT 24.pdf",
            "long": 1722365,
            "datMod": "2024-11-08T13:15:13.000+01:00",
            "datPublicacion": "2024-11-08T13:25:22.000+01:00",
        }
    ],
    "anuncios": [],
    "advertencia": "La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción.",
} """


data = { "id":992327,"organo":{"nivel1":"GANDIA","nivel2":"AYUNTAMIENTO DE GANDIA","nivel3":None},"sedeElectronica":"https://gandia.sedelectronica.es/","codigoBDNS":"790767","fechaRecepcion":"2024-10-14T15:57:09+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":100000,"mrr":False,"descripcion":"2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","descripcionLeng":None,"tiposBeneficiarios":[{"descripcion":"PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"OTROS SERVICIOS","codigo":"S"}],"regiones":[{"descripcion":"ES52 - COMUNIDAD VALENCIANA"}],"descripcionFinalidad":"Acceso a la vivienda y fomento de la edificación","descripcionBasesReguladoras":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","urlBasesReguladoras":"www.bop.es","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"2024-10-31T00:00:00+01:00","fechaFinSolicitud":"2024-11-15T00:00:00+01:00","textInicio":None,"textFin":None,"ayudaEstado":None,"urlAyudaEstado":None,"fondos":[],"reglamento":None,"objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144216,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241011_Certificat_punt 4 Aprobación convocatoria ayuda alquiler residencia habitual, facilitar acceso a la vivienda. Exp. 35295-2024.pdf","long":344807,"datMod":"2024-10-14T18:15:02.000+02:00","datPublicacion":"2024-10-14T18:15:02.000+02:00"}],"anuncios":[{"numAnuncio":168388,"titulo":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","tituloLeng":None,"texto":"<p>Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda, constituyendoe el objeto de las bases la regulación del Régimen Jurídico, solicitud, tramitación y concesión de ayudas consistentes en la financiación por parte del Ayuntamiento de Gandia de a) el seguro de impago de la renta del alquiler b) el seguro por daños ocasionados al continente y/o contenido de la vivienda y c) gastos por mejoras en la vivienda para su puesta a punto para el alquiler.</p>","textoLeng":None,"url":"https://bop.dival.es/bop/downloads?anuncioCSV=BOPV-2024/14394&lang=es","cve":"BOPV-2024/14394","desDiarioOficial":"B.O.P. DE VALENCIA","datPublicacion":"2024-10-24T00:00:00.000+02:00"}],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."}

# Plantilla del texto
template = """
Código de ayuda o  subvención: {id}
Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/{id}
Órgano convocante: {organo_nivel1} - {organo_nivel2}
Enlace a sede electrónica: {sedeElectronica}
Código BDNS: {codigoBDNS}
Fecha de recepción: {fechaRecepcion}
Instrumentos: {instrumentos}
Tipo de convocatoria: {tipoConvocatoria}
Presupuesto total: {presupuestoTotal}
Descripción: {descripcion}
Tipos de beneficiarios: {tiposBeneficiarios}
Sectores involucrados: {sectores}
Regiones: {regiones}
Finalidad: {descripcionFinalidad}
Bases reguladoras: {descripcionBasesReguladoras}
URL Bases Reguladoras: {urlBasesReguladoras}
Publicación en diario oficial: {sePublicaDiarioOficial}
Estado de convocatoria abierta: {abierto}
Fecha de inicio de solicitudes: {fechaInicioSolicitud}
Fecha de fin de solicitudes: {fechaFinSolicitud}
Inicio de texto: {textInicio}
Fin de texto: {textFin}
Reglamento: {reglamento}
Documentos: {documentos}
"""

# Función para convertir `None` en vacío
def safe_value(value):
    if value is None:
        return ""
    elif isinstance(value, bool):
        return "Sí" if value else "No"
    return value

# Función para aplanar y procesar el JSON
def safe_format(data, template):
    flat_data = defaultdict(
        str,  # Devuelve cadena vacía si falta alguna clave
        {
            "id": safe_value(data.get("id")),
            "organo_nivel1": safe_value(data.get("organo", {}).get("nivel1")),
            "organo_nivel2": safe_value(data.get("organo", {}).get("nivel2")),
            "sedeElectronica": safe_value(data.get("sedeElectronica")),
            "codigoBDNS": safe_value(data.get("codigoBDNS")),
            "fechaRecepcion": safe_value(data.get("fechaRecepcion")),
            "instrumentos": ", ".join(
                safe_value(i.get("descripcion")) for i in data.get("instrumentos", [])
            ),
            "tipoConvocatoria": safe_value(data.get("tipoConvocatoria")),
            "presupuestoTotal": safe_value(data.get("presupuestoTotal")),
            "descripcion": safe_value(data.get("descripcion")),
            "tiposBeneficiarios": ", ".join(
                safe_value(t.get("descripcion"))
                for t in data.get("tiposBeneficiarios", [])
            ),
            "sectores": ", ".join(
                safe_value(s.get("descripcion")) for s in data.get("sectores", [])
            ),
            "regiones": ", ".join(
                safe_value(r.get("descripcion")) for r in data.get("regiones", [])
            ),
            "descripcionFinalidad": safe_value(data.get("descripcionFinalidad")),
            "descripcionBasesReguladoras": safe_value(
                data.get("descripcionBasesReguladoras")
            ),
            "urlBasesReguladoras": safe_value(data.get("urlBasesReguladoras")),
            "sePublicaDiarioOficial": safe_value(data.get("sePublicaDiarioOficial")),
            "abierto": safe_value(data.get("abierto")),
            "fechaInicioSolicitud": safe_value(data.get("fechaInicioSolicitud")),
            "fechaFinSolicitud": safe_value(data.get("fechaFinSolicitud")),
            "textInicio": safe_value(data.get("textInicio")),
            "textFin": safe_value(data.get("textFin")),
            "reglamento": safe_value(
                data.get("reglamento", {}).get("descripcion")
            ),
            "documentos": ", ".join(
                safe_value(d.get("descripcion")) for d in data.get("documentos", [])
            ),
        },
    )
    return template.format_map(flat_data)

# Generar texto
formatted_text = safe_format(data, template)
print(formatted_text)
