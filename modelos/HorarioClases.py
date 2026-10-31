from datetime import timedelta

NOMBRES_DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
DIAS_CLASE = [1, 2, 4]  # martes, miércoles, viernes
HORA_INICIO = "19:00"
HORA_FIN = "20:30"


class HorarioClases:
    def obtenerDiasClase(self):
        return [NOMBRES_DIAS[dia] for dia in DIAS_CLASE]

    def calcularProximaClase(self, fecha):
        proximaFecha = fecha + timedelta(days=1)
        while proximaFecha.weekday() not in DIAS_CLASE:
            proximaFecha += timedelta(days=1)
        return proximaFecha

    def obtenerNombreDia(self, fecha):
        return NOMBRES_DIAS[fecha.weekday()]

    def obtenerHorario(self):
        return HORA_INICIO, HORA_FIN