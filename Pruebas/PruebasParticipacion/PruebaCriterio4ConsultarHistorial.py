import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio4ConsultarHistorial(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testConsultaLasParticipacionesRealizadas(self):
        primera = self.gestor.obtenerPregunta(0)
        segunda = self.gestor.obtenerPregunta(1)
        self.gestor.registrarParticipacion(primera, True)
        self.gestor.registrarParticipacion(segunda, False)

        historial = self.gestor.listarParticipaciones()

        self.assertEqual(len(historial), 2)
        self.assertEqual({registro["resultado"] for registro in historial},
                         {"Correcta", "Incorrecta"})
        self.assertTrue(all(registro["fecha"] for registro in historial))


if __name__ == "__main__":
    unittest.main()
