from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CollaboratorCreationForm, InputRecordForm, OutputRecordForm
from .models import CustomUser, Collaborator, Record, AttendanceRecord
from .scripts import generateUniqueUsername
from openpyxl import Workbook
from openpyxl.styles import Alignment,Font
from django.http import HttpResponse
from openpyxl.utils import get_column_letter
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.utils.timezone import now

## VIEWS
### LOGIN
def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

### LOGOUT
def logoutView(request):
    logout(request)
    return redirect('login')

### HOME
def homeView(request):
    if request.user.is_authenticated:
        collaborators=Collaborator.objects.all()
        return render(request, 'home.html',{"collaborators":collaborators})
    return render(request, 'home.html')

###ADMIN

@user_passes_test(lambda u: u.is_superuser or (u.isAdmin))
def dashboard_view(request):
    return render(request, 'admin_dashboard.html')


### CREAR USUARIOS Y COLABORADORES
@user_passes_test(lambda u: u.is_superuser)
def createUserView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            collaborator=Collaborator.objects.create(
                user=user,
                favoritePlaceIsOffice=form.cleaned_data['favoritePlaceIsOffice']
            )
            collaborator.save()
            return redirect('user', user_id=user.id)
    else:
        form = CustomUserCreationForm()

    return render(request, 'createUser.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def userDetailView(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, 'user.html', {'user': user})

@user_passes_test(lambda u: u.is_superuser or (u.isAdmin))
def createCollaboratorview(request):
    if request.method == 'POST':
        form = CollaboratorCreationForm(request.POST)
        if form.is_valid():
            collaborator = form.save(commit=False)
            password = form.cleaned_data['password1']
            name=form.cleaned_data['name']
            username=generateUniqueUsername(name)
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                first_name=name
            )
            user.username=username+str(user.id)+str(int(user.is_staff))
            user.save()
            collaborator.user = user
            collaborator.save()
            messages.success(request, "Colaborador inscrito exitosamente.")
            return redirect('collaborator', collaborator_id=collaborator.id)
    else:
        form = CollaboratorCreationForm()

    return render(request, 'createCollaborator.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser or (u.isAdmin))
def collaboratorDetailView(request, collaborator_id):
    collaborator = Collaborator.objects.get(id=collaborator_id)
    return render(request, 'collaborator.html', {'collaborator': collaborator})

@login_required
def registerInputView(request):
    if request.method == 'POST':
        form = InputRecordForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            input = form.save(commit=False)
            collaborator = form.cleaned_data.get('collaborator')
            input.unTimelyDateTime=form.cleaned_data.get('unTimelyDateTime')
            input.collaborator = collaborator
            if collaborator.isWorking==-1:
                input.save()
                completeRecord=AttendanceRecord.objects.create(
                    inRecord=input,
                    collaborator=collaborator,
                )
                completeRecord.save()
                idCompleteRecord=completeRecord.id
                collaborator.isWorking=int(idCompleteRecord)
                collaborator.save()
                return redirect('record',record_id=input.id)
            else:
                messages.error(request, "Usted ya se encuentra trabajando, para ingresar de nuevo primero debe marcar su salida.")
                return render(request, 'registerInput.html', {'form': form})
    else:
        form = InputRecordForm(user=request.user)
    
    return render(request, 'registerInput.html', {'form': form})

@login_required
def registerOutputView(request):
    if request.method == 'POST':
        form = OutputRecordForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            output = form.save(commit=False)
            collaborator = form.cleaned_data.get('collaborator')
            output.collaborator = collaborator
            if collaborator.isWorking!=-1:
                output.typeIsInput=False
                completeAttendancePartial=AttendanceRecord.objects.get(id=collaborator.isWorking)
                output.placeIsOffice=completeAttendancePartial.inRecord.placeIsOffice
                output.save()
                completeAttendancePartial.outRecord=output
                completeAttendancePartial.save()
                collaborator.isWorking=-1
                collaborator.save()
                return redirect('attendanceRecord',attendanceRecord_id=completeAttendancePartial.id)
            else:
                messages.error(request, "Usted no esta trabajado, no puede marcar salida.")
                return render(request, 'registerOutput.html', {'form': form})
    else:
        form = OutputRecordForm(user=request.user)
    
    return render(request, 'registerOutput.html', {'form': form})

@login_required
def recordDetailView(request, record_id):
    record = Record.objects.get(id=record_id)
    return render(request, 'record.html', {'record': record})

@login_required
def attendanceRecordDetailView(request, attendanceRecord_id):
    attendanceRecord = AttendanceRecord.objects.get(id=attendanceRecord_id)
    if attendanceRecord.outRecord:
        time_diff = attendanceRecord.outRecord.dateTime - attendanceRecord.inRecord.dateTime
        worked_hours = time_diff.total_seconds() / 3600 
    else:
        worked_hours = None
    context = {
        'attendanceRecord': attendanceRecord,
        'worked_hours': worked_hours
    }
    return render(request, 'attendanceRecord.html', context)

@login_required
def myRecords(request):
    if request.user.is_staff or hasattr(request.user, 'isAdmin') and request.user.isAdmin:
        collaborators = Collaborator.objects.all()
        selected_collaborator_id = request.GET.get('collaborator', None)

        if selected_collaborator_id:
            records = AttendanceRecord.objects.filter(collaborator_id=selected_collaborator_id).order_by('-inRecord__dateTime')
        else:
            records = AttendanceRecord.objects.none()
    else:
        collaborators = None
        records = AttendanceRecord.objects.filter(collaborator=request.user.collaborator).order_by('-inRecord__dateTime')
        selected_collaborator_id=None

    return render(request, 'myRecords.html', {
        'records': records,
        'collaborators': collaborators,
        'selected_collaborator_id': selected_collaborator_id
    })
@login_required
def hoursWorked(request):
    user = request.user
    today = now().date()

    period = request.GET.get('period', 'week')
    start_date = today - timedelta(days=today.weekday()) if period == 'week' else today.replace(day=1)
    
    if user.is_staff or user.isAdmin:
        collaborators = Collaborator.objects.all()
        selected_collaborator_id = request.GET.get('collaborator', None)

        if selected_collaborator_id:
            records = AttendanceRecord.objects.filter(
                collaborator_id=selected_collaborator_id,
                inRecord__dateTime__date__gte=start_date
            )
        else:
            records = AttendanceRecord.objects.none()
    else:
        collaborators = None
        selected_collaborator_id=None
        records = AttendanceRecord.objects.filter(
            collaborator=user.collaborator,
            inRecord__dateTime__date__gte=start_date
        )

    records = records.annotate(
        hours_worked=ExpressionWrapper(
            F('outRecord__dateTime') - F('inRecord__dateTime'),
            output_field=fields.DurationField()
        )
    )
    total_hours = records.aggregate(Sum('hours_worked'))['hours_worked__sum']
    if total_hours:
        total_hours = str(total_hours).split(".")[0]

    return render(request, 'hoursWorked.html', {
        'records': records,
        'collaborators': collaborators,
        'selected_collaborator_id': selected_collaborator_id,
        'total_hours': total_hours,
        'period': period
    })
    
@login_required
def dashboard_view(request):
    if not request.user.is_staff and not request.user.isAdmin:
        return redirect('home')

    total_users = CustomUser.objects.filter(isDelete=False).count()
    total_collaborators = Collaborator.objects.filter(isDelete=False).count()
    total_attendance = AttendanceRecord.objects.count()

    context = {
        "total_users": total_users,
        "total_collaborators": total_collaborators,
        "total_attendance": total_attendance,
    }
    return render(request, "adminDashboard.html", context)
