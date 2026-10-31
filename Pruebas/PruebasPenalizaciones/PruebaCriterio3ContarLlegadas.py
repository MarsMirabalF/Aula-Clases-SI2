import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio3ContarLlegadas(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testCuentaLasVecesQueLlegueTarde(self):
        # Preparar: llego tarde 3 veces
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 21))
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 23))
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))

        # Ejecutar
        total = self.gestor.contarLlegadasTarde()

        # Comprobar
        self.assertEqual(total, 3)


if __name__ == "__main__":
    unittest.main()