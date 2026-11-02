from unittest.mock import patch

from modelos.GestorParticipacion import GestorParticipacion


class ReferenciaFalsa:
    def __init__(self, registros, ruta):
        self.registros = registros
        self.ruta = ruta
        self.key = None

    def get(self):
        return self.registros.get(self.ruta) or None

    def push(self, datos):
        participaciones = self.registros.setdefault(self.ruta, {})
        self.key = "id" + str(len(participaciones) + 1)
        participaciones[self.key] = datos
        return self


def crearGestorConBaseFalsa(prueba):
    registros = {}
    parche = patch(
        "firebase_admin.db.reference",
        side_effect=lambda ruta: ReferenciaFalsa(registros, ruta))
    parche.start()
    prueba.addCleanup(parche.stop)
    return GestorParticipacion()
