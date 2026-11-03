from datetime import date
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter.scrolledtext import ScrolledText

import pymupdf

from estilos import COLOR_FONDO, COLOR_PRIMARIO, FUENTE_BOTON, FUENTE_NORMAL, FUENTE_TITULO


class PantallaLectura(tk.Toplevel):
    def __init__(self, padre, gestorApuntes):
        super().__init__(padre)
        self.gestorApuntes = gestorApuntes
        self.lecturas = []
        self.idApunte = None
        self.documento = None
        self.pagina = 0
        self.title("Lecturas y apuntes")
        self.geometry("1050x760")
        self.configure(bg=COLOR_FONDO)
        self.protocol("WM_DELETE_WINDOW", self.cerrar)

        tk.Label(self, text="Lecturas y apuntes", font=FUENTE_TITULO,
                 bg=COLOR_PRIMARIO, fg=COLOR_FONDO).pack(fill="x", pady=(0, 8))
        importar = tk.Frame(self, bg=COLOR_FONDO)
        importar.pack(fill="x", padx=16)
        tk.Label(importar, text="Título:", bg=COLOR_FONDO, font=FUENTE_NORMAL).pack(side="left")
        self.tituloLectura = tk.Entry(importar, font=FUENTE_NORMAL)
        self.tituloLectura.pack(side="left", fill="x", expand=True, padx=8)
        self.crearBoton(importar, "Importar PDF", self.importarLectura).pack(side="left")

        tk.Label(self, text="Lectura del PDF y del apunte:", bg=COLOR_FONDO,
                 font=FUENTE_NORMAL).pack(anchor="w", padx=16, pady=(8, 0))
        self.selectorLectura = ttk.Combobox(self, state="readonly", font=FUENTE_NORMAL)
        self.selectorLectura.pack(fill="x", padx=16, pady=4)
        self.selectorLectura.bind("<<ComboboxSelected>>", self.abrirLectura)

        paneles = tk.Frame(self, bg=COLOR_FONDO)
        paneles.pack(fill="both", expand=True, padx=16, pady=8)
        visor = tk.Frame(paneles)
        visor.pack(side="left", fill="both", expand=True)
        self.lienzo = tk.Canvas(visor, bg="white", width=480, height=330)
        vertical = ttk.Scrollbar(visor, command=self.lienzo.yview)
        horizontal = ttk.Scrollbar(visor, orient="horizontal", command=self.lienzo.xview)
        self.lienzo.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        horizontal.pack(side="bottom", fill="x")
        vertical.pack(side="right", fill="y")
        self.lienzo.pack(fill="both", expand=True)

        editor = tk.Frame(paneles, bg=COLOR_FONDO)
        editor.pack(side="left", fill="both", expand=True, padx=(12, 0))
        tk.Label(editor, text="Fecha de clase (AAAA-MM-DD):", bg=COLOR_FONDO,
                 font=FUENTE_NORMAL).pack(anchor="w")
        self.fechaClase = tk.Entry(editor, font=FUENTE_NORMAL)
        self.fechaClase.pack(fill="x", pady=4)
        self.textoApunte = ScrolledText(editor, width=38, height=10, wrap="word", font=FUENTE_NORMAL)
        self.textoApunte.pack(fill="both", expand=True)
        acciones = tk.Frame(editor, bg=COLOR_FONDO)
        acciones.pack(fill="x", pady=6)
        self.crearBoton(acciones, "Guardar apunte", self.guardarApunte).pack(side="left")
        self.crearBoton(acciones, "Nuevo apunte", self.nuevoApunte).pack(side="left", padx=8)

        paginas = tk.Frame(self, bg=COLOR_FONDO)
        paginas.pack(fill="x", padx=16)
        self.crearBoton(paginas, "Anterior", lambda: self.cambiarPagina(-1)).pack(side="left")
        self.etiquetaPagina = tk.Label(paginas, text="Sin PDF", bg=COLOR_FONDO, font=FUENTE_NORMAL)
        self.etiquetaPagina.pack(side="left", padx=12)
        self.crearBoton(paginas, "Siguiente", lambda: self.cambiarPagina(1)).pack(side="left")

        filtros = tk.Frame(self, bg=COLOR_FONDO)
        filtros.pack(fill="x", padx=16, pady=8)
        tk.Label(filtros, text="Filtrar por fecha:", bg=COLOR_FONDO).pack(side="left")
        self.fechaFiltro = tk.Entry(filtros, width=12)
        self.fechaFiltro.pack(side="left", padx=6)
        self.selectorFiltro = ttk.Combobox(filtros, state="readonly", width=30)
        self.selectorFiltro.pack(side="left", fill="x", expand=True, padx=6)
        self.crearBoton(filtros, "Filtrar", self.actualizarApuntes).pack(side="left")
        self.crearBoton(filtros, "Ver todos", self.limpiarFiltros).pack(side="left", padx=6)

        tk.Label(self, text="Apuntes guardados: doble clic para editar", bg=COLOR_FONDO,
                 font=FUENTE_NORMAL).pack(anchor="w", padx=16)
        tabla = tk.Frame(self)
        tabla.pack(fill="x", padx=16, pady=(4, 12))
        self.tablaApuntes = ttk.Treeview(tabla, columns=("fecha", "dia", "lectura", "texto"),
                                        show="headings", height=5, selectmode="browse")
        for columna, titulo, ancho in (("fecha", "Fecha", 100), ("dia", "Día", 100),
                                      ("lectura", "Lectura", 230), ("texto", "Apunte", 450)):
            self.tablaApuntes.heading(columna, text=titulo)
            self.tablaApuntes.column(columna, width=ancho)
        barra = ttk.Scrollbar(tabla, command=self.tablaApuntes.yview)
        self.tablaApuntes.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tablaApuntes.pack(side="left", fill="x", expand=True)
        self.tablaApuntes.bind("<Double-1>", self.seleccionarApunte)
        self.nuevoApunte()
        try:
            self.actualizarLecturas()
            self.actualizarApuntes()
        except Exception as error:
            messagebox.showerror("Lecturas y apuntes", str(error), parent=self)

    def crearBoton(self, padre, texto, comando):
        return tk.Button(padre, text=texto, command=comando, font=FUENTE_BOTON,
                         bg=COLOR_PRIMARIO, fg=COLOR_FONDO, relief="flat", padx=10, pady=5)

    def idLectura(self, selector):
        indice = selector.current() - (1 if selector is self.selectorFiltro else 0)
        return self.lecturas[indice]["id"] if 0 <= indice < len(self.lecturas) else None

    def actualizarLecturas(self, idSeleccionado=None):
        self.lecturas = self.gestorApuntes.listarLecturas()
        opciones = [f"{numero}. {lectura['titulo']}" for numero, lectura in enumerate(self.lecturas, 1)]
        self.selectorLectura.configure(values=opciones)
        self.selectorFiltro.configure(values=["Todas las lecturas"] + opciones)
        self.selectorFiltro.current(0)
        for indice, lectura in enumerate(self.lecturas):
            if lectura["id"] == idSeleccionado:
                self.selectorLectura.current(indice)

    def importarLectura(self):
        ruta = filedialog.askopenfilename(parent=self, filetypes=[("Documentos PDF", "*.pdf")])
        if not ruta:
            return
        try:
            # Conservar la asociación del apunte aunque cambie el orden de las lecturas.
            seleccion = self.idLectura(self.selectorLectura)
            lectura = self.gestorApuntes.agregarLectura(self.tituloLectura.get(), ruta)
            self.actualizarLecturas(seleccion or lectura["id"])
            self.tituloLectura.delete(0, "end")
            self.abrirLectura()
        except Exception as error:
            messagebox.showerror("Importar PDF", str(error), parent=self)

    def abrirLectura(self, evento=None):
        if self.documento is not None:
            self.documento.close()
            self.documento = None
        self.lienzo.delete("all")
        self.etiquetaPagina.config(text="Sin PDF")
        try:
            ruta = self.gestorApuntes.obtenerRutaPdf(self.idLectura(self.selectorLectura))
            self.documento = pymupdf.open(str(ruta))
            self.pagina = 0
            self.cambiarPagina(0)
        except Exception as error:
            messagebox.showerror("Abrir PDF", str(error), parent=self)

    def cambiarPagina(self, cambio):
        if self.documento is None or not 0 <= self.pagina + cambio < len(self.documento):
            return
        nuevaPagina = self.pagina + cambio
        try:
            imagen = self.documento[nuevaPagina].get_pixmap(alpha=False)
            imagenPagina = tk.PhotoImage(master=self, data=imagen.tobytes("png"))
        except Exception as error:
            messagebox.showerror("Mostrar página", str(error), parent=self)
            return
        self.pagina = nuevaPagina
        self.imagenPagina = imagenPagina
        self.lienzo.delete("all")
        self.lienzo.create_image(0, 0, anchor="nw", image=self.imagenPagina)
        self.lienzo.config(scrollregion=self.lienzo.bbox("all"))
        self.lienzo.yview_moveto(0)
        self.etiquetaPagina.config(text=f"Página {self.pagina + 1} de {len(self.documento)}")

    def nuevoApunte(self):
        if hasattr(self, "guardado") and not self.confirmarCierre():
            return
        self.idApunte = None
        self.fechaClase.delete(0, "end")
        self.fechaClase.insert(0, date.today().isoformat())
        self.textoApunte.delete("1.0", "end")
        self.guardado = self.contenidoEditor()

    def contenidoEditor(self):
        return (self.textoApunte.get("1.0", "end-1c"), self.fechaClase.get(),
                self.idLectura(self.selectorLectura))

    def guardarApunte(self):
        try:
            datos = (self.textoApunte.get("1.0", "end-1c"), self.fechaClase.get().strip(),
                     self.idLectura(self.selectorLectura))
            if self.idApunte is None:
                apunte = self.gestorApuntes.registrarApunte(*datos)
            else:
                apunte = self.gestorApuntes.editarApunte(self.idApunte, *datos)
            self.idApunte = apunte["id"]
            self.guardado = self.contenidoEditor()
            self.actualizarApuntes()
            messagebox.showinfo("Apuntes", "Apunte guardado.", parent=self)
        except Exception as error:
            messagebox.showerror("Guardar apunte", str(error), parent=self)

    def seleccionarApunte(self, evento):
        seleccionado = self.tablaApuntes.identify_row(evento.y)
        if not seleccionado or not self.confirmarCierre():
            return
        apunte = self.apuntes[seleccionado]
        self.idApunte = apunte["id"]
        self.fechaClase.delete(0, "end")
        self.fechaClase.insert(0, apunte["fechaClase"])
        self.textoApunte.delete("1.0", "end")
        self.textoApunte.insert("1.0", apunte["texto"])
        self.selectorLectura.set("")
        for indice, lectura in enumerate(self.lecturas):
            if lectura["id"] == apunte["idLectura"]:
                self.selectorLectura.current(indice)
        self.guardado = self.contenidoEditor()
        self.abrirLectura()

    def actualizarApuntes(self):
        try:
            apuntes = self.gestorApuntes.listarApuntes(
                self.fechaFiltro.get().strip() or None, self.idLectura(self.selectorFiltro))
            self.apuntes = {apunte["id"]: apunte for apunte in apuntes}
            self.tablaApuntes.delete(*self.tablaApuntes.get_children())
            for apunte in apuntes:
                self.tablaApuntes.insert("", "end", iid=apunte["id"], values=(
                    apunte["fechaClase"], apunte["diaClase"], apunte["tituloLectura"],
                    " ".join(apunte["texto"].split())[:100]))
        except Exception as error:
            messagebox.showerror("Consultar apuntes", str(error), parent=self)

    def limpiarFiltros(self):
        self.fechaFiltro.delete(0, "end")
        self.selectorFiltro.current(0)
        self.actualizarApuntes()

    def confirmarCierre(self):
        if self.idApunte is None and not self.textoApunte.get("1.0", "end-1c").strip():
            return True
        return self.contenidoEditor() == self.guardado or messagebox.askokcancel(
            "Cambios sin guardar", "Hay cambios sin guardar. ¿Deseas descartarlos?", parent=self)

    def cerrar(self):
        if self.confirmarCierre():
            self.destroy()

    def destroy(self):
        if self.documento is not None:
            self.documento.close()
        super().destroy()
