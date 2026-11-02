from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pymupdf

from modelos.GestorApuntes import GestorApuntes


class ReferenciaFalsa:
    def __init__(self, registros, ruta):
        self.registros = registros
        self.ruta = ruta

    def get(self):
        partes = self.ruta.split("/")
        registros = self.registros.get(partes[0], {})
        if len(partes) == 2:
            return deepcopy(registros.get(partes[1]))
        return deepcopy(registros) or None

    def set(self, datos):
        coleccion, idRegistro = self.ruta.split("/")
        self.registros.setdefault(coleccion, {})[idRegistro] = deepcopy(datos)


def crearGestorConBaseFalsa(prueba):
    temporal = TemporaryDirectory()
    prueba.addCleanup(temporal.cleanup)
    carpeta = Path(temporal.name)
    registros = {}
    parche = patch("firebase_admin.db.reference",
                   side_effect=lambda ruta: ReferenciaFalsa(registros, ruta))
    parche.start()
    prueba.addCleanup(parche.stop)
    return GestorApuntes(carpetaProyecto=carpeta), registros, carpeta


def crearPdf(ruta):
    with pymupdf.open() as documento:
        pagina = documento.new_page()
        pagina.insert_text((72, 72), "Lectura de prueba")
        documento.save(str(ruta))
    return ruta
