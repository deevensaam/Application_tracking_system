from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.conf.urls.static import static
from django.template import loader
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Recruiter, Job, Candidate, JobApplication, Notes, FeedbackNotes, CandidateApplicationForm
from .forms import JobForm
from django.db import transaction
import time
import json

# Create your views here.

def Signup(request):
    if request.method=='POST':
        uname= request.POST.get('username')
        email= request.POST.get('email')
        pass1= request.POST.get('password1')
        pass2= request.POST.get('password2')
        if pass1!=pass2:
             return HttpResponse("Your Password and conform password are not same")
        else:  
            my_user=Recruiter.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render(request, 'signup.html')


def Login(request):
    if request.method=='POST':
            username=request.POST.get('username')
            pass1=request.POST.get('pass')
            user=authenticate(request, username=username, password=pass1)
            print(user)
          #  return redirect('home')    
            print(username,pass1)  
            if user is not None:
                login(request,user)    
                return redirect('Dashboard')    
            else:
                return HttpResponse("User name or password is Incorrect")   
    return render(request, 'login.html')

@login_required
def Home(request):
    return render(request,'home.html')

@login_required
def Base(request):
     return render(request,'base.html')

@login_required
def Header(request):
    return render(request,'nav-bar.html')

@login_required
def Dashboard(request):

     if request.method == 'POST':
          id=request.POST.get('archived')
          job=Job.objects.get(pk=id)
          job.archived = True
          job.save()
     Count_jobs = Job.objects.filter(archived=False).count()
     Count_jobss = Job.objects.filter(archived=True).count()
     Count_cand = Candidate.objects.values_list('firstname').count()
     jobs= Job.objects.filter(archived=False) 
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 
     return render(request,'Dashboard.html', {'jobs':job_objects,'Count_jobs':Count_jobs,'Count_jobss':Count_jobss,'Count_cand':Count_cand})

     # Job_list = Job.objects.all()
     # Count_jobs = Job.objects.values_list('role').count()
     # Count_cand = Candidate.objects.values_list('firstname').count()
     # jobs= Job.objects.all()
     # job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 

     # return render(request, 'Dashboard.html',{'Job_list':Job_list,'Count_jobs':Count_jobs,'Count_cand':Count_cand,'jobs':job_objects})

@login_required
def LogoutPage(request):
     logout(request)
     return redirect('login')

@login_required
def JobDetails(request):
    return render(request,'job_details.html')

@login_required
def Jobs(request):
     if request.method == 'POST':
          id=request.POST.get('archived')
          job=Job.objects.get(pk=id)
          job.archived = True
          job.save()
     Count_jobs = Job.objects.filter(archived=False).count()
     Count_jobss = Job.objects.filter(archived=True).count()
     jobs= Job.objects.filter(archived=False) 
     
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 
     return render(request,'jobs.html', {'jobs':job_objects,'Count_jobs':Count_jobs,'Count_jobss':Count_jobss})

@login_required
def Jobs_List(request, id):
     job=Job.objects.get(pk=id)
     applications= JobApplication.objects.filter(jobId = job).prefetch_related('applied_by')
     return render(request,'jobs_list.html',{'applications':applications,'job':job})



@login_required
def Candidates_list(request):
     if request.method == 'POST':
          status = request.POST.get('status')
          application_id = request.POST.get('applicationId')
          application = JobApplication.objects.get(pk=application_id)
          application.status = status
          application.save()
          return JsonResponse({'application_id' : application.pk, 'status' : application.status })
     applications = JobApplication.objects.all().prefetch_related('jobId','applied_by')
     print(applications)
     Candidates_count = Candidate.objects.values_list('firstname').count()
     return render(request,'candidates_list.html', {'applications':applications,'Candidates_count':Candidates_count})

@login_required
def create_job_session_generataor(request):
     session_id = int(time.time())
     request.session[str(session_id) + 'job_form'] = json.dumps({'job' : "dev"})
     request.session[str(session_id) + 'check_list'] = json.dumps({'list' : True}) 
     return redirect('create_jobs', session_id)

# add a random session ID to url so that it's unique through out
@login_required
def Create_Jobs(request, sessionId):
     # job = request.session.get(str(sessionId))['job_form']
     # print(job)
     session_item = request.session.get(str(sessionId) + 'job_form') 
     job_item = session_item if session_item is not None else dict()
     if request.method == 'POST':
          # job creator 
          created_by = request.user
          # contents from form 
          job_item = dict()
          job_item['role'] = request.POST.get('role')
          job_item['jobtype']= request.POST.get('jobtype')
          job_item['salary'] = request.POST.get('salary')
          job_item['select_template'] = request.POST.get('select_template')
          job_item['experience_min'] = request.POST.get('experience_min')
          job_item['experience_max'] = request.POST.get('experience_max')
          job_item['description'] = request.POST.get('description')
          job_item['requirements'] = request.POST.get('requirements')
          job_item['about_company'] = request.POST.get('about_company')
          request.session[str(sessionId) + 'job_form'] = job_item
          # job= Job(role=role, jobtype=jobtype, salary=salary, select_template=select_template,experience_min=experience_min,experience_max=experience_max, 
          #             description=description, requirements=requirements, about_company=about_company,created_by=created_by)
          # job.save()
          return redirect('create_application_form', sessionId) 
     return render(request,'create_jobs.html', { 'session_id': sessionId, 'job' : job_item })

@login_required
def Create_Application_Form(request, sessionId):
     session_item = request.session.get(str(sessionId) + 'check_list') 
     check_list_item = session_item if session_item is not None else dict()
     # session_item = request.session.get(str(sessionId))
     if request.method == 'POST':
          # print(request.session.get(str(sessionId)))
          check_list_item = dict()
          # print(request.POST.get('phonenumber'))
          check_list_item['phonenumber'] = bool(request.POST.get('phonenumber'))
          check_list_item['designation'] = request.POST.get('designation')
          check_list_item['currentctc'] = request.POST.get('currentctc')
          check_list_item['expectedctc'] = request.POST.get('expectedctc')
          check_list_item['skypeid'] = request.POST.get('skypeid')
          check_list_item['Github_url'] = request.POST.get('Github_url')
          check_list_item['linkedin_url'] = request.POST.get('linkedin_url')
          check_list_item['portfolio_url'] = request.POST.get('portfolio_url')
          check_list_item['resume'] = request.POST.get('resume')
          check_list_item['experience'] = request.POST.get('experience')
          check_list_item['skills'] = request.POST.get('skills')
          check_list_item['email'] = request.POST.get('email')
          check_list_item['notice'] = request.POST.get('notice')
          check_list_item['source'] = request.POST.get('source')
          check_list_item['current_location'] = request.POST.get('current_location')
          check_list_item['full_name'] = request.POST.get('full_name')
          request.session[str(sessionId) + 'check_list' ] = check_list_item

          # candidate_application_form = CandidateApplicationForm(phonenumber=bool(phonenumber),
          #                                                            designation=bool(designation),
          #                                                            currentctc=bool(currentctc),
          #                                                            expectedctc=bool(expectedctc), 
          #                                                            skypeid=bool(skypeid),
          #                                                            Github_url=bool(Github_url),
          #                                                            linkedin_url=bool(linkedin_url), 
          #                                                            current_location=bool(current_location), 
          #                                                            firstname=full_name == 'True',
          #                                                            lastname=full_name == 'True', 
          #                                                            state=current_location == 'True', 
          #                                                            city=current_location == 'True',
          #                                                            pincode=current_location == 'True',
          #                                                            street=current_location == 'True', 
          #                                                            portfolio_url=bool(portfolio_url),
          #                                                            resume=bool(resume),
          #                                                            experience=bool(experience),
          #                                                            skills=bool(skills),
          #                                                            email=bool(email),
          #                                                            notice=bool(notice),
          #                                                            job_ref=job)
          # candidate_application_form.save()
          return redirect('create_publish', sessionId)
     return render(request,'create_application_form.html', {'session_id' : sessionId, 'check_list' : check_list_item})

@login_required
def Create_Publish(request, sessionId):
     job_form = request.session.get(str(sessionId) + "job_form")
     check_list = request.session.get(str(sessionId) + "check_list")
     # TODO: write transaction for creating job and checklist 
     if request.method == 'POST':
          with transaction.atomic():

               job = Job(role=job_form['role'],
                         created_by=request.user,
                         jobtype=job_form['jobtype'],
                         salary=job_form['salary'],
                         select_template=job_form['select_template'],
                         experience_min=job_form['experience_min'],
                         experience_max=job_form['experience_max'], 
                         description=job_form['description'], 
                         requirements=job_form['requirements'],
                         about_company=job_form['about_company'])
               job.save()
               

               candidate_check_list = CandidateApplicationForm(phonenumber=check_list['phonenumber'],
                                                            designation=check_list['designation'],
                                                            currentctc=check_list['currentctc'],
                                                            expectedctc=check_list['expectedctc'], 
                                                            skypeid=check_list['skypeid'],
                                                            Github_url=check_list['Github_url'],
                                                            linkedin_url=check_list['linkedin_url'], 
                                                            current_location=check_list['current_location'], 
                                                            portfolio_url=check_list['portfolio_url'],
                                                            resume=check_list['resume'],
                                                            experience=check_list['experience'],
                                                            skills=check_list['skills'],
                                                            email=check_list['email'],
                                                            notice=check_list['notice'],
                                                            source=check_list['source'],
                                                            firstname=check_list['full_name'] == 'True',
                                                            lastname=check_list['full_name'] == 'True', 
                                                            state=check_list['current_location'] == 'True', 
                                                            city=check_list['current_location'] == 'True',
                                                            pincode=check_list['current_location'] == 'True',
                                                            street=check_list['current_location'] == 'True', 
                                                                 job_ref=job)
               candidate_check_list.save()
               print(job, candidate_check_list)
          
          return redirect('jobs')
     return render(request,'create_publish.html', {'session_id' : sessionId})


def Job_Templete(request):
     return render(request, 'job_templete.html')


def Candidate_profile_Edit(request):
     return render(request,'candidate_profile_edit.html')


@login_required
def JobApplicationStatus(request, id):

     application = JobApplication.objects.filter(pk=id).prefetch_related('applied_by','jobId')
     notes = Notes.objects.filter(application_ref = application.first()).prefetch_related('added_by')
     feedbacks = FeedbackNotes.objects.filter(application_ref = application.first()).prefetch_related('given_by')


     if request.method == 'POST':
          if 'user_note' in request.POST:
               user_note = request.POST.get('user_note')
               note= Notes(user_note = user_note, added_by = request.user, application_ref = application.first())
               note.save()

          elif 'user_feedback' in request.POST:
               user_feedback = request.POST.get('user_feedback')
               communication_rating = request.POST.get('communication_rating')
               logicalskills_rating = request.POST.get('logicalskills_rating')
               techinicalskills_rating = request.POST.get('techinicalskills_rating')
               feedback= FeedbackNotes(user_feedback = user_feedback,communication_rating=communication_rating, logicalskills_rating=logicalskills_rating, techinicalskills_rating=techinicalskills_rating,  given_by = request.user, application_ref = application.first())
               feedback.save()
     return render(request,'candidate_profile.html',{'feedbacks':feedbacks, 'notes':notes,'application':application.first()})


@login_required
def Candidate_application(request, id):
     job = Job.objects.get(pk=id)
     check_list= CandidateApplicationForm.objects.get(job_ref = job)
     # candidate_application_form_map = CandidateApplicationForm.objects.get(job_ref=job)
     
     if request.method == 'POST':
          email = request.POST.get('email')
          candidate = Candidate.objects.filter(email=email).first()

          if candidate is None:
               firstname = request.POST.get('firstname')
               lastname= request.POST.get('lastname')
               phonenumber = request.POST.get('phonenumber')
               designation = request.POST.get('designation')
               currentctc = request.POST.get('currentctc')
               expectedctc = request.POST.get('expectedctc')
               skypeid = request.POST.get('skypeid')
               Github_url = request.POST.get('Github_url')
               linkedin_url = request.POST.get('linkedin_url')
               portfolio_url= request.POST.get('portfolio_url')
               resume = request.POST.get('resume')
               street = request.POST.get('street')
               pincode = request.POST.get('pincode')
               city = request.POST.get('city')
               state = request.POST.get('state')
               experience = request.POST.get('experience')
               skills = request.POST.get('skills')
               source= request.POST.get('source')
               landmark = request.POST.get('landmark')
               notice = request.POST.get('notice')

               candidate= Candidate(firstname=firstname,lastname=lastname, email=email, phonenumber=phonenumber,designation=designation,
                                   currentctc=currentctc, expectedctc=expectedctc, skypeid=skypeid, Github_url=Github_url,
                                   linkedin_url=linkedin_url,portfolio_url=portfolio_url, resume=resume, street=street,
                                   pincode=pincode,city=city, state=state, experience=experience, skills=skills,source=source,landmark=landmark, notice=notice )
               candidate.save()
               print(candidate)
          else:
               HttpResponse("You have already applied for this job")

          jobApplication = JobApplication(jobId = job, applied_by = candidate, status = 'accepted')
          jobApplication.save()
          print(jobApplication)
          return redirect('jobss') 
     return render(request, 'candidate_application.html',{'check_list':check_list})


def testing(request):
     submitted = False
     if request.method == "POST":
          form = JobForm(request.POST)
          if form.is_valid():
               form.save()
               return HttpResponseRedirect('/testing?submitted=True')
     else:
           form = JobForm
           if 'submitted' in request.GET:
                submitted = True
     return render(request, 'testing.html',{'form':form, 'submitted':submitted})


def Jobss(request):
     #jobs_lists = Job.objects.all()
     # candidate_candlist = JobApplication.objects.filter(jobId = cand_list).prefetch_related('candidate_set')
     # print(candidate_candlist)
     jobs= Job.objects.all()
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 
     return render(request, 'jobss.html',{'jobs':job_objects})

@login_required
def Jobs_Archive(request):
     if request.method == 'POST':
          id=request.POST.get('archived')
          job=Job.objects.get(pk=id)
          job.archived = True
          job.save()
     Count_jobs = Job.objects.filter(archived=False).count()
     Count_jobss = Job.objects.filter(archived=True).count()
     jobs= Job.objects.filter(archived=True) 
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 
     return render(request,'jobs_archive.html', {'jobs':job_objects,'Count_jobs':Count_jobs,'Count_jobss':Count_jobss})



