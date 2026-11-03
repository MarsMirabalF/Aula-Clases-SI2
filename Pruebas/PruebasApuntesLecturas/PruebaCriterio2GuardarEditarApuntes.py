import unittest

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio2GuardarEditarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, _ = crearGestorConBaseFalsa(self)
        self.registros["lecturas"] = {"crc": {"titulo": "Tarjetas CRC"}}

    def testGuardaYEditaElTextoDelApunte(self):
        apunte = self.gestor.registrarApunte("Responsabilidades", "2026-10-27", "crc")
        self.assertEqual(self.gestor.listarApuntes()[0]["texto"], "Responsabilidades")

        self.gestor.editarApunte(apunte["id"], "Colaboradores", "2026-10-27", "crc")

        apuntes = self.gestor.listarApuntes()
        self.assertEqual(len(apuntes), 1)
        self.assertEqual(apuntes[0]["id"], apunte["id"])
        self.assertEqual(apuntes[0]["texto"], "Colaboradores")

    def testRechazaTextoVacioAlGuardarYEditar(self):
        apunte = self.gestor.registrarApunte("Responsabilidades", "2026-10-27", "crc")

        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("  ", "2026-10-27", "crc")
        with self.assertRaises(ValueError):
            self.gestor.editarApunte(apunte["id"], "", "2026-10-27", "crc")

        self.assertEqual(self.gestor.apunte.listarApuntes(), [apunte])


if __name__ == "__main__":
    unittest.main()
