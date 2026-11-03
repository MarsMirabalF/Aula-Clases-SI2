import unittest
from datetime import date

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio3AsociarFechaLectura(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, _ = crearGestorConBaseFalsa(self)
        self.registros["lecturas"] = {
            "crc": {"titulo": "Tarjetas CRC"}, "clases": {"titulo": "Diagrama de clases"}}

    def testAsociaYCambiaLaFechaYLaLectura(self):
        apunte = self.gestor.registrarApunte("Resumen", date(2026, 10, 27), "crc")
        guardado = self.gestor.listarApuntes()[0]
        self.assertEqual(guardado["fechaClase"], "2026-10-27")
        self.assertEqual(guardado["idLectura"], "crc")
        self.assertEqual(guardado["tituloLectura"], "Tarjetas CRC")
        self.assertEqual(guardado["diaClase"], "Martes")

        self.gestor.editarApunte(apunte["id"], "Resumen", "2026-10-29", "clases")

        editado = self.gestor.listarApuntes()[0]
        self.assertEqual(editado["fechaClase"], "2026-10-29")
        self.assertEqual(editado["idLectura"], "clases")
        self.assertEqual(editado["tituloLectura"], "Diagrama de clases")
        self.assertEqual(editado["diaClase"], "Jueves")

    def testRechazaFechaOLecturaInvalida(self):
        for fecha, lectura in (("2026-02-30", "crc"), ("", "crc"),
                               ("2026-10-27", "inexistente"), ("2026-10-27", "")):
            with self.subTest(fecha=fecha, lectura=lectura):
                with self.assertRaises(ValueError):
                    self.gestor.registrarApunte("Resumen", fecha, lectura)
                self.assertEqual(self.gestor.listarApuntes(), [])


if __name__ == "__main__":
    unittest.main()
