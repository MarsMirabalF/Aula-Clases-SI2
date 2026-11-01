from unittest.mock import patch
from modelos.GestorPenalizaciones import GestorPenalizaciones


class ReferenciaFalsa:
    def __init__(self, registros, ruta):
        self.registros = registros
        self.ruta = ruta

    def get(self):
        return self.registros or None

    def push(self, datos):
        self.registros["id" + str(len(self.registros) + 1)] = datos

    def update(self, datos):
        self.registros[self.ruta.split("/")[1]].update(datos)


def crearGestorConBaseFalsa(prueba):
    registros = {}
    parche = patch("firebase_admin.db.reference",
                   side_effect=lambda ruta: ReferenciaFalsa(registros, ruta))
    parche.start()
    prueba.addCleanup(parche.stop)
    return GestorPenalizaciones()
