from modelos.Apunte import Apunte, convertirFechaClase
from modelos.HorarioClases import HorarioClases
from modelos.Lectura import Lectura, validarId


class GestorApuntes:
    def __init__(self, carpetaProyecto=None):
        self.lectura = Lectura(carpetaProyecto)
        self.apunte = Apunte(self.lectura)
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
        if idLectura is not None:
            validarId(idLectura, "una lectura")
        lecturas = {lectura["id"]: lectura for lectura in self.listarLecturas()}
        lista = []
        for apunte in self.apunte.listarApuntes():
            fecha = convertirFechaClase(apunte["fechaClase"])
            if fechaFiltro is not None and fecha != fechaFiltro:
                continue
            if idLectura is not None and apunte["idLectura"] != idLectura:
                continue
            lectura = lecturas.get(apunte["idLectura"])
            lista.append({**apunte,
                          "tituloLectura": lectura["titulo"] if lectura else "Lectura no disponible",
                          "diaClase": self.horarioClases.obtenerNombreDia(fecha)})
        return sorted(lista, key=lambda apunte: (-convertirFechaClase(apunte["fechaClase"]).toordinal(),
                                                 apunte["tituloLectura"].casefold(), apunte["id"]))
