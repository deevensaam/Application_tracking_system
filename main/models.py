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

NOTICE_CHOICES=(
    ('Immediately', 'Immediately'),
    ('15 days', '15 days'),
    ('30 days', '30 days'),
    ('45 days', '45 days'),
    ('60 days', '60 days'),
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

SOURCE_CHOICES=(
    ('Linkedin','Linkedin'),
    ('Dribble','Dribble'),
    ('Self','Self'),
    ('Angellist','Angellist'),
    ('Career Page','Career Page'),
)


class Candidate(models.Model):
    firstname=models.CharField('First name', max_length=50)
    lastname=models.CharField('Last name', max_length=50, blank=True)
    email=models.EmailField('Email id')
    phonenumber=models.IntegerField('Phone number', null=True)
    designation=models.CharField('Designation', max_length=50, null=True)
    currentctc=models.IntegerField('Current ctc', null=True)
    expectedctc=models.IntegerField('Expected ctc', null=True)
    skypeid=models.CharField('Skype id',max_length=50, null=True)
    linkedin_url=models.URLField('Linkedin_url', null=True)
    Github_url=models.URLField('Github_url', null=True)
    portfolio_url=models.URLField('Portfolio_url', null=True)
    resume=models.FileField('Resume/CV ', upload_to='uploads/')
    street=models.CharField('Street', max_length=15, null=True)
    landmark=models.CharField('Landmark', max_length=50, null=True)
    pincode=models.IntegerField('Pincode', null=True)
    city=models.CharField('City', max_length=20, null=True)
    state=models.CharField('State', max_length=20, null=True)
    experience=models.IntegerField('Years Exp', null=True)
    event_time=models.DateTimeField(default=timezone.now)
    skills=models.CharField('Skills', max_length=225, null=True)
    notice = models.CharField(max_length=15, choices=NOTICE_CHOICES, default='15 days', blank=True)
    source = models.CharField(max_length=15, choices=SOURCE_CHOICES, default='Linkedin', blank=True)

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
    archived = models.BooleanField(default=False, null=True)

    def __str__(self) -> str:
        return f"id : {self.pk} role : {self.role} salary : {self.salary}"
    
class CandidateApplicationForm(models.Model):
    firstname=models.BooleanField(default=False, null=True)
    lastname=models.BooleanField(default=False, null=True)
    email=models.BooleanField(default=False, null=True)
    phonenumber=models.BooleanField(default=False, null=True)
    designation=models.BooleanField(default=False, null=True)
    currentctc=models.BooleanField(default=False, null=True)
    expectedctc=models.BooleanField(default=False, null=True)
    skypeid=models.BooleanField(default=False, null=True)
    linkedin_url=models.BooleanField(default=False, null=True)
    Github_url=models.BooleanField(default=False, null=True)
    portfolio_url=models.BooleanField(default=False, null=True)
    resume=models.BooleanField(default=False, null=True)
    street=models.BooleanField(default=False, null=True)
    landmark=models.BooleanField(default=False, null=True)
    pincode=models.BooleanField(default=False, null=True)
    city=models.BooleanField(default=False, null=True)
    state=models.BooleanField(default=False, null=True)
    experience=models.BooleanField(default=False, null=True)
    skills=models.BooleanField(default=False, null=True)
    notice=models.BooleanField(default=False, null=True)
    source = models.BooleanField(default=False, null=True)
    current_location = models.BooleanField(default=False, null=True)
    job_ref = models.OneToOneField(to= Job, on_delete=models.CASCADE,default= None, null=True)

class JobApplication(models.Model):

    class ApplicationStatus(models.TextChoices):
        ACCEPTED = ('SELECTED', 'selected')
        REJECTED = ('REJECTED', 'rejected')
        SCREENING = ('SCREENING', 'screening')
        TELEPHONE =('TELEPHONE', 'telephone') 
        CODING = ('CODING', 'coding')
        F2F = ('F2F', 'f2f')
        MAKEOFFER = ('MAKEOFFER', 'makeoffer')

    jobId = models.ForeignKey(on_delete=models.CASCADE, to=Job)
    applied_by = models.ForeignKey(on_delete=models.CASCADE, to=Candidate)
    # candidate = models.OneToOneField(on_delete=models.CASCADE, to=Candidate, default=None)
    # feedback_note = models.CharField(max_length=200)
    # user_note = models.CharField(max_length=200)
    status = models.CharField(max_length=20,choices=ApplicationStatus.choices,default='SELECTED')

class Notes(models.Model):
    user_note = models.CharField(max_length = 250)
    application_ref = models.ForeignKey(on_delete=models.CASCADE, to=JobApplication)
    added_by = models.ForeignKey(on_delete=models.CASCADE, to=Recruiter)
    event_time_notes = models.DateTimeField(default=timezone.now)

class FeedbackNotes(models.Model):
    user_feedback = models.CharField(max_length = 250)
    communication_rating = models.CharField(max_length = 10)
    logicalskills_rating = models.CharField(max_length = 10)
    techinicalskills_rating = models.CharField(max_length = 10)
    application_ref = models.ForeignKey(on_delete=models.CASCADE, to=JobApplication)
    given_by = models.ForeignKey(on_delete=models.CASCADE, to=Recruiter)
    event_time_feedback = models.DateTimeField(auto_now= True)