import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio1SoloDiasDeClase(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testNoSePenalizaUnDiaSinClase(self):
        # Preparar: un lunes no hay clase
        lunes = date(2026, 10, 26)

        # Ejecutar
        registrada = self.gestor.penalizacion.registrarLlegadaTarde(lunes)

        # Comprobar
        self.assertFalse(registrada)
        self.assertEqual(self.gestor.contarLlegadasTarde(), 0)

    def testSePenalizaMartesMiercolesYViernes(self):
        # Ejecutar
        martes = self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        miercoles = self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 28))
        viernes = self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 30))

        # Comprobar
        self.assertTrue(martes and miercoles and viernes)
        self.assertEqual(self.gestor.contarLlegadasTarde(), 3)


if __name__ == "__main__":
    unittest.main()