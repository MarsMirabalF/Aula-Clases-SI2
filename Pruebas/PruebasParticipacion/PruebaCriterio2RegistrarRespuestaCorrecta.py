import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio2RegistrarRespuestaCorrecta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testRegistraUnaRespuestaCorrecta(self):
        pregunta = self.gestor.obtenerPregunta()

        self.gestor.registrarParticipacion(pregunta, True)

        participacion = self.gestor.listarParticipaciones()[0]
        self.assertEqual(participacion["pregunta"], pregunta.obtenerPregunta())
        self.assertTrue(participacion["esCorrecta"])


if __name__ == "__main__":
    unittest.main()
