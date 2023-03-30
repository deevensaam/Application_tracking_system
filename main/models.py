from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Job(models.Model):
    role = models.CharField(max_length=25)
    description = models.CharField(max_length=300)
    salary = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"id : {self.pk} role : {self.role} salary : {self.salary}"


class Candidate(AbstractUser):
    def __str__(self) -> str:
        return f"Candidate - id : {self.pk} email : {self.email}"


class Recruiter(AbstractUser):
    def __str__(self) -> str:
        return f"Recruiter - id : {self.pk} email : {self.email}" 


class JobApplication(models.Model):

    class ApplicationStatus(models.TextChoices):
        ACCEPTED = 'ACCEPTED', _('accepted')
        REJECTED = 'REJECTED', _('rejected')
 
    jobId = models.ForeignKey(to=Job.pk)
    created_by = models.ForeignKey(to=Recruiter.pk)
    applied_by = models.ForeignKey(to=Candidate.pk)
    feedback_note = models.CharField(max_length=200)
    user_note = models.CharField(max_length=200)
    status = models.CharField(choices=ApplicationStatus.choices)
