

#pip install -r requirements.txt

#pip install vectordb2 
#pip install spacy==3.6.0
#pip intall lightning==2.0.5
#pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.6.0/en_core_web_sm-3.6.0.tar.gz


from vectordb import Memory
import re

memory = Memory(chunking_strategy={'mode':'sliding_window', 'window_size': 32, 'overlap': 4})

# Esto simula los embeddings --> Lo hace manual pero se debería hacer
def tokenize( msg:str ):
    msg = msg.replace( "coche", "vehiculo" )

    ret = [ ]
    not_words = [ "", "con", "de", "y" ]
    msg = re.split("[ ,\.?]", msg)
    
    for m in msg:
        if m not in not_words:
            ret.append( m )

    print( ret )

    return " ".join( ret )

#Además para que funcione.... Reemplazar en el json los null por "", False por False, True por True

memory.save(
    tokenize("subvención y entrega dineraria sin contraprestación ofrecida por Ayuntamiento de Gandia (Gandia) con impacto en la COMUNIDAD VALENCIANA, ofrecida para personas físicas que no desarrollan actividad económica cuya finalidad es el acceso a la vivienda y fomento de la edificación. El título es '2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda'"), 
    {"id":992327,"organo":{"nivel1":"GANDIA","nivel2":"AYUNTAMIENTO DE GANDIA","nivel3":""},"sedeElectronica":"https://gandia.sedelectronica.es/","codigoBDNS":"790767","fechaRecepcion":"2024-10-14T15:57:09+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":100000,"mrr":False,"descripcion":"2024 - Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PERSONAS FÍSICAS QUE NO DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"OTROS SERVICIOS","codigo":"S"}],"regiones":[{"descripcion":"ES52 - COMUNIDAD VALENCIANA"}],"descripcionFinalidad":"Acceso a la vivienda y fomento de la edificación","descripcionBasesReguladoras":"Convocatoria de ayudas destinadas a seguros y mejoras en viviendas para alquiler como residencia habitual en el marco del Plan Estratégico del Ayuntamiento de Gandia para facilitar el acceso a la vivienda.","urlBasesReguladoras":"www.bop.es","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"2024-10-31T00:00:00+01:00","fechaFinSolicitud":"2024-11-15T00:00:00+01:00","textInicio":"","textFin":"","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144216,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241011_Certificat_punt 4 Aprobación convocatoria ayuda alquiler residencia habitual, facilitar acceso a la vivienda. Exp. 35295-2024.pdf","long":344807,"datMod":"2024-10-14T18:15:02.000+02:00","datPublicacion":"2024-10-14T18:15:02.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."},
)

memory.save(
    tokenize( "subvención y entrega dineraria sin contraprestación ofrecida por AYUNTAMIENTO DE VILLA DE MAZO (VILLA DE MAZO) con impacto en La Palma, ofrecida para PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA cuya finalidad es INDUSTRIA Y ENERGÍA. El título es 'SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024'" ), 
    {"id":992284,"organo":{"nivel1":"VILLA DE MAZO","nivel2":"AYUNTAMIENTO DE VILLA DE MAZO","nivel3":""},"sedeElectronica":"WWW.SEDELECTRONICA.VILLADEMAZO.ES","codigoBDNS":"790724","fechaRecepcion":"2024-10-14T14:24:36+02:00","instrumentos":[{"descripcion":"SUBVENCIÓN Y ENTREGA DINERARIA SIN CONTRAPRESTACIÓN "}],"tipoConvocatoria":"Concurrencia competitiva - canónica","presupuestoTotal":70000,"mrr":False,"descripcion":"SUBVENCIONES A INSTALACIONES DE AUTOCONSUMO MEDIANTE SISTEMAS FOTOVOLTAICOS 2024","descripcionLeng":"","tiposBeneficiarios":[{"descripcion":"PYME Y PERSONAS FÍSICAS QUE DESARROLLAN ACTIVIDAD ECONÓMICA"}],"sectores":[{"descripcion":"SUMINISTRO DE ENERGÍA ELÉCTRICA, GAS, VAPOR Y AIRE ACONDICIONADO","codigo":"D"}],"regiones":[{"descripcion":"ES707 - La Palma"}],"descripcionFinalidad":"Industria y Energía","descripcionBasesReguladoras":"BASES GENERALES REGULADORAS DE LA CONCESION DE SUBVENCIONES EN REGIMEN DE CONCURRENCIA COMPETITIVA EN EL AYUNTAMIENTO DE VILLA DE MAZO (BOP SANTA CRUZ DE TFE 108 DE FECHA 06/09/2024)","urlBasesReguladoras":"https://www.bopsantacruzdetenerife.es/bopsc2/index.php","sePublicaDiarioOficial":True,"abierto":False,"fechaInicioSolicitud":"","fechaFinSolicitud":"","textInicio":"A PARTIR DEL DIA SIGUIENTE DE LA PUBLICACION DEL EXTRACTO DE LA CONVOCATORIA EN EL BOP de S/C TFE.","textFin":"QUINCE DIAS HABILES A PARTIR DE LA FECHA DE INICIO","ayudaEstado":"","urlAyudaEstado":"","fondos":[],"reglamento":"","objetivos":[],"sectoresProductos":[],"documentos":[{"id":1144134,"descripcion":"Documento de la convocatoria en español","nombreFic":"20241014_Resolución_Decreto de Alcaldía _ Decreto de Presidencia _RESOLUCIONES ALCALDIA 2024 2024-1055 [APROBACIÓN DE LA CONVOCATORIA]_compressed (1).pdf","long":318170,"datMod":"2024-10-14T15:15:03.000+02:00","datPublicacion":"2024-10-14T15:15:03.000+02:00"}],"anuncios":[],"advertencia":"La reutilización de los datos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas está sujeta a una serie de restricciones y consideraciones legales. Consulte el aviso legal en https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal.Además, el usuario debe ser consciente que la información presentada es de naturaleza dinámica, y que los datos pueden ser sometidos a correcciones, inserciones, modificaciones y eliminaciones en momentos posteriores a su extracción."}
)

print(
    memory.search( tokenize( "subvención para vivienda?" ), top_n=1)
)
