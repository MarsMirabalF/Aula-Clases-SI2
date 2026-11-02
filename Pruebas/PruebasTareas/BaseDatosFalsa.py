from unittest.mock import patch


class ReferenciaFalsa:
    def __init__(self, registros):
        self.registros = registros

    def get(self):
        return self.registros or None

    def push(self, datos):
        self.registros["id" + str(len(self.registros) + 1)] = datos


def usarBaseFalsa(prueba):
    colecciones = {}
    parche = patch("firebase_admin.db.reference",
                   side_effect=lambda ruta: ReferenciaFalsa(colecciones.setdefault(ruta, {})))
    parche.start()
    prueba.addCleanup(parche.stop)
