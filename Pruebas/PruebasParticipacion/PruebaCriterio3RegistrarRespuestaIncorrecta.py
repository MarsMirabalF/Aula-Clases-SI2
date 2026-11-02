import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio3RegistrarRespuestaIncorrecta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testRegistraUnaRespuestaIncorrecta(self):
        pregunta = self.gestor.obtenerPregunta(1)

        self.gestor.registrarParticipacion(pregunta, False)

        participacion = self.gestor.listarParticipaciones()[0]
        self.assertEqual(participacion["resultado"], "Incorrecta")
        self.assertFalse(participacion["esCorrecta"])


if __name__ == "__main__":
    unittest.main()
