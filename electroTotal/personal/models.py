from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class ModelManager(models.Manager):
   
    def enables(self):
        return self.filter(isDelete=False)

class CustomUser(AbstractUser):
    isDelete= models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    
class Collaborator(models.Model):
    isDelete= models.BooleanField(default=False)    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    favoritePlaceIsOffice=models.BooleanField(default=False)
    isWorking=models.IntegerField(default=-1)
    objects=ModelManager()
    
    def __str__(self):
        return f"{self.user.username} - {self.user.first_name}"
    
class Record(models.Model):
    isDelete= models.BooleanField(default=False)
    typeIsInput= models.BooleanField(default=True)
    placeIsOffice=models.BooleanField(default=False)
    collaborator=models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    placeDescription=models.CharField(max_length=30,blank=True,null=True)
    partialDateTime = models.DateTimeField(default=timezone.now )
    dateTime=models.DateTimeField(default=timezone.now)
    unTimelyDateTime = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='fotos_asistencia/')
    objects=ModelManager()
    
    def __str__(self):
        warn=""
        if self.unTimelyDateTime:
            warn="DIFF! "
        return f"{warn}{self.collaborator.user.first_name} - {int(self.typeIsInput)} - {str(self.dateTime.strftime('%H:%M:%S'))}"
    
class AttendanceRecord(models.Model):
    isDelete=models.BooleanField(default=False)
    collaborator=models.ForeignKey(Collaborator, on_delete=models.CASCADE)
    inRecord=models.ForeignKey(Record, on_delete=models.CASCADE, related_name='input')
    outRecord=models.ForeignKey(Record, on_delete=models.CASCADE,blank=True,null=True, related_name='output')
    isLunch=models.BooleanField(default=False)
    objects=ModelManager()
    
    def __str__(self):
        final=""
        if self.outRecord:
            final=str(self.outRecord.dateTime.strftime("%H:%M:%S"))
        return f"{str(self.inRecord.dateTime.strftime('%H:%M:%S'))} - {final}"
