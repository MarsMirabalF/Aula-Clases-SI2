import unittest
from copy import deepcopy
from datetime import date

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import (
    crearGestorConBaseFalsa,
    crearPdf,
)


class PruebaCriterio3AsociarFechaLectura(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        self.lectura = self.gestor.agregarLectura(
            "Diseño de clases", crearPdf(self.carpeta / "clases.pdf")
        )

    def testAsociaElApunteConSuFechaYLectura(self):
        apunte = self.gestor.registrarApunte(
            "Mi resumen", date(2026, 10, 27), self.lectura["id"]
        )

        self.assertEqual(apunte["fechaClase"], "2026-10-27")
        self.assertEqual(apunte["idLectura"], self.lectura["id"])
        mostrado = self.gestor.listarApuntes()[0]
        self.assertEqual(mostrado["tituloLectura"], "Diseño de clases")
        self.assertEqual(mostrado["diaClase"], "Martes")

    def testPermiteCambiarLaFechaYLaLecturaDeUnApunte(self):
        segunda = self.gestor.agregarLectura(
            "Colaboraciones", crearPdf(self.carpeta / "colaboraciones.pdf")
        )
        apunte = self.gestor.registrarApunte("Resumen", "2026-10-27", self.lectura["id"])

        self.gestor.editarApunte(apunte["id"], "Resumen", date(2026, 10, 29), segunda["id"])

        guardado = self.gestor.listarApuntes()[0]
        self.assertEqual(guardado["fechaClase"], "2026-10-29")
        self.assertEqual(guardado["idLectura"], segunda["id"])
        self.assertEqual(guardado["tituloLectura"], "Colaboraciones")
        self.assertEqual(guardado["diaClase"], "Jueves")

    def testRechazaFechasInvalidasYLecturasInexistentesSinGuardar(self):
        antes = deepcopy(self.registros)
        casos = [
            ("2026-02-30", self.lectura["id"]),
            ("fecha", self.lectura["id"]),
            ("", self.lectura["id"]),
            ("2026-10-27", "inexistente"),
            ("2026-10-27", ""),
        ]

        for fecha, idLectura in casos:
            with self.subTest(fecha=fecha, idLectura=idLectura):
                with self.assertRaises(ValueError):
                    self.gestor.registrarApunte("Resumen", fecha, idLectura)

        self.assertEqual(self.registros, antes)


if __name__ == "__main__":
    unittest.main()
