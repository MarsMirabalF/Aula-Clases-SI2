import unittest

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa, crearPdf


class PruebaCriterio4OrganizarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        archivoCRC = crearPdf(self.carpeta / "crc.pdf")
        archivoClases = crearPdf(self.carpeta / "clases.pdf")
        self.lecturaCRC = self.gestor.agregarLectura("Tarjetas CRC", archivoCRC)
        self.lecturaClases = self.gestor.agregarLectura("Diagrama de clases", archivoClases)
        self.anterior = self.gestor.registrarApunte(
            "Relaciones entre clases", "2026-10-20", self.lecturaClases["id"])
        self.apunteCRC = self.gestor.registrarApunte(
            "Responsabilidades de una clase", "2026-10-27", self.lecturaCRC["id"])
        self.apunteClases = self.gestor.registrarApunte(
            "Asociaciones y herencia", "2026-10-27", self.lecturaClases["id"])

    def testOrdenaPorFechaYLectura(self):
        apuntes = self.gestor.listarApuntes()

        self.assertEqual(len(apuntes), 3)
        self.assertEqual(apuntes[0]["id"], self.apunteClases["id"])
        self.assertEqual(apuntes[1]["id"], self.apunteCRC["id"])
        self.assertEqual(apuntes[2]["id"], self.anterior["id"])

    def testOrdenaLasLecturasPorTitulo(self):
        lecturas = self.gestor.listarLecturas()

        self.assertEqual(len(lecturas), 2)
        self.assertEqual(lecturas[0]["titulo"], "Diagrama de clases")
        self.assertEqual(lecturas[1]["titulo"], "Tarjetas CRC")

    def testFiltraPorFecha(self):
        apuntes = self.gestor.listarApuntes(fechaClase="2026-10-27")

        self.assertEqual(len(apuntes), 2)
        self.assertEqual(apuntes[0]["id"], self.apunteClases["id"])
        self.assertEqual(apuntes[1]["id"], self.apunteCRC["id"])

    def testFiltraPorLectura(self):
        apuntes = self.gestor.listarApuntes(idLectura=self.lecturaClases["id"])

        self.assertEqual(len(apuntes), 2)
        self.assertEqual(apuntes[0]["id"], self.apunteClases["id"])
        self.assertEqual(apuntes[1]["id"], self.anterior["id"])

    def testCombinaFechaYLectura(self):
        apuntes = self.gestor.listarApuntes(
            fechaClase="2026-10-27", idLectura=self.lecturaClases["id"])

        self.assertEqual(len(apuntes), 1)
        self.assertEqual(apuntes[0]["id"], self.apunteClases["id"])

    def testNoMuestraApuntesSiNoCoincideLaFecha(self):
        apuntes = self.gestor.listarApuntes(
            fechaClase="2026-10-21", idLectura=self.lecturaClases["id"])

        self.assertEqual(apuntes, [])


if __name__ == "__main__":
    unittest.main()
