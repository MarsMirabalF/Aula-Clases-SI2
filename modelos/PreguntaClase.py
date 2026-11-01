class PreguntaClase:
    def __init__(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("La pregunta no puede estar vacía.")
        self.texto = texto.strip()

    def mostrarPregunta(self):
        return self.texto

    def obtenerPregunta(self):
        return self.texto
