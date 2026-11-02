import unittest
from datetime import datetime
from modelos.HistorialEntregas import HistorialEntregas
from modelos.Tarea import Tarea
from Pruebas.PruebasTareas.BaseDatosFalsa import usarBaseFalsa


class PruebaCriterio5HistorialEntregas(unittest.TestCase):
    def setUp(self):
        usarBaseFalsa(self)
        self.historial = HistorialEntregas()

    def testGuardaLaFechaYHoraDeLaEntrega(self):
        tarea = Tarea(1, "Historias de usuario", "2026-11-03 10:00")

        self.historial.guardar(tarea, datetime(2026, 11, 3, 8, 30))

        entrega = self.historial.mostrarEntregas()[0]
        self.assertEqual(entrega["fecha"], "03/11/2026 08:30")
        self.assertEqual(entrega["estado"], "A tiempo")

    def testCuentaEntregasATiempoYConRetraso(self):
        self.historial.guardar(Tarea(1, "Historias", "2026-11-03 10:00"), datetime(2026, 11, 3, 9, 0))
        self.historial.guardar(Tarea(2, "CRC", "2026-11-04 10:00"), datetime(2026, 11, 4, 11, 0))

        self.assertEqual(self.historial.mostrarATiempoYRetraso(), (1, 1))


if __name__ == "__main__":
    unittest.main()
