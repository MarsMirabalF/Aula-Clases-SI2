# Guía de aprendizaje: TDD, XP y participación

## 1. Propósito

Este documento explica TDD, Extreme Programming, programación en parejas y la implementación de la Historia de Usuario de participación en clase.

La parte desarrollada se encuentra en:

- modelos/PreguntaClase.py
- modelos/Participacion.py
- modelos/HistorialParticipacion.py
- modelos/GestorParticipacion.py
- Vistas/PantallaParticipacion.py
- Vistas/PantallaHistorialParticipacion.py
- Pruebas/PruebasParticipacion/

## 2. TDD

TDD significa Test-Driven Development, o desarrollo guiado por pruebas. La idea es escribir primero una prueba que describa el comportamiento esperado y luego implementar el código necesario.

El ciclo tiene tres pasos:

1. Rojo: la prueba falla porque todavía no existe la solución.
2. Verde: se escribe la solución mínima para que la prueba pase.
3. Refactor: se mejora el código sin cambiar el comportamiento.

En esta parte del proyecto las pruebas describen que se debe mostrar una pregunta, guardar una respuesta correcta o incorrecta, consultar el historial y contar resultados.

TDD no significa probar únicamente al final. Cada prueba sirve como una especificación pequeña del comportamiento del sistema.

## 3. XP y programación en parejas

XP significa Extreme Programming. Es una metodología ágil basada en comunicación, retroalimentación, entregas pequeñas, pruebas, diseño simple y mejora continua.

Conceptos usados en los diagramas:

- Historia de usuario: necesidad expresada desde el punto de vista del usuario.
- Prueba de aceptación: comprueba que la historia cumple lo esperado.
- Programación en parejas: dos personas trabajan sobre la misma tarea.
- Piloto: escribe el código.
- Navegante o copiloto: revisa la lógica, piensa en errores y propone mejoras.
- Refactorización: mejora la estructura sin cambiar el resultado.

TDD es una práctica técnica. XP es una metodología más amplia que puede incluir TDD, historias de usuario y programación en parejas.

## 4. Historia de usuario

Yo como estudiante de Sistemas de Información 2 quiero participar respondiendo las preguntas del ingeniero y visualizar una reacción según mi respuesta sea correcta o incorrecta, para simular la dinámica del aula y registrar mis participaciones.

La aplicación permite:

- mostrar preguntas básicas de UML, Scrum y XP;
- pulsar Participar;
- seleccionar Correcta o Incorrecta;
- mostrar Bien o Date un golpe;
- guardar pregunta, fecha y resultado;
- pasar a otra pregunta;
- consultar el historial y los contadores.

## 5. Organización del código

~~~text
modelos/
    PreguntaClase.py
    Participacion.py
    HistorialParticipacion.py
    GestorParticipacion.py

Vistas/
    PantallaParticipacion.py
    PantallaHistorialParticipacion.py

Pruebas/PruebasParticipacion/
    BaseDatosFalsa.py
    PruebaCriterio1MostrarPregunta.py
    PruebaCriterio2RegistrarRespuestaCorrecta.py
    PruebaCriterio3RegistrarRespuestaIncorrecta.py
    PruebaCriterio4ConsultarHistorial.py
    PruebaCriterio5ContarResultados.py
~~~

El modelo contiene datos y reglas. El gestor coordina los modelos. Las vistas muestran ventanas y tablas. Las pruebas comprueban comportamientos sin usar Firebase real.

## 6. PreguntaClase.py

Archivo: modelos/PreguntaClase.py

~~~python
class PreguntaClase:
    def __init__(self, texto):
        if not isinstance(texto, str) or not texto.strip():
            raise ValueError("La pregunta no puede estar vacía.")
        self.texto = texto.strip()

    def mostrarPregunta(self):
        return self.texto

    def obtenerPregunta(self):
        return self.texto
~~~

Explicación:

- class PreguntaClase declara la clase que representa una pregunta.
- __init__ recibe el texto al crear el objeto.
- isinstance comprueba que el texto sea una cadena.
- strip elimina espacios al inicio y al final.
- La condición rechaza textos vacíos.
- ValueError informa que la pregunta no es válida.
- self.texto guarda el texto limpio.
- mostrarPregunta devuelve el texto para la pantalla.
- obtenerPregunta devuelve el texto para el gestor.

La responsabilidad de esta clase es representar una pregunta válida.

## 7. Participacion.py

Archivo: modelos/Participacion.py

~~~python
from datetime import datetime

from firebase_admin import db


class Participacion:
    def registrar(self, pregunta, esCorrecta, fecha=None):
        if not isinstance(pregunta, str) or not pregunta.strip():
            raise ValueError("La participación debe tener una pregunta.")
        if not isinstance(esCorrecta, bool):
            raise ValueError("El resultado de la participación no es válido.")
        momento = fecha or datetime.now().astimezone()
        registro = {
            "pregunta": pregunta.strip(),
            "fecha": momento.isoformat(timespec="seconds"),
            "esCorrecta": esCorrecta,
        }
        referencia = db.reference("participaciones").push(registro)
        return {"id": referencia.key, **registro} if referencia is not None else registro
~~~

Explicación:

- datetime permite obtener fecha y hora.
- db permite conectarse a Firebase.
- Participacion representa una respuesta registrada.
- registrar recibe pregunta, resultado y opcionalmente fecha.
- La primera validación impide guardar una pregunta vacía.
- La segunda validación exige un booleano.
- momento usa la fecha recibida o la fecha actual.
- registro construye los datos que se guardarán.
- isoformat convierte la fecha a texto estándar.
- db.reference("participaciones") selecciona la colección.
- push guarda el registro y crea una clave automática.
- referencia.key obtiene esa clave.
- return devuelve el registro creado.

## 8. HistorialParticipacion.py

Archivo: modelos/HistorialParticipacion.py

~~~python
from datetime import datetime

from firebase_admin import db


class HistorialParticipacion:
    def guardar(self, participacion):
        db.reference("participaciones").push(participacion)

    def consultar(self):
        registros = db.reference("participaciones").get() or {}
        historial = []
        for identificador, registro in registros.items():
            fecha = datetime.fromisoformat(registro["fecha"])
            esCorrecta = bool(registro["esCorrecta"])
            historial.append({
                "id": identificador,
                "pregunta": registro["pregunta"],
                "fecha": fecha.strftime("%d/%m/%Y %H:%M"),
                "esCorrecta": esCorrecta,
                "resultado": "Correcta" if esCorrecta else "Incorrecta",
            })
        return sorted(historial, key=lambda registro: registro["fecha"], reverse=True)

    def contarCorrectas(self):
        return sum(registro["esCorrecta"] for registro in self.consultar())

    def contarIncorrectas(self):
        return sum(not registro["esCorrecta"] for registro in self.consultar())
~~~

Explicación:

- guardar inserta una participación en la misma colección.
- consultar obtiene todos los registros.
- or {} permite trabajar aunque la colección esté vacía.
- historial es la lista de salida.
- el for recorre identificador y datos.
- fromisoformat convierte la fecha guardada.
- bool normaliza el resultado.
- append prepara un registro para mostrar.
- strftime cambia la fecha a día/mes/año y hora.
- resultado traduce true a Correcta y false a Incorrecta.
- sorted ordena por fecha descendente.
- contarCorrectas suma los valores verdaderos.
- contarIncorrectas suma los valores falsos.

## 9. GestorParticipacion.py

Archivo: modelos/GestorParticipacion.py

~~~python
from modelos.HistorialParticipacion import HistorialParticipacion
from modelos.Participacion import Participacion
from modelos.PreguntaClase import PreguntaClase


class GestorParticipacion:
    PREGUNTAS = (
        "¿Qué representa un diagrama de clases en UML?",
        "¿Qué reunión de Scrum se realiza diariamente para revisar el avance del equipo?",
        "¿Qué práctica de XP consiste en programar en parejas?",
    )

    def __init__(self):
        self.participacion = Participacion()
        self.historial = HistorialParticipacion()

    def obtenerPregunta(self, indice=0):
        return PreguntaClase(self.PREGUNTAS[indice % len(self.PREGUNTAS)])

    def registrarParticipacion(self, pregunta, esCorrecta):
        return self.participacion.registrar(pregunta.obtenerPregunta(), esCorrecta)

    def listarParticipaciones(self):
        return self.historial.consultar()

    def contarCorrectas(self):
        return self.historial.contarCorrectas()

    def contarIncorrectas(self):
        return self.historial.contarIncorrectas()
~~~

Explicación:

- Las importaciones incorporan los tres modelos.
- GestorParticipacion es el punto de entrada de las vistas.
- PREGUNTAS contiene las tres preguntas.
- El constructor crea el objeto de registro y el objeto de historial.
- obtenerPregunta busca una pregunta por índice.
- El operador porcentaje hace que el índice vuelva al inicio.
- registrarParticipacion extrae el texto y delega el guardado.
- listarParticipaciones delega la consulta.
- contarCorrectas y contarIncorrectas delegan los conteos.

La vista no conoce Firebase; solo conoce al gestor.

## 10. PantallaParticipacion.py

Archivo: Vistas/PantallaParticipacion.py

La pantalla tiene este flujo:

~~~text
Abrir ventana
  -> mostrar pregunta
  -> pulsar Participar
  -> mostrar Correcta e Incorrecta
  -> registrar resultado
  -> mostrar mensaje
  -> pulsar Volver a participar
  -> cargar siguiente pregunta
~~~

Puntos principales:

~~~python
class PantallaParticipacion(tk.Toplevel):
~~~

Crea una ventana secundaria.

~~~python
def __init__(self, padre, gestorParticipacion):
    super().__init__(padre)
    self.gestorParticipacion = gestorParticipacion
    self.indicePregunta = 0
    self.pregunta = self.gestorParticipacion.obtenerPregunta(self.indicePregunta)
~~~

Inicializa la ventana, guarda el gestor y obtiene la primera pregunta.

~~~python
self.title("Participación en clase")
self.geometry("620x400")
self.configure(bg=COLOR_FONDO)
~~~

Configura título, tamaño y color.

~~~python
self.etiquetaPregunta = tk.Label(
    self, text=self.pregunta.mostrarPregunta(), font=FUENTE_NORMAL,
    bg=COLOR_FONDO, fg=COLOR_PRIMARIO, wraplength=540, justify="left")
~~~

Crea la etiqueta visible con la pregunta.

~~~python
self.botonParticipar = self.crearBoton("Participar", self.mostrarOpciones)
~~~

Crea el botón inicial y lo conecta con mostrarOpciones.

~~~python
self.botonCorrecta = self.crearBoton(
    "Correcta", lambda: self.registrarResultado(True))
self.botonIncorrecta = self.crearBoton(
    "Incorrecta", lambda: self.registrarResultado(False))
~~~

Los dos botones llaman al mismo método, enviando true o false.

~~~python
def mostrarOpciones(self):
    self.botonParticipar.config(state="disabled")
    self.marcoOpciones.pack(pady=8)
    self.botonCorrecta.pack(side="left", padx=4)
    self.botonIncorrecta.pack(side="left", padx=4)
~~~

Desactiva el botón inicial y muestra las opciones.

~~~python
def registrarResultado(self, esCorrecta):
    self.gestorParticipacion.registrarParticipacion(self.pregunta, esCorrecta)
    mensaje = "¡Bien!" if esCorrecta else "¡Date un golpe!"
    color = COLOR_PRIMARIO if esCorrecta else COLOR_ERROR
~~~

Guarda el resultado y selecciona mensaje y color.

~~~python
self.etiquetaEstado.config(text=mensaje, fg=color)
self.botonCorrecta.config(state="disabled")
self.botonIncorrecta.config(state="disabled")
self.botonNuevaParticipacion.pack(padx=24, pady=8)
~~~

Muestra el resultado, bloquea una segunda respuesta y muestra el botón para continuar.

~~~python
def volverAParticipar(self):
    self.indicePregunta += 1
    self.pregunta = self.gestorParticipacion.obtenerPregunta(self.indicePregunta)
    self.etiquetaPregunta.config(text=self.pregunta.mostrarPregunta())
~~~

Avanza el índice y cambia la pregunta.

~~~python
self.botonCorrecta.pack_forget()
self.botonIncorrecta.pack_forget()
self.marcoOpciones.pack_forget()
self.botonNuevaParticipacion.pack_forget()
~~~

Oculta los controles anteriores.

~~~python
self.botonParticipar.config(state="normal")
self.botonCorrecta.config(state="normal")
self.botonIncorrecta.config(state="normal")
~~~

Habilita los botones para la nueva pregunta. Estas líneas corrigieron el bug donde las respuestas quedaban bloqueadas al volver a participar.

## 11. PantallaHistorialParticipacion.py

Archivo: Vistas/PantallaHistorialParticipacion.py

La ventana utiliza ttk.Treeview con tres columnas: pregunta, fecha y resultado.

- tkinter crea la ventana.
- ttk proporciona la tabla.
- ttk.Style define colores, fuentes y selección.
- Treeview crea la tabla.
- heading coloca los títulos.
- column define tamaños y alineación.
- tag_configure pinta correctas e incorrectas.
- actualizarTabla carga los datos al abrir.

El núcleo de la tabla es:

~~~python
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
~~~

- delete elimina filas anteriores.
- listarParticipaciones obtiene la información preparada por el historial.
- insert agrega cada fila.
- iid usa la clave de Firebase.
- values coloca pregunta, fecha y resultado.
- los contadores actualizan el resumen.

El botón Actualizar fue retirado, pero el método permanece porque la tabla necesita cargar datos al abrirse.

## 12. Integración

En Principal.py:

~~~python
from modelos.GestorParticipacion import GestorParticipacion
~~~

Importa el gestor.

~~~python
pantallaInicio = PantallaInicio(
    ventana, GestorPenalizaciones(), GestorApuntes(), GestorParticipacion())
~~~

Crea y entrega el gestor a Inicio.

En PantallaInicio.py:

~~~python
from Vistas.PantallaParticipacion import PantallaParticipacion
from Vistas.PantallaHistorialParticipacion import PantallaHistorialParticipacion
~~~

Importa las dos ventanas.

~~~python
def abrirParticipacion(self):
    PantallaParticipacion(self.padre, self.gestorParticipacion)

def abrirHistorialParticipacion(self):
    PantallaHistorialParticipacion(self.padre, self.gestorParticipacion)
~~~

Estos métodos se ejecutan desde los botones de Inicio.

## 13. Firebase

La ruta usada es:

~~~text
participaciones
~~~

Ejemplo:

~~~json
{
  "participaciones": {
    "-N123abc": {
      "pregunta": "¿Qué representa un diagrama de clases en UML?",
      "fecha": "2026-11-02T15:30:20-04:00",
      "esCorrecta": true
    }
  }
}
~~~

Firebase crea automáticamente la clave cuando se usa push.

| Campo | Tipo | Significado |
|---|---|---|
| pregunta | texto | Pregunta respondida. |
| fecha | texto ISO | Fecha, hora y zona horaria. |
| esCorrecta | booleano | true correcta, false incorrecta. |

No se crean tablas separadas para correctas e incorrectas. Todo se guarda en participaciones y se cuenta al consultar.

## 14. Pruebas

Carpeta: Pruebas/PruebasParticipacion

### BaseDatosFalsa.py

ReferenciaFalsa imita get, push y key. crearGestorConBaseFalsa usa patch para reemplazar temporalmente la referencia Firebase. Por eso las pruebas trabajan con un diccionario y no modifican la base real.

### PruebaCriterio1MostrarPregunta.py

Obtiene una pregunta, comprueba que no esté vacía y verifica que incluya UML.

### PruebaCriterio2RegistrarRespuestaCorrecta.py

Registra true, consulta el historial y comprueba pregunta y resultado.

### PruebaCriterio3RegistrarRespuestaIncorrecta.py

Registra false y verifica que el resultado sea Incorrecta.

### PruebaCriterio4ConsultarHistorial.py

Guarda una correcta y una incorrecta. Comprueba que haya dos registros, dos resultados diferentes y fechas.

### PruebaCriterio5ContarResultados.py

Guarda dos correctas y una incorrecta. Comprueba los conteos 2 y 1.

Ejecutar todas las pruebas:

~~~bash
python -m unittest discover -s Pruebas/PruebasParticipacion -p "*.py"
~~~

Resultado esperado:

~~~text
.....
----------------------------------------------------------------------
Ran 5 tests

OK
~~~

Ejecutar una sola:

~~~bash
python -m unittest Pruebas.PruebasParticipacion.PruebaCriterio1MostrarPregunta
~~~

Para otra prueba se cambia el nombre final del módulo.

## 15. Flujo completo

~~~text
Participar
  -> PantallaParticipacion.mostrarOpciones()
  -> registrarResultado(True o False)
  -> GestorParticipacion.registrarParticipacion()
  -> Participacion.registrar()
  -> participaciones.push(registro)
  -> Firebase guarda

Abrir historial
  -> GestorParticipacion.listarParticipaciones()
  -> HistorialParticipacion.consultar()
  -> participaciones.get()
  -> tabla y contadores
~~~

## 16. Fuentes de los diagramas

### TDD

Kent Beck. *Test-Driven Development: By Example*. Addison-Wesley, 2003.

El diagrama de TDD se basó en escribir primero la prueba, hacer pasar la prueba y refactorizar. También se tomó el ciclo rojo, verde y refactor.

### XP

Gregorio Robles Martínez y Jorge Ferrer Zarzuela. *Programación eXtrema y Software Libre*. Universidad Rey Juan Carlos y Universidad Politécnica de Madrid, 2002.

Los diagramas de XP se basaron en historias de usuario, cliente, programador, pruebas de aceptación y programación en parejas.

### UML

Grady Booch, James Rumbaugh e Ivar Jacobson. *El lenguaje unificado de modelado. Manual de referencia. Segunda edición*.

De este libro se tomó la representación de clases con nombre, atributos, operaciones, relaciones y multiplicidades.

## 17. Relación de los diagramas

- TDD: requisito, ciclo TDD, prueba unitaria y código fuente.
- Historia de usuario en XP: cliente, historia, programador y prueba de aceptación.
- Programación en parejas en XP: pareja, sesión, programadores y código fuente.
- CRC: sesión CRC, tarjeta, responsabilidades y colaboradores.

Los diagramas son conceptuales y no representan las clases específicas de participación.

## 18. Orden para estudiar

1. Leer la historia de usuario.
2. Ejecutar una prueba individual.
3. Estudiar PreguntaClase.py.
4. Estudiar Participacion.py.
5. Estudiar HistorialParticipacion.py.
6. Estudiar GestorParticipacion.py.
7. Seguir los botones de PantallaParticipacion.py.
8. Estudiar PantallaHistorialParticipacion.py.
9. Revisar la estructura Firebase.
10. Ejecutar las cinco pruebas.
11. Relacionar cada prueba con rojo, verde y refactor.
12. Revisar los diagramas.

La idea principal es seguir un dato completo: la pregunta se crea, recibe una respuesta, se convierte en un registro, se guarda en participaciones, se consulta y aparece en el historial.
+

# Anexo A: código completo de las vistas y pruebas

## A.1. PantallaParticipacion.py

Archivo: Vistas/PantallaParticipacion.py

~~~python
import tkinter as tk

from estilos import *


class PantallaParticipacion(tk.Toplevel):
    def __init__(self, padre, gestorParticipacion):
        super().__init__(padre)
        self.gestorParticipacion = gestorParticipacion
        self.indicePregunta = 0
        self.pregunta = self.gestorParticipacion.obtenerPregunta(self.indicePregunta)
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
        self.etiquetaEstado.pack(anchor="w", padx=24, pady=(20, 8))

        self.botonNuevaParticipacion = self.crearBoton(
            "Volver a participar", self.volverAParticipar, self)
        self.botonNuevaParticipacion.pack(padx=24, pady=8)
        self.botonNuevaParticipacion.pack_forget()

    def crearBoton(self, texto, comando, padre=None):
        contenedor = padre or (self.marcoOpciones if hasattr(self, "marcoOpciones") else self)
        return tk.Button(
            contenedor,
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
        self.botonNuevaParticipacion.pack(padx=24, pady=8)

    def volverAParticipar(self):
        self.indicePregunta += 1
        self.pregunta = self.gestorParticipacion.obtenerPregunta(self.indicePregunta)
        self.etiquetaPregunta.config(text=self.pregunta.mostrarPregunta())
        self.etiquetaEstado.config(text="", fg=COLOR_PRIMARIO)
        self.botonCorrecta.pack_forget()
        self.botonIncorrecta.pack_forget()
        self.marcoOpciones.pack_forget()
        self.botonNuevaParticipacion.pack_forget()
        self.botonParticipar.config(state="normal")
        self.botonCorrecta.config(state="normal")
        self.botonIncorrecta.config(state="normal")
~~~

## A.2. PantallaHistorialParticipacion.py

Archivo: Vistas/PantallaHistorialParticipacion.py

~~~python
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
~~~

## A.3. BaseDatosFalsa.py

Archivo: Pruebas/PruebasParticipacion/BaseDatosFalsa.py

~~~python
from unittest.mock import patch

from modelos.GestorParticipacion import GestorParticipacion


class ReferenciaFalsa:
    def __init__(self, registros, ruta):
        self.registros = registros
        self.ruta = ruta
        self.key = None

    def get(self):
        return self.registros.get(self.ruta) or None

    def push(self, datos):
        participaciones = self.registros.setdefault(self.ruta, {})
        self.key = "id" + str(len(participaciones) + 1)
        participaciones[self.key] = datos
        return self


def crearGestorConBaseFalsa(prueba):
    registros = {}
    parche = patch(
        "firebase_admin.db.reference",
        side_effect=lambda ruta: ReferenciaFalsa(registros, ruta))
    parche.start()
    prueba.addCleanup(parche.stop)
    return GestorParticipacion()
~~~

## A.4. PruebaCriterio1MostrarPregunta.py

~~~python
import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio1MostrarPregunta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testMuestraUnaPreguntaDeLaClase(self):
        pregunta = self.gestor.obtenerPregunta()

        self.assertTrue(pregunta.obtenerPregunta())
        self.assertIn("UML", pregunta.obtenerPregunta())


if __name__ == "__main__":
    unittest.main()
~~~

## A.5. PruebaCriterio2RegistrarRespuestaCorrecta.py

~~~python
import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio2RegistrarRespuestaCorrecta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testRegistraUnaRespuestaCorrecta(self):
        pregunta = self.gestor.obtenerPregunta()

        self.gestor.registrarParticipacion(pregunta, True)

        participacion = self.gestor.listarParticipaciones()[0]
        self.assertEqual(participacion["pregunta"], pregunta.obtenerPregunta())
        self.assertTrue(participacion["esCorrecta"])


if __name__ == "__main__":
    unittest.main()
~~~

## A.6. PruebaCriterio3RegistrarRespuestaIncorrecta.py

~~~python
import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio3RegistrarRespuestaIncorrecta(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testRegistraUnaRespuestaIncorrecta(self):
        pregunta = self.gestor.obtenerPregunta(1)

        self.gestor.registrarParticipacion(pregunta, False)

        participacion = self.gestor.listarParticipaciones()[0]
        self.assertEqual(participacion["resultado"], "Incorrecta")
        self.assertFalse(participacion["esCorrecta"])


if __name__ == "__main__":
    unittest.main()
~~~

## A.7. PruebaCriterio4ConsultarHistorial.py

~~~python
import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio4ConsultarHistorial(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testConsultaLasParticipacionesRealizadas(self):
        primera = self.gestor.obtenerPregunta(0)
        segunda = self.gestor.obtenerPregunta(1)
        self.gestor.registrarParticipacion(primera, True)
        self.gestor.registrarParticipacion(segunda, False)

        historial = self.gestor.listarParticipaciones()

        self.assertEqual(len(historial), 2)
        self.assertEqual({registro["resultado"] for registro in historial},
                         {"Correcta", "Incorrecta"})
        self.assertTrue(all(registro["fecha"] for registro in historial))


if __name__ == "__main__":
    unittest.main()
~~~

## A.8. PruebaCriterio5ContarResultados.py

~~~python
import unittest

from Pruebas.PruebasParticipacion.BaseDatosFalsa import crearGestorConBaseFalsa


class PruebaCriterio5ContarResultados(unittest.TestCase):
    def setUp(self):
        self.gestor = crearGestorConBaseFalsa(self)

    def testCuentaRespuestasCorrectasEIncorrectas(self):
        pregunta = self.gestor.obtenerPregunta()
        self.gestor.registrarParticipacion(pregunta, True)
        self.gestor.registrarParticipacion(pregunta, True)
        self.gestor.registrarParticipacion(pregunta, False)

        self.assertEqual(self.gestor.contarCorrectas(), 2)
        self.assertEqual(self.gestor.contarIncorrectas(), 1)


if __name__ == "__main__":
    unittest.main()
~~~

## A.9. Cómo leer una prueba

Todas siguen el mismo patrón:

1. importan unittest;
2. importan el creador de la base falsa;
3. crean el gestor en setUp;
4. preparan datos;
5. ejecutan una operación;
6. comprueban el resultado con assert;
7. detienen el archivo con unittest.main.

En TDD, el método de prueba expresa primero el comportamiento que se espera del modelo.

# Anexo B: palabras que debes poder explicar

- Clase: molde que define datos y operaciones.
- Objeto: instancia concreta de una clase.
- Atributo: dato guardado dentro del objeto.
- Método: función perteneciente a una clase.
- Constructor: método __init__ que prepara un objeto.
- Booleano: valor True o False.
- Diccionario: estructura de pares clave y valor.
- Lista: colección ordenada de elementos.
- Firebase reference: referencia a una ruta de la base.
- push: inserta datos con una clave automática.
- get: lee datos.
- patch: reemplaza temporalmente una dependencia durante una prueba.
- assert: comprobación que hace fallar la prueba si no se cumple.

