import unittest
from datetime import datetime
from modelos.RedireccionCorreo import RedireccionCorreo
from modelos.Tarea import Tarea


class PruebaCriterio4AvisoRetraso(unittest.TestCase):
    def setUp(self):
        self.tarea = Tarea(2, "Tarjetas CRC", "2026-11-03 10:00")

    def testMuestraElAvisoSiYaPasoLaHoraLimite(self):
        aviso = RedireccionCorreo().mostrarAvisoRetraso(self.tarea, datetime(2026, 11, 3, 10, 5))

        self.assertEqual(aviso, "Entrega con retraso")

    def testNoMuestraAvisoSiEntregoATiempo(self):
        aviso = RedireccionCorreo().mostrarAvisoRetraso(self.tarea, datetime(2026, 11, 3, 9, 0))

        self.assertEqual(aviso, "")


if __name__ == "__main__":
    unittest.main()
