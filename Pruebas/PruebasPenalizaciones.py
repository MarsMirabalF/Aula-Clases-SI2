import unittest
from datetime import date
from unittest.mock import patch

from Modelos.GestorPenalizaciones import GestorPenalizaciones


class ReferenciaFalsa:
    def __init__(self, baseDatos, ruta):
        self.baseDatos = baseDatos
        self.ruta = ruta

    def get(self):
        return dict(self.baseDatos.registros) or None

    def push(self, datos):
        self.baseDatos.contador += 1
        self.baseDatos.registros["id" + str(self.baseDatos.contador)] = datos

    def update(self, datos):
        idPenalizacion = self.ruta.split("/")[1]
        self.baseDatos.registros[idPenalizacion].update(datos)


class BaseDatosFalsa:
    def __init__(self):
        self.registros = {}
        self.contador = 0

    def reference(self, ruta):
        return ReferenciaFalsa(self, ruta)


class PruebasPenalizaciones(unittest.TestCase):
    def setUp(self):
        self.baseDatos = BaseDatosFalsa()
        parche = patch("firebase_admin.db.reference", side_effect=self.baseDatos.reference)
        parche.start()
        self.addCleanup(parche.stop)
        self.gestorPenalizaciones = GestorPenalizaciones()

    # Criterio 1: Mostrar el día que llegué tarde (martes, miércoles o viernes)
    def testMostrarDiaQueLlegueTarde(self):
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 21))
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 23))

        dias = [penalizacion["diaTarde"]
                for penalizacion in self.gestorPenalizaciones.listarPenalizaciones()]

        self.assertEqual(dias, ["Miércoles", "Viernes", "Martes"])

    # Criterio 2: Marcar como cumplida y que ese día ya no se tome en cuenta
    def testMarcarComoCumplidaYaNoSeTomaEnCuenta(self):
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))
        idPenalizacion = self.gestorPenalizaciones.listarPenalizaciones()[0]["id"]

        self.gestorPenalizaciones.marcarComoCumplida(idPenalizacion)

        penalizacion = self.gestorPenalizaciones.listarPenalizaciones()[0]
        self.assertEqual(penalizacion["estado"], "Cumplida")
        self.assertEqual(penalizacion["proximaClase"], "-")

    # Criterio 3: Ver cuántas veces he llegado tarde
    def testContarVecesQueLlegueTarde(self):
        self.assertEqual(self.gestorPenalizaciones.contarLlegadasTarde(), 0)

        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 21))
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 23))
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))

        self.assertEqual(self.gestorPenalizaciones.contarLlegadasTarde(), 3)

    # Criterio 4: Mostrar la fecha y el día de la siguiente clase en la que debo llevar fruta
    def testMostrarFechaYDiaDeLaSiguienteClase(self):
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 27))  # martes
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 21))  # miércoles
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 30))  # viernes

        proximasClases = [penalizacion["proximaClase"]
                          for penalizacion in self.gestorPenalizaciones.listarPenalizaciones()]

        self.assertEqual(proximasClases, [
            "Viernes 2026-10-23",
            "Miércoles 2026-10-28",
            "Martes 2026-11-03",
        ])

    # Criterio 5: Mostrar el estado (Pendiente / Cumplida)
    def testMostrarEstadoPendienteYCumplida(self):
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 21))
        self.gestorPenalizaciones.penalizacion.registrarLlegadaTarde(date(2026, 10, 23))
        primerId = self.gestorPenalizaciones.listarPenalizaciones()[0]["id"]

        self.gestorPenalizaciones.marcarComoCumplida(primerId)

        estados = [penalizacion["estado"]
                   for penalizacion in self.gestorPenalizaciones.listarPenalizaciones()]
        self.assertEqual(estados, ["Cumplida", "Pendiente"])


if __name__ == "__main__":
    unittest.main()