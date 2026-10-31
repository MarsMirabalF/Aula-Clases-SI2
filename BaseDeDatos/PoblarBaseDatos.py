from datetime import date
import firebase_admin
from firebase_admin import credentials
from modelos.GestorPenalizaciones import GestorPenalizaciones

RUTA_CREDENCIALES = "credenciales.json"
URL_BASE_DATOS = "https://TU-PROYECTO-default-rtdb.firebaseio.com/"

credencial = credentials.Certificate(RUTA_CREDENCIALES)
firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})

gestorPenalizaciones = GestorPenalizaciones()

fechasTarde = [
    date(2026, 10, 21),  # miércoles
    date(2026, 10, 23),  # viernes
    date(2026, 10, 27),  # martes
    date(2026, 10, 30),  # viernes
]

for fechaTarde in fechasTarde:
    gestorPenalizaciones.penalizacion.registrarLlegadaTarde(fechaTarde)

primeraPenalizacion = gestorPenalizaciones.listarPenalizaciones()[0]
gestorPenalizaciones.marcarComoCumplida(primeraPenalizacion["id"])

print("Base de datos poblada")