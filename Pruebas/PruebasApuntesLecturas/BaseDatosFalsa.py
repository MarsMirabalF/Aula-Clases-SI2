from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pymupdf

from modelos.GestorApuntes import GestorApuntes


class ReferenciaFalsa:
    """Simula referencias de Firebase sin compartir objetos con los modelos."""

    def __init__(self, registros, ruta=""):
        self.registros = registros
        self.ruta = [parte for parte in str(ruta).split("/") if parte]

    def get(self):
        registro = self.registros
        for parte in self.ruta:
            if not isinstance(registro, dict) or parte not in registro:
                return None
            registro = registro[parte]
        return deepcopy(registro) if registro else None

    def set(self, datos):
        if not self.ruta:
            self.registros.clear()
            self.registros.update(deepcopy(datos or {}))
            return
        padre = self.registros
        for parte in self.ruta[:-1]:
            padre = padre.setdefault(parte, {})
        if datos is None:
            padre.pop(self.ruta[-1], None)
        else:
            padre[self.ruta[-1]] = deepcopy(datos)

    def update(self, datos):
        for clave, valor in datos.items():
            self.child(clave).set(valor)

    def child(self, ruta):
        return ReferenciaFalsa(
            self.registros, "/".join(self.ruta + [str(ruta)])
        )

    def delete(self):
        self.set(None)


def crearGestorConBaseFalsa(prueba):
    """Aísla tanto Firebase como los archivos de cada prueba."""
    temporal = TemporaryDirectory()
    prueba.addCleanup(temporal.cleanup)
    carpeta = Path(temporal.name)
    registros = {}
    parche = patch(
        "firebase_admin.db.reference",
        side_effect=lambda ruta="", **kwargs: ReferenciaFalsa(registros, ruta),
    )
    parche.start()
    prueba.addCleanup(parche.stop)
    return GestorApuntes(carpetaProyecto=carpeta), registros, carpeta


def crearPdf(ruta, texto="Lectura de prueba", protegido=False):
    ruta = Path(ruta)
    with pymupdf.open() as documento:
        pagina = documento.new_page()
        pagina.insert_text((72, 72), texto)
        opciones = {}
        if protegido:
            opciones = {
                "encryption": pymupdf.PDF_ENCRYPT_AES_256,
                "owner_pw": "propietario",
                "user_pw": "lector",
            }
        documento.save(str(ruta), **opciones)
    return ruta
