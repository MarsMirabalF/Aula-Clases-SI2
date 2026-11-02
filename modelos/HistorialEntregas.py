from datetime import datetime

from firebase_admin import db


class HistorialEntregas:
    def guardar(self, tarea, fechaEntrega=None):
        momento = (fechaEntrega or datetime.now()).replace(microsecond=0)
        db.reference("entregas").push({
            "numero": tarea.numero,
            "tema": tarea.tema,
            "fechaEntrega": momento.isoformat(),
            "aTiempo": not tarea.estaAtrasada(momento)
        })

    def mostrarEntregas(self):
        registros = db.reference("entregas").get() or {}
        entregas = []
        for idEntrega, registro in registros.items():
            fechaEntrega = datetime.fromisoformat(registro["fechaEntrega"])
            entregas.append({
                "id": idEntrega,
                "tarea": "Tarea " + str(registro["numero"]) + " - " + registro["tema"],
                "fechaEntrega": fechaEntrega,
                "fecha": fechaEntrega.strftime("%d/%m/%Y %H:%M"),
                "estado": "A tiempo" if registro["aTiempo"] else "Con retraso"
            })
        return sorted(entregas, key=lambda entrega: entrega["fechaEntrega"], reverse=True)

    def mostrarATiempoYRetraso(self):
        entregas = self.mostrarEntregas()
        aTiempo = sum(entrega["estado"] == "A tiempo" for entrega in entregas)
        return aTiempo, len(entregas) - aTiempo
