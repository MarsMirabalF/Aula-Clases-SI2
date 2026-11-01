import unittest
from copy import deepcopy

from Pruebas.PruebasApuntesLecturas.BaseDatosFalsa import (
    crearGestorConBaseFalsa,
    crearPdf,
)


class PruebaCriterio2GuardarEditarApuntes(unittest.TestCase):
    def setUp(self):
        self.gestor, self.registros, self.carpeta = crearGestorConBaseFalsa(self)
        self.lectura = self.gestor.agregarLectura(
            "Tarjetas CRC", crearPdf(self.carpeta / "crc.pdf")
        )

    def testGuardaElTextoYPermiteEditarElMismoApunte(self):
        apunte = self.gestor.registrarApunte(
            "Una clase tiene responsabilidades", "2026-10-27", self.lectura["id"]
        )

        editado = self.gestor.editarApunte(
            apunte["id"], "Responsabilidades y colaboradores", "2026-10-27", self.lectura["id"]
        )

        self.assertEqual(editado["id"], apunte["id"])
        guardados = self.gestor.apunte.listarApuntes()
        self.assertEqual(len(guardados), 1)
        self.assertEqual(guardados[0]["texto"], "Responsabilidades y colaboradores")

    def testRechazaTextosVaciosSinAlterarElApunteGuardado(self):
        apunte = self.gestor.registrarApunte(
            "Texto original", "2026-10-27", self.lectura["id"]
        )
        antes = deepcopy(self.registros)

        with self.assertRaises(ValueError):
            self.gestor.registrarApunte("  \n ", "2026-10-27", self.lectura["id"])
        with self.assertRaises(ValueError):
            self.gestor.editarApunte(apunte["id"], "", "2026-10-27", self.lectura["id"])

        self.assertEqual(self.registros, antes)

    def testEditarUnApunteInexistenteNoCreaUnoNuevo(self):
        with self.assertRaises(ValueError):
            self.gestor.editarApunte(
                "inexistente", "Texto", "2026-10-27", self.lectura["id"]
            )

        self.assertEqual(self.gestor.apunte.listarApuntes(), [])

    def testGuardarYEditarApuntesConservaLasPenalizaciones(self):
        penalizaciones = {"previa": {"estado": "Pendiente", "fechaTarde": "2026-10-27"}}
        self.registros["penalizaciones"] = deepcopy(penalizaciones)

        apunte = self.gestor.registrarApunte("Texto", "2026-10-27", self.lectura["id"])
        self.gestor.editarApunte(apunte["id"], "Texto nuevo", "2026-10-28", self.lectura["id"])

        self.assertEqual(self.registros["penalizaciones"], penalizaciones)


if __name__ == "__main__":
    unittest.main()
