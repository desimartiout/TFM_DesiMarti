class Cadenas:
    """
    Clase con métodos Helper que facilitan los prompts al script principal del LLM
    """

    @staticmethod
    def obtenerPROMPTTemplatePrincipal():
        """
        Método estatico que devuelve el PROMPT al script principal del LLM
        :return: SystemPrompt para el LLM principal
        """
        return """
            Eres un asistente chat (chatbot) para ayudar obtener ingformación de ayudas y subvenciones del Gobierno de España, tus principales misiones son:            
            * Ayudar al usuario para encontrar las subvenciones que necesite el usuario en base a sus criterios de búsqueda.
            * Deberás de identificar las oportunidades de ayudas y subvenciones.
            * Proporciona detalles el organismo que la publica, la descripción de la convocatoria, el importe, región finalidad y beneficiarios de la ayuda o subvención.
            * Ofrece consejos sobre cómo mejorar mi aplicación y aumentar mis posibilidades de éxito.
            * Cuando te pregunten por las ayudas y subvenciones centrate en la información que te proporciona el contexto.

            * Es importante que los resultados sean precisos y actualizados.
            * No te inventes información ni rellenes los datos vacios. Si no tienes ayudas que cumplan el criterio di que no tienes. Como eres un chat amigable :) también tienes la capacidad de reponder a preguntas no relaccionadas con las ayudas de subvenciones.

            <context>
            {context}
            </context>

            Pregunta: {input}
            """

    @staticmethod
    def obtener_ayuda():
        """
        Método estático que devuelve el codigo HTML estático que ayuda a manejar el chatbot
        :param
        :return: HTML de ayuda
        """
        MARKDOWN = """
        ## Manejo del chatbot:
        
        ### Uso basico:
        Escribe frases que ayuden al chatbot a obtener las ayudas y subvenciones más fácilmente, por ejemplo puedes usar estas:
        <pre>Búscame las ayudas de Murcia para PYME</pre>
        <pre>Localiza todas las ayudas de Personas físicas cuya finalidad sea el turismo.</pre>
        
        ### Metafunciones:
        <pre>@resetear_sesion: Resetea el chatbot para empezar de nuevo</pre>
        <pre>@ver_historial: OEPIA te muestra todo lo que ha conversado contigo</pre>
        """
        return MARKDOWN