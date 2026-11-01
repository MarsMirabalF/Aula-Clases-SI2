import tkinter as tk
from estilos import *
from Vistas.PantallaPenalizaciones import PantallaPenalizaciones
from Vistas.PantallaLectura import PantallaLectura


class PantallaInicio(tk.Frame):
    def __init__(self, padre, gestorPenalizaciones, gestorApuntes):
        super().__init__(padre, bg=COLOR_FONDO)
        self.padre = padre
        self.gestorPenalizaciones = gestorPenalizaciones
        self.gestorApuntes = gestorApuntes
        self.pantallaLecturas = None
        self.padre.protocol("WM_DELETE_WINDOW", self.cerrarSistema)

        self.marcoEncabezado = tk.Frame(self, bg=COLOR_PRIMARIO)
        self.marcoEncabezado.pack(fill="x")
        self.etiquetaTitulo = tk.Label(self.marcoEncabezado, text="Inicio", font=FUENTE_TITULO,
                                       bg=COLOR_PRIMARIO, fg=COLOR_FONDO)
        self.etiquetaTitulo.pack(anchor="w", padx=24, pady=16)

        self.botonPenalizaciones = tk.Button(
            self, text="Penalizaciones", command=self.abrirPenalizaciones, font=FUENTE_BOTON,
            bg=COLOR_PRIMARIO, fg=COLOR_FONDO, activebackground=COLOR_SECUNDARIO,
            activeforeground=COLOR_FONDO, relief="flat", bd=0, cursor="hand2",
            highlightthickness=1, highlightbackground=COLOR_ACENTO, padx=16, pady=8)
        self.botonPenalizaciones.pack(padx=24, pady=24)

        self.botonLecturas = tk.Button(
            self, text="Apuntes y lecturas", command=self.abrirLecturas, font=FUENTE_BOTON,
            bg=COLOR_PRIMARIO, fg=COLOR_FONDO, activebackground=COLOR_SECUNDARIO,
            activeforeground=COLOR_FONDO, relief="flat", bd=0, cursor="hand2",
            highlightthickness=1, highlightbackground=COLOR_ACENTO, padx=16, pady=8)
        self.botonLecturas.pack(padx=24, pady=(0, 24))

    def abrirPenalizaciones(self):
        PantallaPenalizaciones(self.padre, self.gestorPenalizaciones)

    def abrirLecturas(self):
        if self.pantallaLecturas is not None and self.pantallaLecturas.winfo_exists():
            self.pantallaLecturas.lift()
            self.pantallaLecturas.focus_set()
            return
        self.pantallaLecturas = PantallaLectura(self.padre, self.gestorApuntes)

    def cerrarSistema(self):
        if self.pantallaLecturas is not None and self.pantallaLecturas.winfo_exists():
            if not self.pantallaLecturas.confirmarCierre():
                return
        self.padre.destroy()
