import tkinter as tk
from tkinter import messagebox, ttk

from estilos import *
from modelos.RedireccionCorreo import RedireccionCorreo
from modelos.Tarea import Tarea


class PantallaTarea(tk.Toplevel):
    def __init__(self, padre, redireccionCorreo=None):
        super().__init__(padre)
        self.redireccionCorreo = redireccionCorreo or RedireccionCorreo()
        self.tareas = {}
        self.title("Tareas")
        self.geometry("780x720")
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
        self.etiquetaTitulo = tk.Label(self.marcoEncabezado, text="Tareas",
                                       font=FUENTE_TITULO, bg=COLOR_PRIMARIO, fg=COLOR_FONDO)
        self.etiquetaTitulo.pack(anchor="w", padx=24, pady=16)

        self.marcoFormulario = tk.Frame(self, bg=COLOR_FONDO)
        self.marcoFormulario.pack(fill="x", padx=24, pady=(16, 8))
        self.campoNumero = self.crearCampo("Número", 0, 8)
        self.campoTema = self.crearCampo("Tema", 1, 28)
        self.campoHoraLimite = self.crearCampo("Hora límite (AAAA-MM-DD HH:MM)", 2, 18)
        self.botonRegistrar = self.crearBoton(self.marcoFormulario, "Registrar tarea",
                                              self.registrarTarea)
        self.botonRegistrar.grid(row=1, column=3, padx=(8, 0), sticky="s")

        self.marcoTabla = tk.Frame(self, bg=COLOR_FONDO, highlightthickness=1,
                                   highlightbackground=COLOR_ACENTO)
        self.marcoTabla.pack(fill="both", expand=True, padx=24, pady=8)

        self.tablaTareas = ttk.Treeview(
            self.marcoTabla, columns=("numero", "tema", "horaLimite", "tiempoRestante"),
            show="headings", selectmode="browse", height=6)
        self.tablaTareas.heading("numero", text="N°")
        self.tablaTareas.heading("tema", text="Tema")
        self.tablaTareas.heading("horaLimite", text="Hora límite")
        self.tablaTareas.heading("tiempoRestante", text="Tiempo restante")
        self.tablaTareas.column("numero", width=50, anchor="center")
        self.tablaTareas.column("tema", width=280)
        self.tablaTareas.column("horaLimite", width=160, anchor="center")
        self.tablaTareas.column("tiempoRestante", width=160, anchor="center")
        self.tablaTareas.tag_configure("Atrasada", foreground=COLOR_ERROR)
        self.tablaTareas.pack(fill="both", expand=True, padx=1, pady=1)

        self.marcoBotones = tk.Frame(self, bg=COLOR_FONDO)
        self.marcoBotones.pack(fill="x", padx=24, pady=8)
        self.botonEntregar = self.crearBoton(self.marcoBotones, "Entregar tarea",
                                             self.entregarTarea)
        self.botonEntregar.pack(side="left")

        self.etiquetaEstado = tk.Label(self, text="", font=FUENTE_ESTADO,
                                       bg=COLOR_FONDO, fg=COLOR_SECUNDARIO)
        self.etiquetaEstado.pack(anchor="w", padx=24)

        self.etiquetaHistorial = tk.Label(self, text="Historial de entregas",
                                          font=FUENTE_ENCABEZADO_TABLA, bg=COLOR_FONDO,
                                          fg=COLOR_PRIMARIO)
        self.etiquetaHistorial.pack(anchor="w", padx=24, pady=(16, 0))
        self.etiquetaResumen = tk.Label(self, text="", font=FUENTE_NORMAL,
                                        bg=COLOR_FONDO, fg=COLOR_PRIMARIO)
        self.etiquetaResumen.pack(anchor="w", padx=24, pady=(4, 8))

        self.marcoHistorial = tk.Frame(self, bg=COLOR_FONDO, highlightthickness=1,
                                       highlightbackground=COLOR_ACENTO)
        self.marcoHistorial.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        self.tablaEntregas = ttk.Treeview(
            self.marcoHistorial, columns=("tarea", "fecha", "estado"), show="headings",
            selectmode="none", height=6)
        self.tablaEntregas.heading("tarea", text="Tarea")
        self.tablaEntregas.heading("fecha", text="Fecha y hora de entrega")
        self.tablaEntregas.heading("estado", text="Estado")
        self.tablaEntregas.column("tarea", width=340)
        self.tablaEntregas.column("fecha", width=180, anchor="center")
        self.tablaEntregas.column("estado", width=130, anchor="center")
        self.tablaEntregas.tag_configure("A tiempo", foreground=COLOR_PRIMARIO)
        self.tablaEntregas.tag_configure("Con retraso", foreground=COLOR_ERROR)
        self.tablaEntregas.pack(fill="both", expand=True, padx=1, pady=1)

        self.mostrarTareas()
        self.mostrarHistorial()
        self.actualizarCuentaRegresiva()

    def crearCampo(self, texto, columna, ancho):
        tk.Label(self.marcoFormulario, text=texto, font=FUENTE_ESTADO, bg=COLOR_FONDO,
                 fg=COLOR_SECUNDARIO).grid(row=0, column=columna, sticky="w", padx=(0, 8))
        campo = tk.Entry(self.marcoFormulario, width=ancho, font=FUENTE_NORMAL,
                         relief="flat", highlightthickness=1,
                         highlightbackground=COLOR_ACENTO, highlightcolor=COLOR_PRIMARIO)
        campo.grid(row=1, column=columna, sticky="w", padx=(0, 8), ipady=4)
        return campo

    def crearBoton(self, contenedor, texto, comando):
        return tk.Button(contenedor, text=texto, command=comando, font=FUENTE_BOTON,
                         bg=COLOR_PRIMARIO, fg=COLOR_FONDO, activebackground=COLOR_SECUNDARIO,
                         activeforeground=COLOR_FONDO, relief="flat", bd=0, cursor="hand2",
                         highlightthickness=1, highlightbackground=COLOR_ACENTO,
                         padx=16, pady=8)

    def mostrarEstado(self, texto, color):
        self.etiquetaEstado.config(text=texto, fg=color)

    def formatearTiempoRestante(self, tarea):
        if tarea.estaAtrasada():
            return "Atrasada"
        segundos = int(tarea.calcularTiempoRestante().total_seconds())
        dias, segundos = divmod(segundos, 86400)
        horas, segundos = divmod(segundos, 3600)
        minutos, segundos = divmod(segundos, 60)
        return f"{dias} d {horas:02d}:{minutos:02d}:{segundos:02d}"

    def mostrarTareas(self):
        self.tablaTareas.delete(*self.tablaTareas.get_children())
        self.tareas = {str(tarea.numero): tarea for tarea in Tarea.listarTareas()}
        for idTarea, tarea in self.tareas.items():
            self.tablaTareas.insert(
                "", "end", iid=idTarea,
                values=(tarea.numero, tarea.tema, tarea.horaLimite.strftime("%d/%m/%Y %H:%M"),
                        self.formatearTiempoRestante(tarea)),
                tags=("Atrasada",) if tarea.estaAtrasada() else ())

    def actualizarCuentaRegresiva(self):
        if not self.winfo_exists():
            return
        for idTarea, tarea in self.tareas.items():
            self.tablaTareas.set(idTarea, "tiempoRestante", self.formatearTiempoRestante(tarea))
            self.tablaTareas.item(idTarea, tags=("Atrasada",) if tarea.estaAtrasada() else ())
        self.after(1000, self.actualizarCuentaRegresiva)

    def registrarTarea(self):
        try:
            tarea = Tarea(self.campoNumero.get(), self.campoTema.get(), self.campoHoraLimite.get())
            tarea.guardar()
        except ValueError as error:
            self.mostrarEstado(str(error), COLOR_ERROR)
            return
        for campo in (self.campoNumero, self.campoTema, self.campoHoraLimite):
            campo.delete(0, "end")
        self.mostrarTareas()
        self.mostrarEstado("Tarea " + str(tarea.numero) + " registrada", COLOR_PRIMARIO)

    def entregarTarea(self):
        seleccion = self.tablaTareas.selection()
        if not seleccion:
            self.mostrarEstado("Selecciona una tarea", COLOR_ERROR)
            return
        tarea = self.tareas[seleccion[0]]
        aviso = self.redireccionCorreo.mostrarAvisoRetraso(tarea)
        if aviso:
            messagebox.showwarning(aviso, aviso + ": la hora límite ya pasó.", parent=self)
        self.redireccionCorreo.abrirCorreo(tarea)
        self.mostrarHistorial()
        self.mostrarEstado("Correo abierto: " + self.redireccionCorreo.asunto, COLOR_PRIMARIO)

    def mostrarHistorial(self):
        historialEntregas = self.redireccionCorreo.historialEntregas
        self.tablaEntregas.delete(*self.tablaEntregas.get_children())
        for entrega in historialEntregas.mostrarEntregas():
            self.tablaEntregas.insert(
                "", "end", iid=entrega["id"],
                values=(entrega["tarea"], entrega["fecha"], entrega["estado"]),
                tags=(entrega["estado"],))
        aTiempo, conRetraso = historialEntregas.mostrarATiempoYRetraso()
        self.etiquetaResumen.config(
            text=f"Entregas: {aTiempo + conRetraso}   "
                 f"A tiempo: {aTiempo}   Con retraso: {conRetraso}")
