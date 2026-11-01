import tkinter as tk

from estilos import *


class PantallaParticipacion(tk.Toplevel):
    def __init__(self, padre, gestorParticipacion):
        super().__init__(padre)
        self.gestorParticipacion = gestorParticipacion
        self.pregunta = self.gestorParticipacion.obtenerPregunta()
        self.title("Participación en clase")
        self.geometry("620x400")
        self.configure(bg=COLOR_FONDO)

        self.marcoEncabezado = tk.Frame(self, bg=COLOR_PRIMARIO)
        self.marcoEncabezado.pack(fill="x")
        self.etiquetaTitulo = tk.Label(
            self.marcoEncabezado, text="Participación en clase", font=FUENTE_TITULO,
            bg=COLOR_PRIMARIO, fg=COLOR_FONDO)
        self.etiquetaTitulo.pack(anchor="w", padx=24, pady=16)

        self.etiquetaPregunta = tk.Label(
            self, text=self.pregunta.mostrarPregunta(), font=FUENTE_NORMAL,
            bg=COLOR_FONDO, fg=COLOR_PRIMARIO, wraplength=540, justify="left")
        self.etiquetaPregunta.pack(anchor="w", padx=24, pady=(28, 20))

        self.botonParticipar = self.crearBoton("Participar", self.mostrarOpciones)
        self.botonParticipar.pack(padx=24, pady=8)

        self.marcoOpciones = tk.Frame(self, bg=COLOR_FONDO)
        self.botonCorrecta = self.crearBoton("Correcta", lambda: self.registrarResultado(True))
        self.botonIncorrecta = self.crearBoton("Incorrecta", lambda: self.registrarResultado(False))
        self.etiquetaEstado = tk.Label(
            self, text="", font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
        self.etiquetaEstado.pack(padx=24, pady=(20, 8))

    def crearBoton(self, texto, comando):
        return tk.Button(
            self.marcoOpciones if hasattr(self, "marcoOpciones") else self,
            text=texto, command=comando, font=FUENTE_BOTON, bg=COLOR_PRIMARIO,
            fg=COLOR_FONDO, activebackground=COLOR_SECUNDARIO,
            activeforeground=COLOR_FONDO, relief="flat", bd=0, cursor="hand2",
            highlightthickness=1, highlightbackground=COLOR_ACENTO, padx=16, pady=8)

    def mostrarOpciones(self):
        self.botonParticipar.config(state="disabled")
        self.marcoOpciones.pack(pady=8)
        self.botonCorrecta.pack(side="left", padx=4)
        self.botonIncorrecta.pack(side="left", padx=4)

    def registrarResultado(self, esCorrecta):
        self.gestorParticipacion.registrarParticipacion(self.pregunta, esCorrecta)
        mensaje = "¡Bien!" if esCorrecta else "¡Date un golpe!"
        color = COLOR_PRIMARIO if esCorrecta else COLOR_ERROR
        self.etiquetaEstado.config(text=mensaje, fg=color)
        self.botonCorrecta.config(state="disabled")
        self.botonIncorrecta.config(state="disabled")
