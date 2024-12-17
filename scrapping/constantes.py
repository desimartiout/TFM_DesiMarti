
import os

URL_BASE_API = "https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias/ultimas?vpd=GE&order=fechaRecepcion&direccion=desc"
URL_CONVOCATORIA= "https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias?numConv="
URL_CONVOCATORIA_POST= "&vpd=GE"
#https://www.pap.hacienda.gob.es/bdnstrans/api/convocatorias?numConv=790767&vpd=GE

PAGE_SIZE = 200
TOTAL_PAGES = 1 

ruta_actual = os.getcwd()   #Ruta donde se ejecuta el fichero python
RUTA_DESTINO_DOCUMENTOS = f"{ruta_actual}\Documentos"
SCRAP_FILE_PATH_LOG = "/logs/"

TEMPLATE_DOC_OLD = """
Detalle de la convocatoria de ayuda o  subvención: {codigoBDNS}
Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/{codigoBDNS}
Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: {organo_nivel1} - {organo_nivel2}
Enlace / url a sede electrónica presentación ayuda: {sedeElectronica}
Fecha de recepción: {fechaRecepcion}
Tipo de ayuda: {instrumentos}
Tipo de convocatoria: {tipoConvocatoria}
Presupuesto total: {presupuestoTotal} Euros
Descripción: {descripcion}
Tipos de beneficiarios: {tiposBeneficiarios}
Sectores involucrados: {sectores}
Región de impacto: {regiones}
Finalidad: {descripcionFinalidad}
Bases reguladoras: {descripcionBasesReguladoras}
URL Bases Reguladoras: {urlBasesReguladoras}
Publicación en diario oficial: {sePublicaDiarioOficial}
Estado de convocatoria abierta: {abierto}
Fecha de inicio de solicitudes: {fechaInicioSolicitud}
Fecha de fin de solicitudes: {fechaFinSolicitud}
Inicio de convocatoria: {textInicio}
Fin de convocatoria: {textFin}
Reglamento: {reglamento}
Otros documentos de la convocatoria: {documentos}
"""

TEMPLATE_DOC = """
Detalle de la convocatoria de ayuda o  subvención: {codigoBDNS}
Enlace a convocatoria: https://www.pap.hacienda.gob.es/bdnstrans/GE/es/convocatorias/{codigoBDNS}
Órgano, comunidad, autonomía, provincia o ayuntamiento convocante: {organo_nivel1} - {organo_nivel2}
Fecha de recepción: {fechaRecepcion}
Tipo de ayuda: {instrumentos}
Tipo de convocatoria: {tipoConvocatoria}
Presupuesto total: {presupuestoTotal} Euros
Descripción: {descripcion}
Tipos de beneficiarios: {tiposBeneficiarios}
Sectores involucrados: {sectores}
Región de impacto: {regiones}
Finalidad: {descripcionFinalidad}
Bases reguladoras: {descripcionBasesReguladoras}
Publicación en diario oficial: {sePublicaDiarioOficial}
Estado de convocatoria abierta: {abierto}
Inicio de convocatoria: {textInicio}
Fin de convocatoria: {textFin}
"""
