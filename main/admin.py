from django.contrib import admin
from .models import Recruiter
from .models import Job, Candidate, JobApplication

# Register your models here.
admin.site.register(Recruiter)

@admin.register(Job)
class JobsAdmin(admin.ModelAdmin):
    list_display = ('role','salary') #To display jobname and exp years
    ordering = ('role','salary') #Alphabetical order 
    search_fields = ('role','salary') #To search by name and years

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('firstname','email') #To display jobname and exp years
    ordering = ('firstname','email') #Alphabetical order 
    search_fields = ('firstname','email') #To search by name and years

admin.site.register(JobApplication)
