from django.contrib import admin
from .models import Collaborator, CustomUser

# Registra el modelo CustomUser en el admin
admin.site.register(CustomUser)

# Registra el modelo Trabajador en el admin
admin.site.register(Collaborator)
