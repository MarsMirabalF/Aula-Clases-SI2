import unittest
from datetime import datetime
from unittest.mock import patch
from modelos.RedireccionCorreo import RedireccionCorreo
from modelos.Tarea import Tarea
from Pruebas.PruebasTareas.BaseDatosFalsa import usarBaseFalsa


class PruebaCriterio3RedireccionarCorreo(unittest.TestCase):
    def setUp(self):
        usarBaseFalsa(self)

    def testGeneraElAsuntoConNumeroYTema(self):
        tarea = Tarea(3, "Diagrama de clases", "2026-11-03 23:59")

        asunto = RedireccionCorreo().generarAsunto(tarea)

        self.assertEqual(asunto, "Tarea 3 - Diagrama de clases")

    @patch("webbrowser.open")
    def testAbreElCorreoDelIngenieroConElAsunto(self, abrirNavegador):
        tarea = Tarea(3, "Diagrama de clases", "2026-11-03 23:59")

        RedireccionCorreo().abrirCorreo(tarea, datetime(2026, 11, 3, 20, 0))

        url = abrirNavegador.call_args[0][0]
        self.assertIn("to=j.flores%40umss.edu.bo", url)
        self.assertIn("su=Tarea+3+-+Diagrama+de+clases", url)


if __name__ == "__main__":
    unittest.main()
