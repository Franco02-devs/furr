from django.urls import path
from . import views

urlpatterns = [
    ## User URLS
    path('login/', views.loginView, name='login'), #user OK
    path('logout/', views.logoutView, name='logout'), #user OK
    ## Templates home
    path('', views.homeView, name='home'), #user OK
    ### ADMIN DASHBOARD
    path('adminDashboard/', views.dashboardView, name='adminDashboard'), #admin OK
    path('createUser/', views.createUserView, name='createUser'), #admin OK
    path('user/<int:user_id>/', views.userDetailView, name='user'), #admin OK
    path('createCollaborator/', views.createCollaboratorview, name='createCollaborator'), #admin OK
    path('collaborator/<int:collaborator_id>/', views.collaboratorDetailView, name='collaborator'), # OK
    path('adminDashboard/observedList/', views.attendanceObservationsView, name='observedList'), #
    path('reporteAsistencia/', views.reporte_asistencia_template, name='reporte'),
    path('excel/',views.generar_reporte_asistencia,name="excel"),
    ## APPLICATION ASISTENCIA
    path('registerInput/', views.registerInputView, name='registerInput'), #user OK
    path('record/<int:record_id>/', views.recordDetailView, name='record'), #user OK
    path('registerOutput/', views.registerOutputView, name='registerOutput'), #user OK
    path('attendanceRecord/<int:attendanceRecord_id>/', views.attendanceRecordDetailView, name='attendanceRecord'), #user OK
    path('myRecords/', views.myRecords, name='myRecords'), #user
    path('hoursWorked/', views.hoursWorked, name='hoursWorked'), #user
    path('attendanceChat/', views.attendanceChatView, name='attendanceChat'), #user
]
