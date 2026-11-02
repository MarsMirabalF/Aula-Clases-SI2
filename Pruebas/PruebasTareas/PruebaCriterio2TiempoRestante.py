import unittest
from datetime import datetime, timedelta
from modelos.Tarea import Tarea


class PruebaCriterio2TiempoRestante(unittest.TestCase):
    def testCalculaElTiempoQueFaltaParaLaHoraLimite(self):
        tarea = Tarea(1, "Historias de usuario", "2026-11-03 10:00")

        restante = tarea.calcularTiempoRestante(datetime(2026, 11, 3, 8, 30))

        self.assertEqual(restante, timedelta(hours=1, minutes=30))


if __name__ == "__main__":
    unittest.main()
