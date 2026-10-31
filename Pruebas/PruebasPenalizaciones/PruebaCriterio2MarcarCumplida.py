import unittest
from datetime import date
from Pruebas.PruebasPenalizaciones.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio2MarcarCumplida(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testMarcarComoCumplidaYaNoSeTomaEnCuenta(self):
        # Preparar: una penalización pendiente
        self.gestor.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        idPenalizacion = self.gestor.listarPenalizaciones()[0]["id"]

        # Ejecutar: traigo la fruta
        self.gestor.marcarComoCumplida(idPenalizacion)

        # Comprobar: queda cumplida y ya no tiene próxima clase pendiente
        penalizacion = self.gestor.listarPenalizaciones()[0]
        self.assertEqual(penalizacion["estado"], "Cumplida")
        self.assertEqual(penalizacion["proximaClase"], "-")


if __name__ == "__main__":
    unittest.main()