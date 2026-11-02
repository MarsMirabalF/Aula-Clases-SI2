import unittest
from datetime import datetime
from modelos.Tarea import Tarea
from Pruebas.PruebasTareas.BaseDatosFalsa import usarBaseFalsa


class PruebaCriterio1RegistrarTarea(unittest.TestCase):
    def setUp(self):
        usarBaseFalsa(self)

    def testRegistraNumeroTemaYHoraLimite(self):
        Tarea(3, "Diagrama de clases", "2026-11-03 23:59").guardar()

        tarea = Tarea.listarTareas()[0]

        self.assertEqual(tarea.numero, 3)
        self.assertEqual(tarea.tema, "Diagrama de clases")
        self.assertEqual(tarea.horaLimite, datetime(2026, 11, 3, 23, 59))

    def testNoRegistraDosTareasConElMismoNumero(self):
        Tarea(3, "Diagrama de clases", "2026-11-03 23:59").guardar()

        with self.assertRaises(ValueError):
            Tarea(3, "Casos de uso", "2026-11-05 23:59").guardar()


if __name__ == "__main__":
    unittest.main()
