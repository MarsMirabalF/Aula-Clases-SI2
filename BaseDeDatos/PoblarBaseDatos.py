import os
import sys
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

import firebase_admin
from firebase_admin import credentials, db

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(CARPETA_PROYECTO)

from modelos.GestorPenalizaciones import GestorPenalizaciones
from modelos.GestorApuntes import GestorApuntes

RUTA_CREDENCIALES = os.path.join(CARPETA_PROYECTO, "Credenciales.json")

URL_BASE_DATOS = "https://proyecto-aula-clases-default-rtdb.firebaseio.com/"

PENALIZACIONES_DE_PRUEBA = [
    {"fechaTarde": date(2026, 10, 21), "cumplida": True},
    {"fechaTarde": date(2026, 10, 23), "cumplida": False},
    {"fechaTarde": date(2026, 10, 27), "cumplida": False},
    {"fechaTarde": date(2026, 10, 30), "cumplida": False},
]

LECTURAS_DE_PRUEBA = [
    {
        "titulo": "[Ejemplo] Requisitos de software",
        "paginas": [
            "Un requisito describe una necesidad que el sistema debe satisfacer. "
            "Los criterios de aceptacion permiten comprobar el comportamiento esperado.",
            "Ejemplo: el estudiante puede guardar un apunte y consultarlo despues. "
            "Comprobamos que el texto, la fecha y la lectura se conserven.",
        ],
    },
    {
        "titulo": "[Ejemplo] Tarjetas CRC",
        "paginas": [
            "Una tarjeta CRC identifica una clase, sus responsabilidades y sus colaboradores. "
            "Las responsabilidades describen lo que conoce y hace la clase.",
            "Ejemplo: Apunte guarda el texto y la fecha de clase, y colabora con Lectura. "
            "GestorApuntes organiza los apuntes para que PantallaLectura los presente.",
        ],
    },
]

APUNTES_DE_PRUEBA = [
    {
        "tituloLectura": "[Ejemplo] Requisitos de software",
        "fechaClase": "2026-10-27",
        "texto": "Los criterios de aceptación deben poder comprobarse mediante pruebas.",
    },
    {
        "tituloLectura": "[Ejemplo] Requisitos de software",
        "fechaClase": "2026-10-28",
        "texto": "Guardar un apunte implica conservar el texto, la fecha y su lectura relacionada.",
    },
    {
        "tituloLectura": "[Ejemplo] Tarjetas CRC",
        "fechaClase": "2026-10-30",
        "texto": "Cada clase tiene responsabilidades concretas y colabora con otras clases.",
    },
]


def poblarPenalizaciones():
    # Conservar el trabajo de Marcelo y cualquier penalización ya registrada.
    if db.reference("penalizaciones").get():
        print("Penalizaciones existentes conservadas")
        return

    gestor = GestorPenalizaciones()
    for ejemplo in PENALIZACIONES_DE_PRUEBA:
        gestor.penalizacion.registrarLlegadaTarde(ejemplo["fechaTarde"])

    fechasCumplidas = {
        ejemplo["fechaTarde"].isoformat()
        for ejemplo in PENALIZACIONES_DE_PRUEBA if ejemplo["cumplida"]
    }
    for penalizacion in gestor.listarPenalizaciones():
        if penalizacion["fechaTarde"] in fechasCumplidas:
            gestor.marcarComoCumplida(penalizacion["id"])


def crearPdfEjemplo(ruta, ejemplo):
    import pymupdf

    with pymupdf.open() as documento:
        for numero, texto in enumerate(ejemplo["paginas"], start=1):
            pagina = documento.new_page()
            pagina.insert_text((50, 60), ejemplo["titulo"], fontsize=18)
            pagina.insert_textbox((50, 105, 540, 700), texto, fontsize=13)
            pagina.insert_text((50, 780), f"Material de demostracion - Pagina {numero}", fontsize=10)
        documento.save(str(ruta))


def poblarLecturasYApuntes(carpetaProyecto=None):
    gestor = GestorApuntes(carpetaProyecto)
    lecturas = {lectura["titulo"]: lectura for lectura in gestor.listarLecturas()}

    with TemporaryDirectory() as carpetaTemporal:
        for indice, ejemplo in enumerate(LECTURAS_DE_PRUEBA):
            if ejemplo["titulo"] not in lecturas:
                ruta = Path(carpetaTemporal) / f"lectura_{indice}.pdf"
                crearPdfEjemplo(ruta, ejemplo)
                lecturas[ejemplo["titulo"]] = gestor.agregarLectura(ejemplo["titulo"], ruta)

    existentes = {
        (apunte["idLectura"], apunte["fechaClase"], apunte["texto"])
        for apunte in gestor.listarApuntes()
    }
    for ejemplo in APUNTES_DE_PRUEBA:
        idLectura = lecturas[ejemplo["tituloLectura"]]["id"]
        clave = (idLectura, ejemplo["fechaClase"], ejemplo["texto"])
        if clave not in existentes:
            gestor.registrarApunte(ejemplo["texto"], ejemplo["fechaClase"], idLectura)
            existentes.add(clave)


if __name__ == "__main__":
    credencial = credentials.Certificate(RUTA_CREDENCIALES)
    firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})
    poblarLecturasYApuntes()
    poblarPenalizaciones()
    print("Datos de ejemplo disponibles. Se conservaron los registros existentes.")
