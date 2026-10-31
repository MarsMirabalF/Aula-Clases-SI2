import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio5MostrarEstado(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testUnaPenalizacionNuevaEstaPendiente(self):
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))

        penalizacion = self.gestor.listarPenalizaciones()[0]

        self.assertEqual(penalizacion["estado"], "Pendiente")

    def testUnaPenalizacionMarcadaEstaCumplida(self):
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        idPenalizacion = self.gestor.listarPenalizaciones()[0]["id"]

        self.gestor.marcarComoCumplida(idPenalizacion)

        penalizacion = self.gestor.listarPenalizaciones()[0]
        self.assertEqual(penalizacion["estado"], "Cumplida")


if __name__ == "__main__":
    unittest.main()