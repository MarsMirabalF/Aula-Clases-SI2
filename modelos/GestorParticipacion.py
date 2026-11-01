from modelos.HistorialParticipacion import HistorialParticipacion
from modelos.Participacion import Participacion
from modelos.PreguntaClase import PreguntaClase


class GestorParticipacion:
    PREGUNTAS = (
        "¿Qué representa un diagrama de clases en UML?",
        "¿Qué reunión de Scrum se realiza diariamente para revisar el avance del equipo?",
        "¿Qué práctica de XP consiste en programar en parejas?",
    )

    def __init__(self):
        self.participacion = Participacion()
        self.historial = HistorialParticipacion()

    def obtenerPregunta(self, indice=0):
        return PreguntaClase(self.PREGUNTAS[indice % len(self.PREGUNTAS)])

    def registrarParticipacion(self, pregunta, esCorrecta):
        return self.participacion.registrar(pregunta.obtenerPregunta(), esCorrecta)

    def listarParticipaciones(self):
        return self.historial.consultar()

    def contarCorrectas(self):
        return self.historial.contarCorrectas()

    def contarIncorrectas(self):
        return self.historial.contarIncorrectas()
