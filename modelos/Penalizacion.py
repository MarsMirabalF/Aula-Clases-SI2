from firebase_admin import db


class Penalizacion:
    def __init__(self, horarioClases):
        self.horarioClases = horarioClases

    def registrarLlegadaTarde(self, fechaTarde):
        if not self.horarioClases.esDiaDeClase(fechaTarde):
            return False
        fechaProximaClase = self.horarioClases.calcularProximaClase(fechaTarde)
        db.reference("penalizaciones").push({
            "fechaTarde": fechaTarde.isoformat(),
            "fechaProximaClase": fechaProximaClase.isoformat(),
            "estado": "Pendiente"
        })
        return True

    def marcarComoCumplida(self, idPenalizacion):
        db.reference("penalizaciones/" + idPenalizacion).update({"estado": "Cumplida"})