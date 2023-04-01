from django import forms
from django .forms import ModelForm
from .models import Job

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ('role','jobtype','salary','select_template','experience_min','experience_max','description', 'requirements','about_company','event_time')