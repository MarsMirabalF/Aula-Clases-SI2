import unittest

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio4OrganizarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, _ = crearGestorConBaseFalsa(self)
        self.registros["lecturas"] = {
            "crc": {"titulo": "Tarjetas CRC"}, "clases": {"titulo": "Diagrama de clases"}}
        self.anterior = self.gestor.registrarApunte("Relaciones", "2026-10-20", "clases")
        self.crc = self.gestor.registrarApunte("Responsabilidades", "2026-10-27", "crc")
        self.clases = self.gestor.registrarApunte("Herencia", "2026-10-27", "clases")

    def testOrdenaPorFechaYLectura(self):
        apuntes = self.gestor.listarApuntes()
        lecturas = self.gestor.listarLecturas()

        self.assertEqual([apunte["id"] for apunte in apuntes],
                         [self.clases["id"], self.crc["id"], self.anterior["id"]])
        self.assertEqual([lectura["titulo"] for lectura in lecturas],
                         ["Diagrama de clases", "Tarjetas CRC"])

    def testFiltraPorFecha(self):
        apuntes = self.gestor.listarApuntes(fechaClase="2026-10-27")
        self.assertEqual([apunte["id"] for apunte in apuntes],
                         [self.clases["id"], self.crc["id"]])

    def testFiltraPorLectura(self):
        apuntes = self.gestor.listarApuntes(idLectura="clases")
        self.assertEqual([apunte["id"] for apunte in apuntes],
                         [self.clases["id"], self.anterior["id"]])

    def testCombinaFechaYLectura(self):
        apuntes = self.gestor.listarApuntes(fechaClase="2026-10-27", idLectura="clases")
        self.assertEqual(len(apuntes), 1)
        self.assertEqual(apuntes[0]["id"], self.clases["id"])

    def testNoMuestraApuntesDeOtraFecha(self):
        self.assertEqual(self.gestor.listarApuntes(fechaClase="2026-10-21"), [])


if __name__ == "__main__":
    unittest.main()
