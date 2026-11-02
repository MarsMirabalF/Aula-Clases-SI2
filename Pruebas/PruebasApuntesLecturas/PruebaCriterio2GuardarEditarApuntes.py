import unittest

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa, crearPdf


class PruebaCriterio2GuardarEditarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        archivo = crearPdf(self.carpeta / "crc.pdf")
        self.lectura = self.gestor.agregarLectura("Tarjetas CRC", archivo)

    def testGuardaElTextoDelApunte(self):
        self.gestor.registrarApunte("Una clase tiene responsabilidades", "2026-10-27", self.lectura["id"])

        apuntes = self.gestor.listarApuntes()

        self.assertEqual(len(apuntes), 1)
        self.assertEqual(apuntes[0]["texto"], "Una clase tiene responsabilidades")

    def testEditaElTextoDelApunte(self):
        apunte = self.gestor.registrarApunte(
            "Una clase tiene responsabilidades", "2026-10-27", self.lectura["id"])

        editado = self.gestor.editarApunte(
            apunte["id"], "Responsabilidades y colaboradores", "2026-10-27", self.lectura["id"])

        apuntes = self.gestor.listarApuntes()
        self.assertEqual(editado["id"], apunte["id"])
        self.assertEqual(len(apuntes), 1)
        self.assertEqual(apuntes[0]["id"], apunte["id"])
        self.assertEqual(apuntes[0]["texto"], "Responsabilidades y colaboradores")

    def testNoGuardaUnTextoVacio(self):
        apunte = self.gestor.registrarApunte(
            "Responsabilidades de la clase", "2026-10-27", self.lectura["id"])

        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("  \n ", "2026-10-27", self.lectura["id"])

        self.assertEqual(self.gestor.apunte.listarApuntes(), [apunte])

    def testNoEditaConTextoVacio(self):
        apunte = self.gestor.registrarApunte(
            "Responsabilidades de la clase", "2026-10-27", self.lectura["id"])

        with self.assertRaises(ValueError):
            self.gestor.editarApunte(apunte["id"], "", "2026-10-27", self.lectura["id"])

        self.assertEqual(self.gestor.apunte.listarApuntes(), [apunte])

    def testNoEditaUnApunteQueNoExiste(self):
        with self.assertRaises(ValueError):
            self.gestor.editarApunte("inexistente", "Resumen de CRC", "2026-10-27", self.lectura["id"])

        self.assertEqual(self.gestor.listarApuntes(), [])

    def testNoCambiaLasPenalizaciones(self):
        penalizacion = {"estado": "Pendiente", "fechaTarde": "2026-10-27"}
        self.registros["penalizaciones"] = {"id1": penalizacion.copy()}

        apunte = self.gestor.registrarApunte("Responsabilidades", "2026-10-27", self.lectura["id"])
        self.gestor.editarApunte(
            apunte["id"], "Responsabilidades y colaboradores", "2026-10-28", self.lectura["id"])

        self.assertEqual(self.registros["penalizaciones"], {"id1": penalizacion})


if __name__ == "__main__":
    unittest.main()
