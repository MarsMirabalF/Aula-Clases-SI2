import unittest
from datetime import date

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa, crearPdf


class PruebaCriterio3AsociarFechaLectura(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        archivo = crearPdf(self.carpeta / "crc.pdf")
        self.lectura = self.gestor.agregarLectura("Tarjetas CRC", archivo)

    def testAsociaLaFechaYLaLectura(self):
        apunte = self.gestor.registrarApunte(
            "Una clase tiene responsabilidades", date(2026, 10, 27), self.lectura["id"])

        self.assertEqual(apunte["fechaClase"], "2026-10-27")
        self.assertEqual(apunte["idLectura"], self.lectura["id"])
        mostrado = self.gestor.listarApuntes()[0]
        self.assertEqual(mostrado["tituloLectura"], "Tarjetas CRC")
        self.assertEqual(mostrado["diaClase"], "Martes")

    def testCambiaLaFechaYLaLectura(self):
        archivo = crearPdf(self.carpeta / "clases.pdf")
        segunda = self.gestor.agregarLectura("Diagrama de clases", archivo)
        apunte = self.gestor.registrarApunte("Resumen", "2026-10-27", self.lectura["id"])

        self.gestor.editarApunte(apunte["id"], "Resumen", date(2026, 10, 29), segunda["id"])

        guardado = self.gestor.listarApuntes()[0]
        self.assertEqual(guardado["fechaClase"], "2026-10-29")
        self.assertEqual(guardado["idLectura"], segunda["id"])
        self.assertEqual(guardado["tituloLectura"], "Diagrama de clases")
        self.assertEqual(guardado["diaClase"], "Jueves")

    def testNoGuardaConUnaFechaImposible(self):
        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("Resumen", "2026-02-30", self.lectura["id"])

        self.assertEqual(self.gestor.listarApuntes(), [])

    def testNoGuardaConUnaFechaInvalida(self):
        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("Resumen", "fecha", self.lectura["id"])

        self.assertEqual(self.gestor.listarApuntes(), [])

    def testNoGuardaSinFecha(self):
        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("Resumen", "", self.lectura["id"])

        self.assertEqual(self.gestor.listarApuntes(), [])

    def testNoGuardaConUnaLecturaInexistente(self):
        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("Resumen", "2026-10-27", "inexistente")

        self.assertEqual(self.gestor.listarApuntes(), [])

    def testNoGuardaSinLectura(self):
        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("Resumen", "2026-10-27", "")

        self.assertEqual(self.gestor.listarApuntes(), [])


if __name__ == "__main__":
    unittest.main()
