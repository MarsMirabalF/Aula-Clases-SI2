import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import (
    ReferenciaFalsa,
    crearGestorConBaseFalsa,
    crearPdf,
)


class PruebaCriterio1ImportarVerPdf(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)

    def testImportaUnaCopiaQueSigueDisponibleSinElOriginal(self):
        original = crearPdf(self.carpeta / "original.pdf", "Contenido para leer")

        lectura = self.gestor.agregarLectura("Lectura de clase", original)
        original.unlink()
        ruta = Path(self.gestor.obtenerRutaPdf(lectura["id"]))

        self.assertTrue(ruta.is_relative_to(self.carpeta / "Archivos" / "Lecturas"))
        self.assertEqual(self.gestor.listarLecturas()[0]["titulo"], "Lectura de clase")
        with pymupdf.open(ruta) as documento:
            self.assertEqual(documento.page_count, 1)
            self.assertIn("Contenido para leer", documento[0].get_text())

    def testLecturasConElMismoTituloNoSobrescribenSusArchivos(self):
        primera = self.gestor.agregarLectura(
            "Tema", crearPdf(self.carpeta / "primera.pdf", "Primera lectura")
        )
        segunda = self.gestor.agregarLectura(
            "Tema", crearPdf(self.carpeta / "segunda.pdf", "Segunda lectura")
        )

        self.assertNotEqual(primera["id"], segunda["id"])
        rutaPrimera = self.gestor.obtenerRutaPdf(primera["id"])
        rutaSegunda = self.gestor.obtenerRutaPdf(segunda["id"])
        self.assertNotEqual(rutaPrimera, rutaSegunda)
        with pymupdf.open(rutaPrimera) as documento:
            self.assertIn("Primera lectura", documento[0].get_text())
        with pymupdf.open(rutaSegunda) as documento:
            self.assertIn("Segunda lectura", documento[0].get_text())

    def testRechazaUnPdfInvalidoOProtegidoSinRegistrarlo(self):
        invalido = self.carpeta / "invalido.pdf"
        invalido.write_text("Esto no es un PDF", encoding="utf-8")
        protegido = crearPdf(self.carpeta / "protegido.pdf", protegido=True)

        for ruta in (invalido, protegido):
            with self.subTest(archivo=ruta.name):
                with self.assertRaises(ValueError):
                    self.gestor.agregarLectura("Lectura", ruta)

        self.assertEqual(self.gestor.listarLecturas(), [])

    def testEliminaLaCopiaSiFirebaseNoPuedeRegistrarLaLectura(self):
        original = crearPdf(self.carpeta / "original.pdf")

        with patch.object(ReferenciaFalsa, "set", side_effect=RuntimeError("Sin conexión")):
            with self.assertRaises(RuntimeError):
                self.gestor.agregarLectura("Lectura", original)

        self.assertTrue(original.is_file())
        self.assertEqual(self.gestor.listarLecturas(), [])
        self.assertEqual(list((self.carpeta / "Archivos" / "Lecturas").glob("*.pdf")), [])

    def testInformaCuandoLaCopiaImportadaYaNoExiste(self):
        lectura = self.gestor.agregarLectura(
            "Lectura", crearPdf(self.carpeta / "original.pdf")
        )
        Path(self.gestor.obtenerRutaPdf(lectura["id"])).unlink()

        with self.assertRaises(FileNotFoundError):
            self.gestor.obtenerRutaPdf(lectura["id"])

    def testImpideAbrirUnaRutaFueraDeLaCarpetaDeLecturas(self):
        original = crearPdf(self.carpeta / "original.pdf")
        lectura = self.gestor.agregarLectura("Lectura", original)
        self.registros["lecturas"][lectura["id"]]["rutaArchivo"] = str(original)

        with self.assertRaises(ValueError):
            self.gestor.obtenerRutaPdf(lectura["id"])


if __name__ == "__main__":
    unittest.main()
