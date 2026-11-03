import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio4CumplirPenalizacion(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testCumplirDejaDeTomarlaEnCuentaYNoAfectaLasDemas(self):
        # Preparar: dos penalizaciones pendientes
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 28))
        primera = self.gestor.listarPenalizaciones()[0]

        # Ejecutar: traigo la fruta de la primera
        self.gestor.marcarComoCumplida(primera["id"])

        # Comprobar
        primera, segunda = self.gestor.listarPenalizaciones()
        self.assertEqual(primera["estado"], "Cumplida")
        self.assertEqual(primera["proximaClase"], "-")
        self.assertEqual(segunda["estado"], "Pendiente")


if __name__ == "__main__":
    unittest.main()