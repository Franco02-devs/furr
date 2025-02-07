# personal/scripts.py
from .models import CustomUser, Record, Collaborator, AttendanceRecord
import pytz

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
        registro.isDelete=True
        registro.save()
        return True
    return False

############################################################################################
############################################################################################
## GETTERS ##
def getCollaboratorsActive():
    collaboratorsActive = Collaborator.objects.enables().exclude(isWorking=-1)
    return collaboratorsActive

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
        launch=isLaunch(inRecordDT,diffHours)
        if launch:
            diffHours -= 1
    except:
        diffHours=0
        launch=False
    return diffHours,launch

def isLaunch(inRecordDT, diffHours):
    peru_tz = pytz.timezone("America/Lima")
    inRecordDT = inRecordDT.astimezone(peru_tz)

    return inRecordDT.hour < 12 and diffHours > 5


def getAllAttendanceRecordsT(collaborator, limit=None):
    records = AttendanceRecord.objects.filter(
        isDelete=False,
        collaborator=collaborator,
        collaborator__isDelete=False
    ).order_by('-inRecord__dateTime')
    
    if limit is not None:
        records = records[:limit]
    return records

def getAllAttendanceRecordsTRange(collaborator,start,end):
    records = AttendanceRecord.objects.filter(
        isDelete=False,
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
        hoursWorked, _ =calculateHoursWorked(attendanceRecord)
        allHours.append(hoursWorked)
        totalHours=totalHours+hoursWorked
    finalRecords=zip(attendanceRecords,allHours)
    return totalHours,finalRecords

def isObserved(attendance_record):
    if attendance_record.inRecord.unTimelyDateTime or (attendance_record.outRecord and attendance_record.outRecord.unTimelyDateTime):
        return 0
    if attendance_record.outRecord:
        time_diff, _ = calculateHoursWorked(attendance_record)
        if time_diff < 1:
            return 1
        elif time_diff>10:
            return 2
    return -1


def float_to_hms(hours_float):
    hours = int(hours_float)
    minutes = int((hours_float - hours) * 60)
    seconds = int((((hours_float - hours) * 60) - minutes) * 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}"


    
    


    
    
