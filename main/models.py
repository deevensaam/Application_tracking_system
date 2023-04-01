from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
JOBTYPE_CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Remote', 'Remote'),
)

TEMPLATE_CHOICES=(
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
)

STAGE_CHOICE =(
    ('screening', 'screening'),
    ('telephone', 'telephone'),
    ('coding', 'coding'),
    ('F2F', 'F2F'),
    ('Make offer', 'Make offer'),
    ('selected', 'selected'),
)

MIN_CHOICE=(
    ('0','0'),
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
)

MAX_CHOICE=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
)

class Candidate(models.Model):
    firstname=models.CharField('First name', max_length=50)
    lastname=models.CharField('Last name', max_length=50, blank=True)
    email=models.EmailField('Email id')
    phonenumber=models.IntegerField('Phone number', null=True)
    designation=models.CharField('Designation', max_length=15, null=True)
    currentctc=models.IntegerField('Current ctc', null=True)
    expectedctc=models.IntegerField('Expected ctc', null=True)
    skypeid=models.URLField('Skype id', null=True)
    linkedin_url=models.URLField('Linkedin_url', null=True)
    Github_url=models.URLField('Github_url', null=True)
    portfolio_url=models.URLField('Portfolio_url', null=True)
    resume=models.FileField('Resume/CV', upload_to='uploads/')
    street=models.CharField('Street', max_length=15, null=True)
    landmark=models.CharField('Landmark', max_length=50, null=True)
    pincode=models.IntegerField('Pincode', null=True)
    city=models.CharField('City', max_length=20, null=True)
    state=models.CharField('State', max_length=20, null=True)
    exp=models.IntegerField('Years Exp', null=True)
    event_time=models.DateTimeField(default=timezone.now)
    stage= models.CharField('Stage', max_length=25,choices=STAGE_CHOICE,default='screening', null=True)

    def __str__(self) -> str:
        return f"Candidate - id : {self.pk} email : {self.email}"

class Recruiter(AbstractUser):
    def __str__(self) -> str:
        return f"Recruiter - id : {self.pk} email : {self.email}" 
    
class Job(models.Model):
    role = models.CharField(max_length=25)
    jobtype = models.CharField(max_length=15, choices=JOBTYPE_CHOICES,default='Full time',blank=True)
    salary = models.IntegerField(default=0)
    select_template= models.CharField(max_length=20, choices=TEMPLATE_CHOICES, default='01')
    experience_min = models.CharField(choices=MIN_CHOICE,max_length=2,default='1')
    experience_max = models.CharField(choices=MAX_CHOICE,max_length=2, default='1')
    description = models.TextField(max_length=300)
    requirements= models.TextField(max_length=300)
    about_company= models.TextField(max_length=300)
    event_time = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(on_delete=models.CASCADE, to=Recruiter)

    def __str__(self) -> str:
        return f"id : {self.pk} role : {self.role} salary : {self.salary}"

class JobApplication(models.Model):

    class ApplicationStatus(models.TextChoices):
        ACCEPTED = ('ACCEPTED', 'accepted')
        REJECTED = ('REJECTED', 'rejected')
    jobId = models.ForeignKey(on_delete=models.CASCADE, to=Job)
    applied_by = models.ForeignKey(on_delete=models.CASCADE, to=Candidate)
    feedback_note = models.CharField(max_length=200)
    user_note = models.CharField(max_length=200)
    status = models.CharField(max_length=20,choices=ApplicationStatus.choices)