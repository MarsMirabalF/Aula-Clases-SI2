import tkinter as tk
import calendar
from datetime import date
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
        self.campoFechaLimite = self.crearCampo("Fecha límite (AAAA-MM-DD)", 2, 12)
        self.botonCalendario = self.crearBoton(
            self.marcoFormulario, "Calendario", self.abrirCalendario)
        self.botonCalendario.grid(row=1, column=3, padx=(0, 8), sticky="s")
        self.campoHoraLimite = self.crearCampo("Hora límite (HH:MM)", 4, 7)
        self.botonReloj = self.crearBoton(
            self.marcoFormulario, "Reloj", self.abrirReloj)
        self.botonReloj.grid(row=1, column=5, padx=(0, 8), sticky="s")
        self.botonRegistrar = self.crearBoton(self.marcoFormulario, "Registrar tarea",
                                              self.registrarTarea)
        self.botonRegistrar.grid(row=2, column=0, columnspan=7,
                                 padx=(0, 0), pady=(10, 0), sticky="w")

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

    def abrirCalendario(self):
        ventana = tk.Toplevel(self)
        ventana.title("Seleccionar fecha")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        fechaActual = date.today()
        try:
            fechaActual = date.fromisoformat(self.campoFechaLimite.get())
        except ValueError:
            pass
        ano = fechaActual.year
        mes = fechaActual.month

        encabezado = tk.Frame(ventana, bg=COLOR_FONDO)
        encabezado.pack(padx=12, pady=12)
        marcoDias = tk.Frame(ventana, bg=COLOR_FONDO)
        marcoDias.pack(padx=12, pady=(0, 12))

        etiquetaMes = tk.Label(encabezado, font=FUENTE_BOTON,
                               bg=COLOR_FONDO, fg=COLOR_PRIMARIO, width=16)
        etiquetaMes.pack(side="left", padx=8)

        def cambiarMes(cambio):
            nonlocal ano, mes
            mes += cambio
            if mes == 13:
                mes, ano = 1, ano + 1
            elif mes == 0:
                mes, ano = 12, ano - 1
            mostrarMes()

        tk.Button(encabezado, text="<", command=lambda: cambiarMes(-1),
                  font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
                  relief="flat", padx=8).pack(side="left")
        tk.Button(encabezado, text=">", command=lambda: cambiarMes(1),
                  font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
                  relief="flat", padx=8).pack(side="right")

        def seleccionarDia(dia):
            self.campoFechaLimite.delete(0, "end")
            self.campoFechaLimite.insert(0, f"{ano:04d}-{mes:02d}-{dia:02d}")
            ventana.destroy()

        def mostrarMes():
            for widget in marcoDias.winfo_children():
                widget.destroy()
            etiquetaMes.config(text=f"{calendar.month_name[mes]} {ano}")
            for columna, nombre in enumerate(("Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do")):
                tk.Label(marcoDias, text=nombre, font=FUENTE_ESTADO,
                         bg=COLOR_FONDO, fg=COLOR_SECUNDARIO,
                         width=4).grid(row=0, column=columna, pady=4)
            for fila, semana in enumerate(calendar.monthcalendar(ano, mes), start=1):
                for columna, dia in enumerate(semana):
                    if dia:
                        tk.Button(
                            marcoDias, text=str(dia), command=lambda d=dia: seleccionarDia(d),
                            font=FUENTE_NORMAL, bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
                            activebackground=COLOR_SECUNDARIO, relief="flat", width=3,
                            padx=2, pady=2).grid(row=fila, column=columna, padx=2, pady=2)

        mostrarMes()

    def abrirReloj(self):
        ventana = tk.Toplevel(self)
        ventana.title("Seleccionar hora")
        ventana.configure(bg=COLOR_FONDO)
        ventana.resizable(False, False)

        horaInicial, minutoInicial = 0, 0
        try:
            horaInicial, minutoInicial = map(int, self.campoHoraLimite.get().split(":"))
        except (ValueError, AttributeError):
            pass

        marco = tk.Frame(ventana, bg=COLOR_FONDO)
        marco.pack(padx=20, pady=20)
        tk.Label(marco, text="Hora", font=FUENTE_ESTADO,
                 bg=COLOR_FONDO, fg=COLOR_SECUNDARIO).grid(row=0, column=0, padx=4)
        tk.Label(marco, text="Minutos", font=FUENTE_ESTADO,
                 bg=COLOR_FONDO, fg=COLOR_SECUNDARIO).grid(row=0, column=1, padx=4)
        campoHora = tk.Spinbox(marco, from_=0, to=23, width=4, format="%02.0f",
                               font=FUENTE_NORMAL, justify="center")
        campoHora.delete(0, "end")
        campoHora.insert(0, f"{horaInicial:02d}")
        campoHora.grid(row=1, column=0, padx=4, pady=8)
        campoMinuto = tk.Spinbox(marco, from_=0, to=59, width=4, format="%02.0f",
                                 font=FUENTE_NORMAL, justify="center")
        campoMinuto.delete(0, "end")
        campoMinuto.insert(0, f"{minutoInicial:02d}")
        campoMinuto.grid(row=1, column=1, padx=4, pady=8)

        def seleccionarHora():
            self.campoHoraLimite.delete(0, "end")
            self.campoHoraLimite.insert(
                0, f"{int(campoHora.get()):02d}:{int(campoMinuto.get()):02d}")
            ventana.destroy()

        tk.Button(ventana, text="Aceptar", command=seleccionarHora,
                  font=FUENTE_BOTON, bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
                  activebackground=COLOR_SECUNDARIO, relief="flat",
                  padx=16, pady=8).pack(pady=(0, 16))

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
            fechaHoraLimite = self.campoFechaLimite.get() + " " + self.campoHoraLimite.get()
            tarea = Tarea(self.campoNumero.get(), self.campoTema.get(), fechaHoraLimite)
            tarea.guardar()
        except ValueError as error:
            self.mostrarEstado(str(error), COLOR_ERROR)
            return
        for campo in (self.campoNumero, self.campoTema,
                      self.campoFechaLimite, self.campoHoraLimite):
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
