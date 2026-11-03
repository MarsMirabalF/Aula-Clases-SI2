import unittest
from datetime import date
from modelos.HorarioClases import HorarioClases


class PruebaCriterio2ProximaClase(unittest.TestCase):
    def setUp(self):
        self.horarioClases = HorarioClases()

    def testDespuesDelMartesVieneElMiercoles(self):
        proxima = self.horarioClases.calcularProximaClase(date(2026, 10, 27))
        self.assertEqual(proxima, date(2026, 10, 28))

    def testDespuesDelMiercolesVieneElViernes(self):
        proxima = self.horarioClases.calcularProximaClase(date(2026, 10, 28))
        self.assertEqual(proxima, date(2026, 10, 30))

    def testDespuesDelViernesVieneElMartesSiguiente(self):
        proxima = self.horarioClases.calcularProximaClase(date(2026, 10, 30))
        self.assertEqual(proxima, date(2026, 11, 3))


if __name__ == "__main__":
    unittest.main()