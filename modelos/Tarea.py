from datetime import datetime, timedelta

from firebase_admin import db

FORMATO_HORA_LIMITE = "%Y-%m-%d %H:%M"


def convertirHoraLimite(horaLimite):
    if isinstance(horaLimite, datetime):
        return horaLimite.replace(second=0, microsecond=0)
    if isinstance(horaLimite, str):
        try:
            return datetime.strptime(horaLimite.strip(), FORMATO_HORA_LIMITE)
        except ValueError:
            pass
    raise ValueError("Escribe una hora límite válida con formato AAAA-MM-DD HH:MM.")


class Tarea:
    def __init__(self, numero, tema, horaLimite):
        try:
            numero = int(numero)
        except (TypeError, ValueError):
            raise ValueError("El número de tarea debe ser un número entero.") from None
        if numero <= 0:
            raise ValueError("El número de tarea debe ser mayor a cero.")
        if not isinstance(tema, str) or not tema.strip():
            raise ValueError("Escribe el tema de la tarea.")
        self.numero = numero
        self.tema = tema.strip()
        self.horaLimite = convertirHoraLimite(horaLimite)

    def guardar(self):
        if any(tarea.numero == self.numero for tarea in Tarea.listarTareas()):
            raise ValueError("Ya existe la Tarea " + str(self.numero) + ".")
        db.reference("tareas").push({
            "numero": self.numero,
            "tema": self.tema,
            "horaLimite": self.horaLimite.strftime(FORMATO_HORA_LIMITE)
        })

    def calcularTiempoRestante(self, ahora=None):
        restante = self.horaLimite - (ahora or datetime.now())
        return max(restante, timedelta(0))

    def estaAtrasada(self, ahora=None):
        return (ahora or datetime.now()) > self.horaLimite

    @staticmethod
    def listarTareas():
        registros = db.reference("tareas").get() or {}
        tareas = [Tarea(registro["numero"], registro["tema"], registro["horaLimite"])
                  for registro in registros.values()]
        return sorted(tareas, key=lambda tarea: tarea.numero)
