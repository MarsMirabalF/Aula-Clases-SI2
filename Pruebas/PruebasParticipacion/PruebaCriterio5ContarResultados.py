import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio5ContarResultados(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testCuentaRespuestasCorrectasEIncorrectas(self):
        pregunta = self.gestor.obtenerPregunta()
        self.gestor.registrarParticipacion(pregunta, True)
        self.gestor.registrarParticipacion(pregunta, True)
        self.gestor.registrarParticipacion(pregunta, False)

        self.assertEqual(self.gestor.contarCorrectas(), 2)
        self.assertEqual(self.gestor.contarIncorrectas(), 1)


if __name__ == "__main__":
    unittest.main()
