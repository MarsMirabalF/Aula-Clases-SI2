import unittest
from pathlib import Path

import pymupdf

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa, crearPdf


class PruebaCriterio1ImportarVerPdf(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)

    def testImportaYConservaUnaCopiaDelPdf(self):
        original = crearPdf(self.carpeta / "crc.pdf")

        lectura = self.gestor.agregarLectura("Tarjetas CRC", original)
        original.unlink()

        ruta = Path(self.gestor.obtenerRutaPdf(lectura["id"]))
        self.assertEqual(ruta.parent, self.carpeta / "Archivos" / "Lecturas")
        self.assertEqual(self.gestor.listarLecturas()[0]["titulo"], "Tarjetas CRC")
        with pymupdf.open(ruta) as documento:
            self.assertEqual(documento.page_count, 1)
            self.assertIn("Lectura de prueba", documento[0].get_text())

    def testRechazaArchivosQueNoSonPdf(self):
        for nombre in ("texto.txt", "danado.pdf"):
            with self.subTest(archivo=nombre):
                archivo = self.carpeta / nombre
                archivo.write_text("Esto no es un PDF", encoding="utf-8")
                with self.assertRaises(ValueError):
                    self.gestor.agregarLectura("Tarjetas CRC", archivo)
                self.assertEqual(self.gestor.listarLecturas(), [])


if __name__ == "__main__":
    unittest.main()
