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
        diferencia = fecha_fin - fecha_inicio
        horas = diferencia.days * 24 + diferencia.seconds // 3600
        minutos = (diferencia.seconds % 3600) // 60
        segundos = diferencia.seconds % 60
        return f'{horas:02}:{minutos:02}:{segundos:02}'
    return None

def corregirFecha(registro):
    if registro.unTimelyDateTime:
        registro.dateTime = registro.unTimelyDateTime
        registro.unTimelyDateTime = None
        registro.save()
        return True
    return False
def eliminar(registro):
    if registro:
        registro.delete()
        registro.save()
        return True
    return False



    
    
