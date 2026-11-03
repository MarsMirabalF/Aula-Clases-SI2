import tkinter as tk
from tkinter import ttk
from estilos import *


class PantallaPenalizaciones(tk.Toplevel):
    def __init__(self, padre, gestorPenalizaciones):
        super().__init__(padre)
        self.gestorPenalizaciones = gestorPenalizaciones
        self.title("Penalizaciones")
        self.geometry("760x480")
        self.configure(bg=COLOR_FONDO)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background=COLOR_FONDO, fieldbackground=COLOR_FONDO,
                         foreground=COLOR_PRIMARIO, font=FUENTE_NORMAL, rowheight=24,
                         bordercolor=COLOR_ACENTO)
        estilo.configure("Treeview.Heading", font=FUENTE_ENCABEZADO_TABLA,
                         background=COLOR_ACENTO, foreground=COLOR_PRIMARIO)
        estilo.map("Treeview", background=[("selected", COLOR_ACENTO)],
                   foreground=[("selected", COLOR_PRIMARIO)])

        self.marcoEncabezado = tk.Frame(self, bg=COLOR_PRIMARIO)
        self.marcoEncabezado.pack(fill="x")
        self.etiquetaTitulo = tk.Label(self.marcoEncabezado, text="Penalizaciones",
                                       font=FUENTE_TITULO, bg=COLOR_PRIMARIO, fg=COLOR_FONDO)
        self.etiquetaTitulo.pack(anchor="w", padx=24, pady=16)

        self.etiquetaContador = tk.Label(self, text="", font=FUENTE_NORMAL,
                                         bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
        self.etiquetaContador.pack(anchor="w", padx=24, pady=(16, 8))

        self.marcoTabla = tk.Frame(self, bg=COLOR_FONDO, highlightthickness=1,
                                   highlightbackground=COLOR_ACENTO)
        self.marcoTabla.pack(fill="both", expand=True, padx=24, pady=8)

        self.tablaPenalizaciones = ttk.Treeview(
            self.marcoTabla, columns=("diaTarde", "fechaTarde", "proximaClase", "estado"),
            show="headings", selectmode="browse")
        self.tablaPenalizaciones.heading("diaTarde", text="Día que llegué tarde")
        self.tablaPenalizaciones.heading("fechaTarde", text="Fecha")
        self.tablaPenalizaciones.heading("proximaClase", text="Llevar fruta el")
        self.tablaPenalizaciones.heading("estado", text="Estado")
        self.tablaPenalizaciones.column("diaTarde", width=160)
        self.tablaPenalizaciones.column("fechaTarde", width=120)
        self.tablaPenalizaciones.column("proximaClase", width=220)
        self.tablaPenalizaciones.column("estado", width=120)
        self.tablaPenalizaciones.tag_configure("Pendiente", foreground=COLOR_ERROR)
        self.tablaPenalizaciones.tag_configure("Cumplida", foreground=COLOR_PRIMARIO)
        self.tablaPenalizaciones.pack(fill="both", expand=True, padx=1, pady=1)

        self.marcoBotones = tk.Frame(self, bg=COLOR_FONDO)
        self.marcoBotones.pack(fill="x", padx=24, pady=8)
        self.botonRegistrar = self.crearBoton("Registrar llegada tarde", self.registrarLlegadaTarde)
        self.botonRegistrar.pack(side="left", padx=(0, 8))
        self.botonMarcarCumplida = self.crearBoton("Marcar como cumplida", self.marcarComoCumplida)
        self.botonMarcarCumplida.pack(side="left")

        self.etiquetaEstado = tk.Label(self, text="", font=FUENTE_ESTADO,
                                       bg=COLOR_FONDO, fg=COLOR_SECUNDARIO)
        self.etiquetaEstado.pack(anchor="w", padx=24, pady=(0, 16))

        self.actualizarTabla()

    def crearBoton(self, texto, comando):
        return tk.Button(self.marcoBotones, text=texto, command=comando, font=FUENTE_BOTON,
                         bg=COLOR_PRIMARIO, fg=COLOR_FONDO, activebackground=COLOR_SECUNDARIO,
                         activeforeground=COLOR_FONDO, relief="flat", bd=0, cursor="hand2",
                         highlightthickness=1, highlightbackground=COLOR_ACENTO,
                         padx=16, pady=8)

    def actualizarTabla(self):
        self.tablaPenalizaciones.delete(*self.tablaPenalizaciones.get_children())
        for penalizacion in self.gestorPenalizaciones.listarPenalizaciones():
            self.tablaPenalizaciones.insert(
                "", "end", iid=penalizacion["id"],
                values=(penalizacion["diaTarde"], penalizacion["fechaTarde"],
                        penalizacion["proximaClase"], "● " + penalizacion["estado"]),
                tags=(penalizacion["estado"],))
        self.etiquetaContador.config(
            text="Veces que he llegado tarde: " + str(self.gestorPenalizaciones.contarLlegadasTarde()))

    def mostrarEstado(self, texto, color):
        self.etiquetaEstado.config(text=texto, fg=color)

    def registrarLlegadaTarde(self):
        if self.gestorPenalizaciones.registrarLlegadaTarde():
            self.actualizarTabla()
            self.mostrarEstado("Llegada tarde registrada", COLOR_PRIMARIO)
        else:
            self.mostrarEstado("Hoy no hay clase, no se registra", COLOR_ERROR)
            
    def marcarComoCumplida(self):
        seleccion = self.tablaPenalizaciones.selection()
        if not seleccion:
            self.mostrarEstado("Selecciona una penalización", COLOR_ERROR)
            return
        self.gestorPenalizaciones.marcarComoCumplida(seleccion[0])
        self.actualizarTabla()
        self.mostrarEstado("Penalización marcada como cumplida", COLOR_PRIMARIO)
