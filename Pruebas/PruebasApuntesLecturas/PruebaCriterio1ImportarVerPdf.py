import unittest
from pathlib import Path
from unittest.mock import patch

import pymupdf

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import ReferenciaFalsa, crearGestorConBaseFalsa, crearPdf


class PruebaCriterio1ImportarVerPdf(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)

    def testImportaUnaLecturaPdf(self):
        archivo = crearPdf(self.carpeta / "crc.pdf", "Responsabilidades y colaboradores")

        lectura = self.gestor.agregarLectura("Tarjetas CRC", archivo)

        self.assertEqual(self.gestor.listarLecturas()[0]["titulo"], "Tarjetas CRC")
        with pymupdf.open(self.gestor.obtenerRutaPdf(lectura["id"])) as documento:
            self.assertEqual(documento.page_count, 1)
            self.assertIn("Responsabilidades y colaboradores", documento[0].get_text())

    def testGuardaUnaCopiaDelPdf(self):
        original = crearPdf(self.carpeta / "crc.pdf", "Responsabilidades y colaboradores")
        lectura = self.gestor.agregarLectura("Tarjetas CRC", original)

        original.unlink()

        ruta = Path(self.gestor.obtenerRutaPdf(lectura["id"]))
        self.assertEqual(ruta.parent, self.carpeta / "Archivos" / "Lecturas")
        with pymupdf.open(ruta) as documento:
            self.assertIn("Responsabilidades y colaboradores", documento[0].get_text())

    def testPermiteDosLecturasConElMismoTitulo(self):
        archivo1 = crearPdf(self.carpeta / "primera.pdf", "Primera lectura")
        archivo2 = crearPdf(self.carpeta / "segunda.pdf", "Segunda lectura")

        primera = self.gestor.agregarLectura("Tarjetas CRC", archivo1)
        segunda = self.gestor.agregarLectura("Tarjetas CRC", archivo2)

        self.assertNotEqual(primera["id"], segunda["id"])
        rutaPrimera = self.gestor.obtenerRutaPdf(primera["id"])
        rutaSegunda = self.gestor.obtenerRutaPdf(segunda["id"])
        self.assertNotEqual(rutaPrimera, rutaSegunda)
        with pymupdf.open(rutaPrimera) as documento:
            self.assertIn("Primera lectura", documento[0].get_text())
        with pymupdf.open(rutaSegunda) as documento:
            self.assertIn("Segunda lectura", documento[0].get_text())

    def testNoImportaUnPdfDanado(self):
        archivo = self.carpeta / "crc.pdf"
        archivo.write_text("Esto no es un PDF", encoding="utf-8")

        with self.assertRaises(ValueError):
            self.gestor.agregarLectura("Tarjetas CRC", archivo)

        self.assertEqual(self.gestor.listarLecturas(), [])

    def testNoImportaUnPdfConContrasena(self):
        archivo = crearPdf(self.carpeta / "crc.pdf", protegido=True)

        with self.assertRaises(ValueError):
            self.gestor.agregarLectura("Tarjetas CRC", archivo)

        self.assertEqual(self.gestor.listarLecturas(), [])

    def testBorraLaCopiaSiFallaElRegistro(self):
        original = crearPdf(self.carpeta / "crc.pdf")

        with patch.object(ReferenciaFalsa, "set", side_effect=RuntimeError("Sin conexión")):
            with self.assertRaises(RuntimeError):
                self.gestor.agregarLectura("Tarjetas CRC", original)

        self.assertTrue(original.is_file())
        self.assertEqual(self.gestor.listarLecturas(), [])
        self.assertEqual(list((self.carpeta / "Archivos" / "Lecturas").glob("*.pdf")), [])

    def testAvisaSiFaltaElPdf(self):
        archivo = crearPdf(self.carpeta / "crc.pdf")
        lectura = self.gestor.agregarLectura("Tarjetas CRC", archivo)
        Path(self.gestor.obtenerRutaPdf(lectura["id"])).unlink()

        with self.assertRaises(FileNotFoundError):
            self.gestor.obtenerRutaPdf(lectura["id"])

    def testNoAbreUnPdfFueraDeLecturas(self):
        original = crearPdf(self.carpeta / "crc.pdf")
        lectura = self.gestor.agregarLectura("Tarjetas CRC", original)
        self.registros["lecturas"][lectura["id"]]["rutaArchivo"] = str(original)

        with self.assertRaises(ValueError):
            self.gestor.obtenerRutaPdf(lectura["id"])


if __name__ == "__main__":
    unittest.main()
