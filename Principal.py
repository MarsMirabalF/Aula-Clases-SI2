import tkinter as tk
import firebase_admin
from firebase_admin import credentials
from Estilos import COLOR_FONDO
from Modelos.GestorPenalizaciones import GestorPenalizaciones
from Vistas.PantallaInicio import PantallaInicio

RUTA_CREDENCIALES = "Credenciales.json"
URL_BASE_DATOS = "https://proyecto-aula-clases-default-rtdb.firebaseio.com/"

credencial = credentials.Certificate(RUTA_CREDENCIALES)
firebase_admin.initialize_app(credencial, {"databaseURL": URL_BASE_DATOS})

ventana = tk.Tk()
ventana.title("Sistemas de Información 2")
ventana.geometry("480x240")
ventana.configure(bg=COLOR_FONDO)

pantallaInicio = PantallaInicio(ventana, GestorPenalizaciones())
pantallaInicio.pack(fill="both", expand=True)

ventana.mainloop()