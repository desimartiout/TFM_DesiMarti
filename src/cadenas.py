class Cadenas:
    """
    Clase con métodos Helper que facilitan los prompts al script principal del LLM
    """

    @staticmethod
    def obtenerPROMPTTemplatePrincipal():
        return """
            Eres un asistente chat (chatbot) para ayudar obtener información de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario para encontrar las subvenciones que necesite el usuario en base a sus criterios de búsqueda.
            * Proporciona detalles del organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Sofo ofrece información a partir del Contexto proporcionado.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.

            ----
            Contexto:
                {context}
            ....

            Pregunta: 
                {input}
            """

    @staticmethod
    def obtener_ayuda():
        MARKDOWN = """
        ## Manejo del chatbot:
        
        ### Uso basico:
        Escribe frases que ayuden al chatbot a obtener las ayudas y subvenciones más fácilmente, por ejemplo puedes usar estas:
        <pre>Búscame ayudas de Murcia para PYMES</pre>
        <pre>Localiza todas ayudas de Personas físicas para turismo.</pre>
        
        ### Metafunciones:
        <pre>@resetear_sesion: Resetea el chatbot para empezar de nuevo</pre>
        <pre>@ver_historial: OEPIA te muestra todo lo que ha conversado contigo</pre>
        """
        return MARKDOWN