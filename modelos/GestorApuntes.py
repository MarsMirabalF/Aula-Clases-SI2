from modelos.Apunte import Apunte, convertirFechaClase
from modelos.HorarioClases import HorarioClases
from modelos.Lectura import Lectura


class GestorApuntes:
    def __init__(self, carpetaProyecto=None):
        self.lectura = Lectura(carpetaProyecto)
        self.apunte = Apunte()
        self.horarioClases = HorarioClases()

    def agregarLectura(self, titulo, rutaPdf):
        return self.lectura.agregarLectura(titulo, rutaPdf)

    def listarLecturas(self):
        return self.lectura.listarLecturas()

    def obtenerRutaPdf(self, idLectura):
        return self.lectura.obtenerRutaPdf(idLectura)

    def registrarApunte(self, texto, fechaClase, idLectura):
        return self.apunte.registrarApunte(texto, fechaClase, idLectura)

    def editarApunte(self, idApunte, texto, fechaClase, idLectura):
        return self.apunte.editarApunte(idApunte, texto, fechaClase, idLectura)

    def listarApuntes(self, fechaClase=None, idLectura=None):
        fechaFiltro = convertirFechaClase(fechaClase) if fechaClase is not None else None
        titulos = {lectura["id"]: lectura["titulo"] for lectura in self.listarLecturas()}
        lista = []
        for apunte in self.apunte.listarApuntes():
            fecha = convertirFechaClase(apunte["fechaClase"])
            if fechaFiltro is not None and fecha != fechaFiltro:
                continue
            if idLectura is not None and apunte["idLectura"] != idLectura:
                continue
            lista.append({**apunte,
                          "tituloLectura": titulos.get(apunte["idLectura"], "Lectura no disponible"),
                          "diaClase": self.horarioClases.obtenerNombreDia(fecha)})
        return sorted(lista, key=lambda apunte: (-convertirFechaClase(apunte["fechaClase"]).toordinal(),
                                                 apunte["tituloLectura"].casefold(), apunte["id"]))
