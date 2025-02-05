# personal/scripts.py
from .models import CustomUser, Record, Collaborator, AttendanceRecord


def getFirstWord(string):
    space=string.find(" ")
    if space!=-1:
        return (string[0:space])
    return string.lower()

def generateUniqueUsername(base_username):
    counter = 1
    username=getFirstWord(base_username)
    while CustomUser.objects.filter(username=username).exists():
        username=f"{username}{counter}"
        counter += 1
    return username.lower()
            
def diferenciaFecha(fecha_inicio, fecha_fin):
    if fecha_inicio and fecha_fin:
        # Calculamos la diferencia entre las fechas
        diferencia = fecha_fin - fecha_inicio
        
        # Extraemos las horas, minutos y segundos
        horas = diferencia.days * 24 + diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        segundos = diferencia.seconds % 60
        
        # Devuelves la diferencia en formato horas:minutos:segundos
        return f'{horas:02}:{minutos:02}:{segundos:02}'
    return None


    
    
