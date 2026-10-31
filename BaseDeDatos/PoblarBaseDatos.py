import os
import sys
from datetime import date

import firebase_admin
from firebase_admin import credentials, db

CARPETA_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(CARPETA_PROYECTO)

from Modelos.GestorPenalizaciones import GestorPenalizaciones

RUTA_CREDENCIALES = os.path.join(CARPETA_PROYECTO, "Credenciales.json")

URL_BASE_DATOS = "https://proyecto-aula-clases-default-rtdb.firebaseio.com/"

PENALIZACIONES_DE_PRUEBA = [
    {"fechaTarde": date(2026, 10, 21), "cumplida": True},
    {"fechaTarde": date(2026, 10, 23), "cumplida": False},
    {"fechaTarde": date(2026, 10, 27), "cumplida": False},
    {"fechaTarde": date(2026, 10, 30), "cumplida": False},
]

credencial = credentials.Certificate(RUTA_CREDENCIALES)
firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})

db.reference("/").delete()

gestorPenalizaciones = GestorPenalizaciones()

for penalizacionPrueba in PENALIZACIONES_DE_PRUEBA:
    gestorPenalizaciones.penalizacion.registrarLlegadaTarde(
        penalizacionPrueba["fechaTarde"]
    )

fechasCumplidas = [
    penalizacionPrueba["fechaTarde"].isoformat()
    for penalizacionPrueba in PENALIZACIONES_DE_PRUEBA
    if penalizacionPrueba["cumplida"]
]

for penalizacion in gestorPenalizaciones.listarPenalizaciones():
    if penalizacion["fechaTarde"] in fechasCumplidas:
        gestorPenalizaciones.marcarComoCumplida(penalizacion["id"])

print("Base de datos poblada")