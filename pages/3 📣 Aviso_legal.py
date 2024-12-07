import streamlit as st

# Configuración de la página
st.set_page_config(page_title="HelpMe.ai - Aviso Legal", layout="wide")

# Versión completa del aviso legal
detalle = """

**⚠️ Aviso importante ⚠️**

El presente asistente ha sido diseñado para proporcionar información basada en datos obtenidos del Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas <a href='https://www.pap.hacienda.gob.es/bdnstrans/GE/es/inicio'>(url acceso)</a> de la Intervención General de la Administración del Estado del 🏛️ Gobierno de España 🏛️. 

ℹ️ La Internvención General del Estado **NO apoya ni patrocina** este asistente, siendo agena a la existencia del mismo ℹ️.

**Descargo de responsabilidad**

A pesar de los esfuerzos realizados para garantizar la precisión y actualidad de la información proporcionada, no podemos garantizar que dicha información sea siempre completa, precisa o libre de errores.

El usuario reconoce que la información suministrada por el asistente puede contener imprecisiones, omisiones o errores, y se compromete a verificar la exactitud y validez de la información antes de tomar cualquier decisión basada en ella.

El uso del asistente es bajo el propio riesgo del usuario. En ningún caso nos hacemos responsables de los posibles errores, perjuicios o daños que puedan derivarse del uso o de la interpretación incorrecta de la información proporcionada, incluyendo pero no limitándose a decisiones de carácter administrativo, legal, financiero o de cualquier otro tipo.

Se recomienda encarecidamente al usuario que consulte con un experto o recurra a las fuentes oficiales para confirmar cualquier información relevante antes de actuar en base a la misma.




***Fecha de última actualización de los datos de las ayudas: 15/12/2024 a las 23:45 horas.***
"""

# Interfaz de la aplicación
st.title("Aviso Legal")
st.markdown(detalle, unsafe_allow_html=True)
