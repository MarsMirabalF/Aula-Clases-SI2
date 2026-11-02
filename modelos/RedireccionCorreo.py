import webbrowser
from urllib.parse import urlencode

from modelos.HistorialEntregas import HistorialEntregas

CORREO_INGENIERO = "j.flores@umss.edu.bo"
URL_GMAIL = "https://mail.google.com/mail/?"


class RedireccionCorreo:
    def __init__(self, historialEntregas=None):
        self.correoIngeniero = CORREO_INGENIERO
        self.asunto = ""
        self.historialEntregas = historialEntregas or HistorialEntregas()

    def generarAsunto(self, tarea):
        self.asunto = "Tarea " + str(tarea.numero) + " - " + tarea.tema
        return self.asunto

    def mostrarAvisoRetraso(self, tarea, ahora=None):
        return "Entrega con retraso" if tarea.estaAtrasada(ahora) else ""

    def abrirCorreo(self, tarea, ahora=None):
        self.generarAsunto(tarea)
        self.historialEntregas.guardar(tarea, ahora)
        webbrowser.open(URL_GMAIL + urlencode({
            "view": "cm", "fs": "1", "to": self.correoIngeniero, "su": self.asunto}))
