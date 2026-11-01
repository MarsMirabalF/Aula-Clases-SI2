from datetime import datetime

from firebase_admin import db


class HistorialParticipacion:
    def guardar(self, participacion):
        db.reference("participaciones").push(participacion)

    def consultar(self):
        registros = db.reference("participaciones").get() or {}
        historial = []
        for identificador, registro in registros.items():
            fecha = datetime.fromisoformat(registro["fecha"])
            esCorrecta = bool(registro["esCorrecta"])
            historial.append({
                "id": identificador,
                "pregunta": registro["pregunta"],
                "fecha": fecha.strftime("%d/%m/%Y %H:%M"),
                "esCorrecta": esCorrecta,
                "resultado": "Correcta" if esCorrecta else "Incorrecta",
            })
        return sorted(historial, key=lambda registro: registro["fecha"], reverse=True)

    def contarCorrectas(self):
        return sum(registro["esCorrecta"] for registro in self.consultar())

    def contarIncorrectas(self):
        return sum(not registro["esCorrecta"] for registro in self.consultar())
