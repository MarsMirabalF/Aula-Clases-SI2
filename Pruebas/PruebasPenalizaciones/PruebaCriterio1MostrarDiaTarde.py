import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio1MostrarDiaTarde(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testMuestraElDiaQueLlegueTarde(self):
        # Preparar: llego tarde un martes
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))

        # Ejecutar
        penalizacion = self.gestor.listarPenalizaciones()[0]

        # Comprobar
        self.assertEqual(penalizacion["diaTarde"], "Martes")


if __name__ == "__main__":
    unittest.main()