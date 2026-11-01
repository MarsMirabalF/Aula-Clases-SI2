from datetime import date, datetime
from uuid import uuid4

from firebase_admin import db
from modelos.Lectura import Lectura, validarId


def convertirFechaClase(fechaClase):
    if isinstance(fechaClase, datetime):
        return fechaClase.date()
    if isinstance(fechaClase, date):
        return fechaClase
    if isinstance(fechaClase, str):
        try:
            return date.fromisoformat(fechaClase)
        except ValueError:
            pass
    raise ValueError("Escribe una fecha de clase válida con formato AAAA-MM-DD.")


class Apunte:
    def __init__(self, lectura=None):
        self.lectura = lectura if lectura is not None else Lectura()

    def prepararRegistro(self, texto, fechaClase, idLectura):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("Escribe el contenido del apunte antes de guardar.")
        fecha = convertirFechaClase(fechaClase)
        if self.lectura.obtenerLectura(idLectura) is None:
            raise ValueError("La lectura seleccionada no existe.")
        return {"texto": texto, "fechaClase": fecha.isoformat(), "idLectura": idLectura}

    def registrarApunte(self, texto, fechaClase, idLectura):
        registro = self.prepararRegistro(texto, fechaClase, idLectura)
        idApunte = uuid4().hex
        db.reference("apuntes/" + idApunte).set(registro)
        return {"id": idApunte, **registro}

    def editarApunte(self, idApunte, texto, fechaClase, idLectura):
        validarId(idApunte, "un apunte")
        referencia = db.reference("apuntes/" + idApunte)
        if referencia.get() is None:
            raise ValueError("El apunte que intentas editar no existe.")
        registro = self.prepararRegistro(texto, fechaClase, idLectura)
        referencia.set(registro)
        return {"id": idApunte, **registro}

    def listarApuntes(self):
        registros = db.reference("apuntes").get() or {}
        return [{**registro, "id": idApunte} for idApunte, registro in registros.items()]
