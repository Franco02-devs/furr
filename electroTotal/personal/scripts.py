# personal/scripts.py
from .models import CustomUser, Record, Collaborator, AttendanceRecord
from datetime import timedelta


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
############################################################################################

def getAllCollaborators():
    collaborators=Collaborator.objects.enables()
    return collaborators
def getAllUsers():
    users=CustomUser.objects.enables()
    return users
def getAllAttendanceRecords():
    records=AttendanceRecord.objects.enables()
    return records
def calculateHoursWorked(attendanceRecord):
    try:
        inRecordDT=attendanceRecord.inRecord.dateTime
        outRecordDT=attendanceRecord.outRecord.dateTime
        diff=outRecordDT-inRecordDT
        diffHours=diff.total_seconds() / 3600
        if inRecordDT.hour < 12 and diffHours > 5:
            attendanceRecord.isLunch=True
            attendanceRecord.save()
            diffHours -= 1
        else:
            attendanceRecord.isLunch=False
            attendanceRecord.save()           
    except:
        diffHours=0
    return diffHours
def getAllAttendanceRecordsT(collaborator):
    records = AttendanceRecord.objects.filter(
        collaborator=collaborator,
        collaborator__isDelete=False
    ).order_by('-inRecord__dateTime')
    return records
def getAllAttendanceRecordsTRange(collaborator,start,end):
    records = AttendanceRecord.objects.filter(
        collaborator=collaborator,
        collaborator__isDelete=False,
        inRecord__dateTime__date__gte=start,
        inRecord__dateTime__date__lte=end,
    ).order_by('-inRecord__dateTime')
    return records
def getAllHoursWorked(attendanceRecords):
    allHours=[]
    totalHours=0
    for attendanceRecord in attendanceRecords:
        hoursWorked=calculateHoursWorked(attendanceRecord)
        allHours.append(hoursWorked)
        totalHours=totalHours+hoursWorked
    finalRecords=zip(attendanceRecords,allHours)
    return totalHours,finalRecords

def isObserved(attendance_record):
    if attendance_record.inRecord.unTimelyDateTime or (attendance_record.outRecord and attendance_record.outRecord.unTimelyDateTime):
        return True
    
    if attendance_record.outRecord:
        time_diff = attendance_record.outRecord.dateTime - attendance_record.inRecord.dateTime
        if time_diff < timedelta(hours=1) or time_diff > timedelta(hours=10):
            return True
    return False

def float_to_hms(hours_float):
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    seconds = int((((hours_float - hours) * 60) - minutes) * 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


    
    


    
    
