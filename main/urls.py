from django.urls import path
from . import views

urlpatterns = [
    path('',views.Signup, name='signup'),
    path('login',views.Login, name='login'),
    path('Dashboard',views.Dashboard, name='Dashboard'),
    path('nav-bar/',views.Header, name='nav-bar'),
    path('logout/', views.LogoutPage, name='logout'),
    path('job_details/',views.JobDetails, name='job_details'),
    path('jobs/',views.Jobs,name='jobs'),
    path('jobs/apply/',views.Jobss,name='jobss'),
    path('jobs_list/<id>/', views.Jobs_List,name='jobs_list'),
    path('create_jobs/', views.Create_Jobs, name='create_jobs'),
    path('create_application_form/', views.Create_Application_Form, name='create_application_form'),
    path('create_publish/', views.Create_Publish, name='create_publish'),
    path('candidates_list/', views.Candidates_list, name='candidates_list'),
    path('job_templete/', views.Job_Templete, name='job_templete'),
    path('candidate_profile/<id>/', views.Candidate_profile, name='candidate_profile'),
    path('candidate_profile_edit/', views.Candidate_profile_Edit, name='candidate_profile_edit'),
    # path('candidate_application/',views.Candidate_application, name='candidate_application'),
    path('candidate_application/<id>/',views.Candidate_application, name='candidate_application'),
    path('testing/',views.testing, name='testing'),
    
]