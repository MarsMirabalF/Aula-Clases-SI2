import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio3NaceConEstadoPendiente(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testUnaPenalizacionNuevaEstaPendiente(self):
        # Preparar y ejecutar
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))

        # Comprobar
        penalizacion = self.gestor.listarPenalizaciones()[0]
        self.assertEqual(penalizacion["estado"], "Pendiente")


if __name__ == "__main__":
    unittest.main()