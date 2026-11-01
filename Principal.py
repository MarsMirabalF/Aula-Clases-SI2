import tkinter as tk
from pathlib import Path
import firebase_admin
from firebase_admin import credentials
from estilos import COLOR_FONDO
from modelos.GestorPenalizaciones import GestorPenalizaciones
from modelos.GestorApuntes import GestorApuntes
from Vistas.PantallaInicio import PantallaInicio

RUTA_CREDENCIALES = Path(__file__).resolve().parent / "Credenciales.json"
URL_BASE_DATOS = "https://proyecto-aula-clases-default-rtdb.firebaseio.com/"

credencial = credentials.Certificate(str(RUTA_CREDENCIALES))
firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})

ventana = tk.Tk()
ventana.title("Sistemas de Información 2")
ventana.geometry("480x320")
ventana.configure(bg=COLOR_FONDO)

pantallaInicio = PantallaInicio(ventana, GestorPenalizaciones(), GestorApuntes())
pantallaInicio.pack(fill="both", expand=True)

ventana.mainloop()
