import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio5ContarPendientes(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testLasCumplidasCuentanEnElTotalPeroNoEnLasPendientes(self):
        # Preparar: 3 llegadas tarde, una ya cumplida
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 28))
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 30))
        primera = self.gestor.listarPenalizaciones()[0]
        self.gestor.marcarComoCumplida(primera["id"])

        # Ejecutar
        total = self.gestor.contarLlegadasTarde()
        pendientes = self.gestor.contarPendientes()

        # Comprobar
        self.assertEqual(total, 3)
        self.assertEqual(pendientes, 2)


if __name__ == "__main__":
    unittest.main()