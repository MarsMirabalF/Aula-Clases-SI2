import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio1MostrarPregunta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testMuestraUnaPreguntaDeLaClase(self):
        pregunta = self.gestor.obtenerPregunta()

        self.assertTrue(pregunta.obtenerPregunta())
        self.assertIn("UML", pregunta.obtenerPregunta())


if __name__ == "__main__":
    unittest.main()
