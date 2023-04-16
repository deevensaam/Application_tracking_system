from django.urls import path
from . import views

urlpatterns = [
    path('login',views.Signup, name='signup'),
    path('',views.Login, name='login'),
    path('Dashboard',views.Dashboard, name='Dashboard'),
    path('nav-bar/',views.Header, name='nav-bar'),
    path('logout/', views.LogoutPage, name='logout'),
    path('job_details/',views.JobDetails, name='job_details'),
    path('jobs/',views.Jobs,name='jobs'),
    path('jobs/archive',views.Jobs_Archive,name='jobs_archive'),
    path('jobs/apply/',views.Jobss,name='jobss'),
    path('jobs_list/<id>/', views.Jobs_List,name='jobs_list'),
    path('create_jobs_redirect', views.create_job_session_generataor, name='create_jobs_redirect'),
    path('create_jobs/<int:sessionId>', views.Create_Jobs, name='create_jobs'),
    path('create_application_form/<int:sessionId>', views.Create_Application_Form, name='create_application_form'),
    path('create_publish/<int:sessionId>', views.Create_Publish, name='create_publish'),
    path('candidates_list/', views.Candidates_list, name='candidates_list'),
    path('job_templete/', views.Job_Templete, name='job_templete'),
    path('application/<id>/', views.JobApplicationStatus, name='application'),
    path('candidate_profile_edit/', views.Candidate_profile_Edit, name='candidate_profile_edit'),
    # path('candidate_application/',views.Candidate_application, name='candidate_application'),
    path('candidate_application/<id>/',views.Candidate_application, name='candidate_application'),
    path('create_jobs/<int:sessionId>/edit/', views.Job_edit, name='job_edit'),
    path('testing/',views.testing, name='testing'),
    
]