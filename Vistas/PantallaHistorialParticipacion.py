import tkinter as tk
from tkinter import ttk

from estilos import *


class PantallaHistorialParticipacion(tk.Toplevel):
    def __init__(self, padre, gestorParticipacion):
        super().__init__(padre)
        self.gestorParticipacion = gestorParticipacion
        self.title("Historial de participaciones")
        self.geometry("820x480")
        self.configure(bg=COLOR_FONDO)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure(
            "Treeview", background=COLOR_FONDO, fieldbackground=COLOR_FONDO,
            foreground=COLOR_PRIMARIO, font=FUENTE_NORMAL, rowheight=28,
            bordercolor=COLOR_ACENTO)
        estilo.configure(
            "Treeview.Heading", font=FUENTE_ENCABEZADO_TABLA,
            background=COLOR_ACENTO, foreground=COLOR_PRIMARIO)
        estilo.map(
            "Treeview", background=[("selected", COLOR_ACENTO)],
            foreground=[("selected", COLOR_PRIMARIO)])

        self.marcoEncabezado = tk.Frame(self, bg=COLOR_PRIMARIO)
        self.marcoEncabezado.pack(fill="x")
        self.etiquetaTitulo = tk.Label(
            self.marcoEncabezado, text="Historial de participaciones",
            font=FUENTE_TITULO, bg=COLOR_PRIMARIO, fg=COLOR_FONDO)
        self.etiquetaTitulo.pack(anchor="w", padx=24, pady=16)

        self.etiquetaResumen = tk.Label(
            self, text="", font=FUENTE_NORMAL, bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
        self.etiquetaResumen.pack(anchor="w", padx=24, pady=(16, 8))

        self.marcoTabla = tk.Frame(
            self, bg=COLOR_FONDO, highlightthickness=1,
            highlightbackground=COLOR_ACENTO)
        self.marcoTabla.pack(fill="both", expand=True, padx=24, pady=8)

        self.tablaHistorial = ttk.Treeview(
            self.marcoTabla, columns=("pregunta", "fecha", "resultado"),
            show="headings")
        self.tablaHistorial.heading("pregunta", text="Pregunta")
        self.tablaHistorial.heading("fecha", text="Fecha")
        self.tablaHistorial.heading("resultado", text="Resultado")
        self.tablaHistorial.column("pregunta", width=480, anchor="w")
        self.tablaHistorial.column("fecha", width=150, anchor="center")
        self.tablaHistorial.column("resultado", width=140, anchor="center")
        self.tablaHistorial.tag_configure("Correcta", foreground=COLOR_PRIMARIO)
        self.tablaHistorial.tag_configure("Incorrecta", foreground=COLOR_ERROR)
        self.tablaHistorial.pack(fill="both", expand=True, padx=1, pady=1)

        self.botonActualizar = tk.Button(
            self, text="Actualizar", command=self.actualizarTabla,
            font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
            activebackground=COLOR_SECUNDARIO, activeforeground=COLOR_FONDO,
            relief="flat", bd=0, cursor="hand2", highlightthickness=1,
            highlightbackground=COLOR_ACENTO, padx=16, pady=8)
        self.botonActualizar.pack(anchor="e", padx=24, pady=(0, 16))

        self.actualizarTabla()

    def actualizarTabla(self):
        self.tablaHistorial.delete(*self.tablaHistorial.get_children())
        for participacion in self.gestorParticipacion.listarParticipaciones():
            resultado = participacion["resultado"]
            self.tablaHistorial.insert(
                "", "end", iid=participacion["id"],
                values=(participacion["pregunta"], participacion["fecha"], resultado),
                tags=(resultado,))
        correctas = self.gestorParticipacion.contarCorrectas()
        incorrectas = self.gestorParticipacion.contarIncorrectas()
        self.etiquetaResumen.config(
            text=f"Participaciones: {correctas + incorrectas}   "
                 f"Correctas: {correctas}   Incorrectas: {incorrectas}")
