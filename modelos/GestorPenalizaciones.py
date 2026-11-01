from datetime import date
from firebase_admin import db
from modelos.HorarioClases import HorarioClases
from modelos.Penalizacion import Penalizacion


class GestorPenalizaciones:
    def __init__(self):
        self.horarioClases = HorarioClases()
        self.penalizacion = Penalizacion(self.horarioClases)

    def registrarLlegadaTarde(self):
        self.penalizacion.registrarLlegadaTarde(date.today())

    def marcarComoCumplida(self, idPenalizacion):
        self.penalizacion.marcarComoCumplida(idPenalizacion)

    def listarPenalizaciones(self):
        registros = db.reference("penalizaciones").get() or {}
        lista = []
        for idPenalizacion, registro in registros.items():
            fechaTarde = date.fromisoformat(registro["fechaTarde"])
            fechaProximaClase = date.fromisoformat(registro["fechaProximaClase"])
            pendiente = registro["estado"] == "Pendiente"
            lista.append({
                "id": idPenalizacion,
                "diaTarde": self.horarioClases.obtenerNombreDia(fechaTarde),
                "fechaTarde": fechaTarde.isoformat(),
                "proximaClase": (self.horarioClases.obtenerNombreDia(fechaProximaClase)
                                 + " " + fechaProximaClase.isoformat()) if pendiente else "-",
                "estado": registro["estado"]
            })
        return sorted(lista, key=lambda penalizacion: penalizacion["fechaTarde"])

    def contarLlegadasTarde(self):
        return len(self.listarPenalizaciones())
