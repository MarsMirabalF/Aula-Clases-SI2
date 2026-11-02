from datetime import date, datetime
from uuid import uuid4

from firebase_admin import db


def convertirFechaClase(fechaClase):
    if isinstance(fechaClase, datetime):
        fechaClase = fechaClase.date()
    try:
        return date.fromisoformat(str(fechaClase))
    except ValueError:
        raise ValueError("Escribe una fecha de clase válida con formato AAAA-MM-DD.") from None


class Apunte:
    def registrarApunte(self, texto, fechaClase, idLectura, idApunte=None):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("Escribe el contenido del apunte antes de guardar.")
        fecha = convertirFechaClase(fechaClase)
        if idLectura not in (db.reference("lecturas").get() or {}):
            raise ValueError("La lectura seleccionada no existe.")
        registro = {"texto": texto, "fechaClase": fecha.isoformat(), "idLectura": idLectura}
        idApunte = idApunte or uuid4().hex
        db.reference("apuntes/" + idApunte).set(registro)
        return {"id": idApunte, **registro}

    def editarApunte(self, idApunte, texto, fechaClase, idLectura):
        if idApunte not in (db.reference("apuntes").get() or {}):
            raise ValueError("El apunte que intentas editar no existe.")
        return self.registrarApunte(texto, fechaClase, idLectura, idApunte)

    def listarApuntes(self):
        registros = db.reference("apuntes").get() or {}
        return [{**registro, "id": idApunte} for idApunte, registro in registros.items()]
