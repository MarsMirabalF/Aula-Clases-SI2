import unittest

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import (
    crearGestorConBaseFalsa,
    crearPdf,
)


class PruebaCriterio4OrganizarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        self.lecturaB = self.gestor.agregarLectura("Beta", crearPdf(self.carpeta / "beta.pdf"))
        self.lecturaA = self.gestor.agregarLectura("Alfa", crearPdf(self.carpeta / "alfa.pdf"))
        self.antiguo = self.gestor.registrarApunte("Anterior", "2026-10-20", self.lecturaA["id"])
        self.actualB = self.gestor.registrarApunte("De Beta", "2026-10-27", self.lecturaB["id"])
        self.actualA = self.gestor.registrarApunte("De Alfa", "2026-10-27", self.lecturaA["id"])

    def testOrdenaPorFechaRecienteYPorLecturaDentroDeCadaFecha(self):
        apuntes = self.gestor.listarApuntes()

        self.assertEqual(
            [apunte["id"] for apunte in apuntes],
            [self.actualA["id"], self.actualB["id"], self.antiguo["id"]],
        )
        self.assertEqual([lectura["titulo"] for lectura in self.gestor.listarLecturas()], ["Alfa", "Beta"])

    def testFiltraPorFechaOPorLectura(self):
        porFecha = self.gestor.listarApuntes(fechaClase="2026-10-27")
        porLectura = self.gestor.listarApuntes(idLectura=self.lecturaA["id"])

        self.assertEqual({apunte["id"] for apunte in porFecha}, {self.actualA["id"], self.actualB["id"]})
        self.assertEqual({apunte["id"] for apunte in porLectura}, {self.actualA["id"], self.antiguo["id"]})

    def testCombinaLosFiltrosDeFechaYLectura(self):
        apuntes = self.gestor.listarApuntes(fechaClase="2026-10-27", idLectura=self.lecturaA["id"])

        self.assertEqual([apunte["id"] for apunte in apuntes], [self.actualA["id"]])
        self.assertEqual(
            self.gestor.listarApuntes(fechaClase="2026-10-21", idLectura=self.lecturaA["id"]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
