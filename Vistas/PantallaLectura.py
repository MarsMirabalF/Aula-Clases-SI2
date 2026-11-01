from datetime import date
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from estilos import (
    COLOR_ACENTO, COLOR_ERROR, COLOR_FONDO, COLOR_PRIMARIO, COLOR_SECUNDARIO,
    FUENTE_BOTON, FUENTE_ENCABEZADO_TABLA, FUENTE_ESTADO, FUENTE_NORMAL,
    FUENTE_TITULO,
)


class PantallaLectura(tk.Toplevel):
    """Lecturas PDF y apuntes de clase en una misma ventana."""

    def __init__(self, padre, gestorApuntes):
        super().__init__(padre)
        self.gestorApuntes = gestorApuntes
        self.lecturas = []
        self.apuntes = {}
        self.idApunte = None
        self.documento = None
        self.imagenPagina = None
        self.pagina = 0
        self.zoom = 1.0
        self._seleccionProgramada = False
        self.title("Lecturas y apuntes")
        self.geometry("1200x820")
        self.minsize(1000, 700)
        self.configure(bg=COLOR_FONDO)
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        self.tituloLectura = tk.StringVar()
        self.lecturaVisor = tk.StringVar()
        self.lecturaApunte = tk.StringVar()
        self.fechaClase = tk.StringVar(value=date.today().isoformat())
        self.fechaFiltro = tk.StringVar()
        self.lecturaFiltro = tk.StringVar(value="Todas las lecturas")
        self._crearInterfaz()
        self._guardado = self._contenidoEditor()
        self.actualizarLecturas()
        self.actualizarApuntes()

    def _etiqueta(self, padre, texto, **opciones):
        return tk.Label(padre, text=texto, bg=COLOR_FONDO, fg=COLOR_PRIMARIO,
                        font=FUENTE_NORMAL, **opciones)

    def _boton(self, padre, texto, comando):
        return tk.Button(
            padre, text=texto, command=comando, font=FUENTE_BOTON,
            bg=COLOR_PRIMARIO, fg=COLOR_FONDO,
            activebackground=COLOR_SECUNDARIO, activeforeground=COLOR_FONDO,
            relief="flat", cursor="hand2", padx=10, pady=5)

    def _crearInterfaz(self):
        encabezado = tk.Frame(self, bg=COLOR_PRIMARIO)
        encabezado.pack(fill="x")
        tk.Label(encabezado, text="Lecturas y apuntes", font=FUENTE_TITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_FONDO).pack(anchor="w", padx=20, pady=12)

        importar = tk.Frame(self, bg=COLOR_FONDO)
        importar.pack(fill="x", padx=16, pady=10)
        self._etiqueta(importar, "Título de la lectura:").pack(side="left")
        tk.Entry(importar, textvariable=self.tituloLectura,
                 font=FUENTE_NORMAL).pack(side="left", fill="x", expand=True, padx=10)
        self._boton(importar, "Seleccionar e importar PDF", self.importarLectura).pack(side="left")

        paneles = tk.PanedWindow(self, orient="horizontal", bg=COLOR_ACENTO,
                                sashwidth=6, bd=0)
        paneles.pack(fill="both", expand=True, padx=16)
        visor = tk.Frame(paneles, bg=COLOR_FONDO)
        editor = tk.Frame(paneles, bg=COLOR_FONDO)
        paneles.add(visor, minsize=410, stretch="always")
        paneles.add(editor, minsize=380, stretch="always")
        self._crearVisor(visor)
        self._crearEditor(editor)
        self._crearListaApuntes()

        self.etiquetaEstado = tk.Label(self, text="", font=FUENTE_ESTADO,
                                       bg=COLOR_FONDO, fg=COLOR_SECUNDARIO, anchor="w")
        self.etiquetaEstado.pack(fill="x", padx=16, pady=(4, 10))

    def _crearVisor(self, padre):
        self._etiqueta(padre, "Lectura que estás consultando").pack(anchor="w", pady=(4, 2))
        self.selectorVisor = ttk.Combobox(padre, textvariable=self.lecturaVisor,
                                          state="readonly", font=FUENTE_NORMAL)
        self.selectorVisor.pack(fill="x", padx=(0, 8))
        self.selectorVisor.bind("<<ComboboxSelected>>", self.abrirLectura)
        controles = tk.Frame(padre, bg=COLOR_FONDO)
        controles.pack(fill="x", pady=6)
        self.botonAnterior = self._boton(controles, "◀", lambda: self.cambiarPagina(-1))
        self.botonAnterior.pack(side="left")
        self.etiquetaPagina = self._etiqueta(controles, "Sin PDF", width=16)
        self.etiquetaPagina.pack(side="left")
        self.botonSiguiente = self._boton(controles, "▶", lambda: self.cambiarPagina(1))
        self.botonSiguiente.pack(side="left")
        self._boton(controles, "−", lambda: self.cambiarZoom(-0.25)).pack(side="left", padx=(12, 0))
        self.etiquetaZoom = self._etiqueta(controles, "100 %", width=6)
        self.etiquetaZoom.pack(side="left")
        self._boton(controles, "+", lambda: self.cambiarZoom(0.25)).pack(side="left")

        marco = tk.Frame(padre, bg=COLOR_ACENTO)
        marco.pack(fill="both", expand=True, padx=(0, 8), pady=(0, 4))
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        self.lienzo = tk.Canvas(marco, bg="white", highlightthickness=0)
        vertical = ttk.Scrollbar(marco, orient="vertical", command=self.lienzo.yview)
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=self.lienzo.xview)
        self.lienzo.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        self._mensajeVisor("Importa o selecciona una lectura PDF.")
        self._actualizarControlesPdf()

    def _crearEditor(self, padre):
        self.etiquetaEditor = self._etiqueta(padre, "Nuevo apunte")
        self.etiquetaEditor.pack(anchor="w", padx=8, pady=(4, 6))
        formulario = tk.Frame(padre, bg=COLOR_FONDO)
        formulario.pack(fill="x", padx=8)
        formulario.columnconfigure(1, weight=1)
        self._etiqueta(formulario, "Fecha de clase:").grid(row=0, column=0, sticky="w")
        tk.Entry(formulario, textvariable=self.fechaClase, font=FUENTE_NORMAL,
                 width=14).grid(row=0, column=1, sticky="w", padx=8)
        self._etiqueta(formulario, "Formato: AAAA-MM-DD").grid(row=1, column=1, sticky="w", padx=8)
        self._etiqueta(formulario, "Lectura asociada:").grid(row=2, column=0, sticky="w", pady=6)
        self.selectorApunte = ttk.Combobox(formulario, textvariable=self.lecturaApunte,
                                           state="readonly", font=FUENTE_NORMAL)
        self.selectorApunte.grid(row=2, column=1, sticky="ew", padx=8, pady=6)
        self.selectorApunte.bind("<<ComboboxSelected>>", self._consultarLecturaAsociada)

        marcoTexto = tk.Frame(padre, bg=COLOR_FONDO)
        marcoTexto.pack(fill="both", expand=True, padx=8, pady=4)
        self.textoApunte = tk.Text(marcoTexto, wrap="word", undo=True, width=40,
                                   height=10, font=FUENTE_NORMAL, padx=8, pady=8)
        scroll = ttk.Scrollbar(marcoTexto, orient="vertical", command=self.textoApunte.yview)
        self.textoApunte.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.textoApunte.pack(side="left", fill="both", expand=True)
        acciones = tk.Frame(padre, bg=COLOR_FONDO)
        acciones.pack(fill="x", padx=8, pady=6)
        self._boton(acciones, "Guardar apunte", self.guardarApunte).pack(side="left")
        self._boton(acciones, "Nuevo apunte", self.nuevoApunte).pack(side="left", padx=8)

    def _crearListaApuntes(self):
        marco = tk.Frame(self, bg=COLOR_FONDO)
        marco.pack(fill="x", padx=16, pady=(8, 0))
        self._etiqueta(marco, "Apuntes guardados · selecciona uno para editarlo").pack(anchor="w")
        filtros = tk.Frame(marco, bg=COLOR_FONDO)
        filtros.pack(fill="x", pady=5)
        self._etiqueta(filtros, "Fecha (AAAA-MM-DD):").pack(side="left")
        tk.Entry(filtros, textvariable=self.fechaFiltro, font=FUENTE_NORMAL,
                 width=13).pack(side="left", padx=(6, 12))
        self._etiqueta(filtros, "Lectura:").pack(side="left")
        self.selectorFiltro = ttk.Combobox(filtros, textvariable=self.lecturaFiltro,
                                           state="readonly", font=FUENTE_NORMAL, width=26,
                                           values=["Todas las lecturas"])
        self.selectorFiltro.pack(side="left", fill="x", expand=True, padx=6)
        self._boton(filtros, "Filtrar", self.aplicarFiltros).pack(side="left", padx=4)
        self._boton(filtros, "Limpiar filtros", self.limpiarFiltros).pack(side="left")

        estilo = ttk.Style(self)
        estilo.configure("Lecturas.Treeview", font=FUENTE_NORMAL, rowheight=24,
                         background=COLOR_FONDO, fieldbackground=COLOR_FONDO,
                         foreground=COLOR_PRIMARIO)
        estilo.configure("Lecturas.Treeview.Heading", font=FUENTE_ENCABEZADO_TABLA)
        tablaMarco = tk.Frame(marco, bg=COLOR_FONDO)
        tablaMarco.pack(fill="x")
        self.tablaApuntes = ttk.Treeview(tablaMarco, columns=("fecha", "dia", "lectura", "texto"),
                                        show="headings", selectmode="browse", height=5,
                                        style="Lecturas.Treeview")
        for columna, titulo, ancho in (("fecha", "Fecha", 110), ("dia", "Día", 110),
                                      ("lectura", "Lectura", 280), ("texto", "Apunte", 420)):
            self.tablaApuntes.heading(columna, text=titulo)
            self.tablaApuntes.column(columna, width=ancho, minwidth=80)
        barra = ttk.Scrollbar(tablaMarco, orient="vertical", command=self.tablaApuntes.yview)
        self.tablaApuntes.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tablaApuntes.pack(side="left", fill="x", expand=True)
        self.tablaApuntes.bind("<<TreeviewSelect>>", self.seleccionarApunte)

    def _opcionesLecturas(self):
        # El número permite distinguir títulos repetidos sin mostrar IDs internos.
        return [f"{numero}. {lectura['titulo']}" for numero, lectura in enumerate(self.lecturas, 1)]

    def _idLectura(self, selector):
        indice = selector.current()
        if selector is self.selectorFiltro:
            indice -= 1
        if 0 <= indice < len(self.lecturas):
            return self.lecturas[indice]["id"]
        return None

    def _seleccionarLectura(self, selector, idLectura):
        for indice, lectura in enumerate(self.lecturas):
            if lectura["id"] == idLectura:
                selector.current(indice + (1 if selector is self.selectorFiltro else 0))
                return
        selector.set("Todas las lecturas" if selector is self.selectorFiltro else "")

    def actualizarLecturas(self):
        anteriores = [(selector, self._idLectura(selector)) for selector in
                      (self.selectorVisor, self.selectorApunte, self.selectorFiltro)]
        try:
            lecturas = self.gestorApuntes.listarLecturas()
        except Exception as error:
            self._mostrarError("cargar las lecturas", error)
            return False
        self.lecturas = lecturas
        opciones = self._opcionesLecturas()
        self.selectorVisor.configure(values=opciones)
        self.selectorApunte.configure(values=opciones)
        self.selectorFiltro.configure(values=["Todas las lecturas"] + opciones)
        for selector, idLectura in anteriores:
            self._seleccionarLectura(selector, idLectura)
        return True

    def importarLectura(self):
        titulo = self.tituloLectura.get().strip()
        if not titulo:
            messagebox.showwarning("Título requerido", "Escribe el título de la lectura antes de importar.", parent=self)
            return
        ruta = filedialog.askopenfilename(parent=self, title="Seleccionar lectura PDF",
                                          filetypes=[("Documentos PDF", "*.pdf")])
        if not ruta:
            return
        try:
            lectura = self.gestorApuntes.agregarLectura(titulo, ruta)
        except Exception as error:
            self._mostrarError("importar la lectura", error)
            return
        self.tituloLectura.set("")
        if self.actualizarLecturas():
            self._seleccionarLectura(self.selectorVisor, lectura["id"])
            self.abrirLectura()
        self._estado("Lectura importada. Puedes asociarla a un apunte.")

    def _consultarLecturaAsociada(self, evento=None):
        self._seleccionarLectura(self.selectorVisor, self._idLectura(self.selectorApunte))
        self.abrirLectura()

    def abrirLectura(self, evento=None):
        self._cerrarDocumento()
        self._mensajeVisor("Selecciona una lectura PDF.")
        idLectura = self._idLectura(self.selectorVisor)
        if idLectura is None:
            return
        try:
            import pymupdf
        except ImportError:
            self._mensajeVisor("Falta PyMuPDF para visualizar esta lectura.")
            messagebox.showerror("Visor PDF no disponible",
                                 "Instala el visor desde la carpeta del proyecto:\n\n"
                                 "python -m pip install pymupdf\n\n"
                                 "Después vuelve a abrir el sistema.", parent=self)
            return
        try:
            ruta = self.gestorApuntes.obtenerRutaPdf(idLectura)
            self.documento = pymupdf.open(str(ruta))
            if not self.documento.is_pdf or self.documento.needs_pass or self.documento.page_count < 1:
                raise ValueError("Selecciona un PDF válido, con páginas y sin contraseña.")
            self.pagina = 0
            self.zoom = 1.0
            self._renderizarPagina()
        except Exception as error:
            self._cerrarDocumento()
            self._mensajeVisor("No se pudo abrir el PDF. Los apuntes siguen disponibles.")
            self._mostrarError("abrir el PDF", error)

    def _renderizarPagina(self):
        if self.documento is None:
            return
        pagina = self.documento.load_page(self.pagina)
        imagen = pagina.get_pixmap(dpi=round(72 * self.zoom), alpha=False)
        self.imagenPagina = tk.PhotoImage(master=self, data=imagen.tobytes("png"))
        self.lienzo.delete("all")
        self.lienzo.create_image(0, 0, anchor="nw", image=self.imagenPagina)
        self.lienzo.configure(scrollregion=(0, 0, imagen.width, imagen.height))
        self.lienzo.xview_moveto(0)
        self.lienzo.yview_moveto(0)
        self._actualizarControlesPdf()

    def _actualizarControlesPdf(self):
        total = self.documento.page_count if self.documento is not None else 0
        self.etiquetaPagina.configure(text=f"Página {self.pagina + 1} de {total}" if total else "Sin PDF")
        self.etiquetaZoom.configure(text=f"{round(self.zoom * 100)} %")
        self.botonAnterior.configure(state="normal" if total and self.pagina > 0 else "disabled")
        self.botonSiguiente.configure(state="normal" if total and self.pagina < total - 1 else "disabled")

    def cambiarPagina(self, desplazamiento):
        if self.documento is None:
            return
        nueva = self.pagina + desplazamiento
        if 0 <= nueva < self.documento.page_count:
            anterior = self.pagina
            self.pagina = nueva
            try:
                self._renderizarPagina()
            except Exception as error:
                self.pagina = anterior
                self._mostrarError("mostrar la página", error)

    def cambiarZoom(self, cambio):
        if self.documento is None:
            return
        anterior = self.zoom
        self.zoom = min(2.0, max(0.5, self.zoom + cambio))
        try:
            self._renderizarPagina()
        except Exception as error:
            self.zoom = anterior
            self._mostrarError("ampliar el PDF", error)

    def _mensajeVisor(self, texto):
        self.imagenPagina = None
        self.lienzo.delete("all")
        self.lienzo.create_text(20, 30, text=texto, anchor="nw", width=360,
                                font=FUENTE_NORMAL, fill=COLOR_SECUNDARIO)
        self.lienzo.configure(scrollregion=(0, 0, 400, 100))

    def _cerrarDocumento(self):
        if self.documento is not None:
            self.documento.close()
            self.documento = None
        self.imagenPagina = None
        self._actualizarControlesPdf()

    def _contenidoEditor(self):
        return (self.textoApunte.get("1.0", "end-1c"), self.fechaClase.get(),
                self._idLectura(self.selectorApunte))

    def _confirmarCambios(self):
        if self._contenidoEditor() == self._guardado:
            return True
        respuesta = messagebox.askyesnocancel(
            "Cambios sin guardar", "Hay cambios en el apunte. ¿Deseas guardarlos?\n\n"
            "Sí: guardar. No: descartar. Cancelar: seguir editando.", parent=self)
        if respuesta is None:
            return False
        return self.guardarApunte() if respuesta else True

    def nuevoApunte(self):
        if not self._confirmarCambios():
            return
        self.idApunte = None
        self.fechaClase.set(date.today().isoformat())
        self._seleccionarLectura(self.selectorApunte, self._idLectura(self.selectorVisor))
        self.textoApunte.delete("1.0", "end")
        self.textoApunte.edit_reset()
        self.etiquetaEditor.configure(text="Nuevo apunte")
        self.tablaApuntes.selection_remove(*self.tablaApuntes.selection())
        self._guardado = self._contenidoEditor()
        self.textoApunte.focus_set()

    @staticmethod
    def _validarFecha(valor):
        try:
            fecha = date.fromisoformat(valor)
        except ValueError:
            raise ValueError("Escribe una fecha válida con formato AAAA-MM-DD.") from None
        if fecha.isoformat() != valor:
            raise ValueError("Escribe la fecha con formato AAAA-MM-DD; por ejemplo, 2026-11-01.")
        return valor

    def guardarApunte(self):
        texto, fecha, idLectura = self._contenidoEditor()
        try:
            self._validarFecha(fecha.strip())
            if not texto.strip():
                raise ValueError("Escribe el contenido del apunte.")
            if idLectura is None:
                raise ValueError("Selecciona la lectura asociada al apunte.")
            if self.idApunte is None:
                apunte = self.gestorApuntes.registrarApunte(texto, fecha.strip(), idLectura)
            else:
                apunte = self.gestorApuntes.editarApunte(self.idApunte, texto, fecha.strip(), idLectura)
        except Exception as error:
            self._mostrarError("guardar el apunte", error)
            return False
        self.idApunte = apunte["id"]
        self.fechaClase.set(apunte["fechaClase"])
        self._guardado = self._contenidoEditor()
        self.etiquetaEditor.configure(text="Editar apunte")
        if self.actualizarApuntes():
            self._estado("Apunte guardado.")
        return True

    def seleccionarApunte(self, evento=None):
        seleccion = self.tablaApuntes.selection()
        if self._seleccionProgramada or not seleccion or seleccion[0] == self.idApunte:
            return
        idSeleccionado = seleccion[0]
        # Guardar puede refrescar la tabla; conservamos el apunte elegido antes.
        apunte = self.apuntes.get(idSeleccionado)
        if apunte is None:
            return
        if not self._confirmarCambios():
            self._restaurarSeleccion()
            return
        self.idApunte = idSeleccionado
        self.fechaClase.set(apunte["fechaClase"])
        self._seleccionarLectura(self.selectorApunte, apunte["idLectura"])
        self.textoApunte.delete("1.0", "end")
        self.textoApunte.insert("1.0", apunte["texto"])
        self.textoApunte.edit_reset()
        self.etiquetaEditor.configure(text="Editar apunte")
        self._guardado = self._contenidoEditor()
        self._restaurarSeleccion()
        self._consultarLecturaAsociada()

    def _restaurarSeleccion(self):
        self._seleccionProgramada = True
        try:
            self.tablaApuntes.selection_remove(*self.tablaApuntes.selection())
            if self.idApunte is not None and self.tablaApuntes.exists(self.idApunte):
                self.tablaApuntes.selection_set(self.idApunte)
                self.tablaApuntes.see(self.idApunte)
        finally:
            self._seleccionProgramada = False

    def actualizarApuntes(self):
        try:
            fecha = self.fechaFiltro.get().strip() or None
            if fecha is not None:
                self._validarFecha(fecha)
            apuntes = self.gestorApuntes.listarApuntes(
                fechaClase=fecha, idLectura=self._idLectura(self.selectorFiltro))
        except Exception as error:
            self._mostrarError("cargar los apuntes", error)
            return False
        self.apuntes = {apunte["id"]: apunte for apunte in apuntes}
        self.tablaApuntes.delete(*self.tablaApuntes.get_children())
        for apunte in apuntes:
            resumen = " ".join(apunte["texto"].split())
            self.tablaApuntes.insert("", "end", iid=apunte["id"], values=(
                apunte["fechaClase"], apunte["diaClase"], apunte["tituloLectura"], resumen[:160]))
        self._restaurarSeleccion()
        self._estado(f"{len(apuntes)} apunte(s) encontrado(s).")
        return True

    def aplicarFiltros(self):
        # Filtrar solo cambia la lista: el editor conserva incluso cambios pendientes.
        self.actualizarApuntes()

    def limpiarFiltros(self):
        self.fechaFiltro.set("")
        self.selectorFiltro.current(0)
        self.actualizarApuntes()

    def _estado(self, texto, color=COLOR_SECUNDARIO):
        self.etiquetaEstado.configure(text=texto, fg=color)

    def _mostrarError(self, accion, error):
        if isinstance(error, FileNotFoundError):
            detalle = "No se encontró el archivo PDF. Comprueba que exista en la carpeta de lecturas."
        elif isinstance(error, (ValueError, ImportError)):
            detalle = str(error)
        elif accion in ("abrir el PDF", "mostrar la página", "ampliar el PDF"):
            detalle = "No se pudo leer el PDF. Comprueba que sea válido y que puedas acceder al archivo.\n\n" + str(error)
        else:
            detalle = ("Comprueba la conexión, las credenciales y la configuración de Firebase "
                       "si el problema ocurre al cargar o guardar datos.\n\n" + str(error))
        self._estado(f"No se pudo {accion}.", COLOR_ERROR)
        messagebox.showerror("No se pudo completar la operación", f"No se pudo {accion}.\n\n{detalle}", parent=self)

    def cerrar(self):
        if not self._confirmarCambios():
            return
        self.destroy()

    def confirmarCierre(self):
        return self._confirmarCambios()

    def destroy(self):
        # También libera el PDF cuando se cierra la ventana principal.
        self._cerrarDocumento()
        super().destroy()
