from django.urls import path
from . import views

urlpatterns = [
    ## User URLS
    path('login/', views.loginView, name='login'), #user
    path('logout/', views.logoutView, name='logout'), #user
    ## Templates home
    path('', views.homeView, name='home'), #user
    ## APPLICATION ASISTENCIA
    path('registerInput/', views.registerInputView, name='registerInput'), #user
    path('record/<int:record_id>/', views.recordDetailView, name='record'), #user
    path('registerOutput/', views.registerOutputView, name='registerOutput'), #user
    path('attendanceRecord/<int:attendanceRecord_id>/', views.attendanceRecordDetailView, name='attendanceRecord'), #user
    path('myRecords/', views.myRecords, name='myRecords'), #user
    path('hoursWorked/', views.hoursWorked, name='hoursWorked'), #user
    path('attendanceChat/', views.attendanceChatView, name='attendanceChat'), #user
    
    ### ADMIN DASHBOARD
    path('adminDashboard/', views.dashboard_view, name='adminDashboard'), #admin
    path('createUser/', views.createUserView, name='createUser'), #admin
    path('user/<int:user_id>/', views.userDetailView, name='user'), #admin
    path('createCollaborator/', views.createCollaboratorview, name='createCollaborator'), #admin
    path('collaborator/<int:collaborator_id>/', views.collaboratorDetailView, name='collaborator'), #

]
