from datetime import datetime

from firebase_admin import db


class Participacion:
    def registrar(self, pregunta, esCorrecta, fecha=None):
        if not isinstance(pregunta, str) or not pregunta.strip():
            raise ValueError("La participación debe tener una pregunta.")
        if not isinstance(esCorrecta, bool):
            raise ValueError("El resultado de la participación no es válido.")
        momento = fecha or datetime.now().astimezone()
        registro = {
            "pregunta": pregunta.strip(),
            "fecha": momento.isoformat(timespec="seconds"),
            "esCorrecta": esCorrecta,
        }
        referencia = db.reference("participaciones").push(registro)
        return {"id": referencia.key, **registro} if referencia is not None else registro
