from django import forms
from .models import CustomUser, Collaborator, Record
from .scripts import getFirstWord
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(forms.ModelForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña", required=True)
    favoritePlaceIsOffice=forms.BooleanField(label="¿Suele trabajar en la oficina?", required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username','first_name', 'isAdmin','favoritePlaceIsOffice', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['isAdmin'].label = '¿Es administrador?:'
        self.fields['first_name'].label = 'Nombre del colaborador:'
        self.fields['favoritePlaceIsOffice'].required=False


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username
    
    def clean_first_name(self):
        name = self.cleaned_data.get('first_name')
        if Collaborator.objects.filter(user__first_name=name).exists():
            raise forms.ValidationError("Ya existe un colaborador con este nombre")
        return name

class CollaboratorCreationForm(forms.ModelForm):
    
    name = forms.CharField(label="Nombre")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Contraseña", required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña", required=True)
    

    class Meta:
        model = Collaborator
        fields = ['name','favoritePlaceIsOffice','password1','password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['favoritePlaceIsOffice'].label = '¿Suele trabajar en la oficina?'
        
   
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Collaborator.objects.filter(user__first_name=name).exists():
            raise forms.ValidationError("Ya existe un colaborador con este nombre")
        return name
    
class InputRecordForm(forms.ModelForm):
    
    isUnTimelyRecord = forms.BooleanField(
        label="¿Estás marcando fuera de tiempo?", 
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-custom'})
    )
    class Meta:
        model=Record
        fields=['collaborator','isUnTimelyRecord', 'unTimelyDateTime','placeIsOffice', 'placeDescription', 'photo']
        widgets = {
            'unTimelyDateTime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['collaborator'].label = 'Colaborador'
        self.fields['placeIsOffice'].label = '¿Estas en la oficina?'
        self.fields['unTimelyDateTime'].label = 'Fecha y Hora de Asistencia (SOLO SI MARCAS A DESTIEMPO)'
        self.fields['placeDescription'].label = 'Especificar lugar (SOLO EN CAMPO)'
        self.fields['photo'].label = 'Foto (CON FECHA Y HORA)'
        self.fields['unTimelyDateTime'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['isUnTimelyRecord'].initial=False
        self.fields['isUnTimelyRecord'].required=False
        self.fields['collaborator'].disabled = True
        
        if self.user.isAdmin or self.user.is_staff:
            self.fields['collaborator'].disabled = False
            
        try:
            self.fields['placeIsOffice'].initial = self.user.collaborator.favoritePlaceIsOffice
            self.fields['collaborator'].initial = self.user.collaborator
        except:
            print(f"Admin register: {self.user.username}")
            
            
    def clean_placeDescription(self):
        placeIsOffice=self.cleaned_data.get('placeIsOffice')
        placeDescription=self.cleaned_data.get('placeDescription')
        if (not placeDescription) and (not placeIsOffice):
            raise ValidationError(_("SI ESTAS EN CAMPO ES OBLIGATORIO ESPECIFICAR EL LUGAR"))
        return self.cleaned_data.get('placeDescription')
    
    def clean_unTimelyDateTime(self):
        isUnTimelyRecord=self.cleaned_data.get('isUnTimelyRecord')
        unTimelyDateTime=self.cleaned_data.get('unTimelyDateTime')
        if (not unTimelyDateTime) and (isUnTimelyRecord):
            raise ValidationError(_("SI ESTAS EN MARCANDO A DESTIEMPO ES OBLIGATORIO ESPECIFICAR LA FECHA Y HORA"))
        return self.cleaned_data.get('unTimelyDateTime')
    
class OutputRecordForm(forms.ModelForm):

    isUnTimelyRecord=forms.BooleanField(label="¿Estas marcando fuera de tiempo?")
    
    class Meta:
        model=Record
        fields=['collaborator', 'isUnTimelyRecord','unTimelyDateTime', 'photo']
        widgets = {
            'unTimelyDateTime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['collaborator'].label = 'Colaborador'
        self.fields['unTimelyDateTime'].label = 'Fecha y Hora de Asistencia (SOLO SI MARCAS A DESTIEMPO)'
        self.fields['photo'].label = 'Foto (CON FECHA Y HORA)'
        self.fields['unTimelyDateTime'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['isUnTimelyRecord'].required=False
        self.fields['collaborator'].disabled = True
        
        if self.user.isAdmin or self.user.is_staff:
            self.fields['collaborator'].disabled = False
        try:
            self.fields['collaborator'].initial = self.user.collaborator
        except:
            print(f"Admin register: {self.user.username}")

    def clean_unTimelyDateTime(self):
        isUnTimelyRecord=self.cleaned_data.get('isUnTimelyRecord')
        unTimelyDateTime=self.cleaned_data.get('unTimelyDateTime')
        if (not unTimelyDateTime) and (isUnTimelyRecord):
            raise ValidationError(_("SI ESTAS EN MARCANDO A DESTIEMPO ES OBLIGATORIO ESPECIFICAR LA FECHA Y HORA"))
        return self.cleaned_data.get('unTimelyDateTime')
        