import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio4ProximaClase(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testMuestraFechaYDiaDeLaSiguienteClase(self):
        # Preparar: llego tarde el viernes 30 de octubre
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 30))

        # Ejecutar
        penalizacion = self.gestor.listarPenalizaciones()[0]

        # Comprobar: la siguiente clase es el martes 3 de noviembre
        self.assertEqual(penalizacion["proximaClase"], "Martes 2026-11-03")


if __name__ == "__main__":
    unittest.main()