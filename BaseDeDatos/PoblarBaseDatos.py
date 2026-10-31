from datetime import date
import firebase_admin
from firebase_admin import credentials
from modelos.GestorPenalizaciones import GestorPenalizaciones

RUTA_CREDENCIALES = "Credenciales.json"
URL_BASE_DATOS = "https://proyecto-aula-clases-default-rtdb.firebaseio.com/"

PENALIZACIONES_DE_PRUEBA = [
    {"fechaTarde": date(2026, 10, 21), "cumplida": True},   # miércoles
    {"fechaTarde": date(2026, 10, 23), "cumplida": False},  # viernes
    {"fechaTarde": date(2026, 10, 27), "cumplida": False},  # martes
    {"fechaTarde": date(2026, 10, 30), "cumplida": False},  # viernes
]

credencial = credentials.Certificate(RUTA_CREDENCIALES)
firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})

gestorPenalizaciones = GestorPenalizaciones()

for penalizacionPrueba in PENALIZACIONES_DE_PRUEBA:
    gestorPenalizaciones.penalizacion.registrarLlegadaTarde(penalizacionPrueba["fechaTarde"])

fechasCumplidas = [penalizacionPrueba["fechaTarde"].isoformat()
                   for penalizacionPrueba in PENALIZACIONES_DE_PRUEBA
                   if penalizacionPrueba["cumplida"]]

for penalizacion in gestorPenalizaciones.listarPenalizaciones():
    if penalizacion["fechaTarde"] in fechasCumplidas:
        gestorPenalizaciones.marcarComoCumplida(penalizacion["id"])

print("Base de datos poblada")