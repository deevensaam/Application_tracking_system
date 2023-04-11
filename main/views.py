from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.conf.urls.static import static
from django.template import loader
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Recruiter, Job, Candidate, JobApplication, Notes, FeedbackNotes, CandidateApplicationForm
from .forms import JobForm

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

def Home(request):
    return render(request,'home.html')

def Base(request):
     return render(request,'base.html')

def Header(request):
    return render(request,'nav-bar.html')

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

def LogoutPage(request):
     logout(request)
     return redirect('login')

def JobDetails(request):
    return render(request,'job_details.html')

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

def Jobs_List(request, id):
     job=Job.objects.get(pk=id)
     applications= JobApplication.objects.filter(jobId = job).prefetch_related('applied_by')
     return render(request,'jobs_list.html',{'applications':applications,'job':job})

def Candidates_list(request):
     # Candidate_list = Candidate.objects.all()
     # # applications = JobApplication.objects.filter(jobId=Candidate_list)
     # # print(applications)
     # # job=Candidate.objects.all()
     # # applications= JobApplication.objects.prefetch_related('applied_by')
     # Candidates_count = Candidate.objects.values_list('firstname').count()

     # jobs= Candidate.objects.all()
     # job_objects = [{JobApplication.objects.filter(applied_by=job)} for job in jobs] 
     applications = JobApplication.objects.all().prefetch_related('jobId','applied_by')
     Candidates_count = Candidate.objects.values_list('firstname').count()
     return render(request,'candidates_list.html', {'applications':applications,'Candidates_count':Candidates_count})

def Create_Jobs(request):
     if request.method == 'POST':
          role = request.POST.get('role')
          jobtype= request.POST.get('jobtype')
          salary = request.POST.get('salary')
          select_template = request.POST.get('select_template')
          experience_min = request.POST.get('experience_min')
          experience_max = request.POST.get('experience_max')
          description = request.POST.get('description')
          requirements = request.POST.get('requirements')
          about_company = request.POST.get('about_company')
          created_by = request.user
          job= Job(role=role, jobtype=jobtype, salary=salary, select_template=select_template,experience_min=experience_min,experience_max=experience_max, 
                      description=description, requirements=requirements, about_company=about_company,created_by=created_by)
          job.save()
          return redirect('create_application_form', job.pk) 
     return render(request,'create_jobs.html')


def Create_Application_Form(request, jobId):
     job=Job.objects.get(pk=jobId)
     if request.method == 'POST':
          phonenumber = request.POST.get('phonenumber') 
          designation = request.POST.get('designation')
          currentctc = request.POST.get('currentctc')
          expectedctc = request.POST.get('expectedctc')
          skypeid = request.POST.get('skypeid')
          Github_url = request.POST.get('Github_url')
          linkedin_url = request.POST.get('linkedin_url')
          portfolio_url= request.POST.get('portfolio_url')
          resume = request.POST.get('resume')
          experience = request.POST.get('experience')
          skills = request.POST.get('skills')
          email = request.POST.get('email')
          notice = request.POST.get('notice')
          current_location = request.POST.get('current_location')
          full_name = request.POST.get('full_name')
          candidate_application_form = CandidateApplicationForm(phonenumber=bool(phonenumber),
                                                                     designation=bool(designation),
                                                                     currentctc=bool(currentctc),
                                                                     expectedctc=bool(expectedctc), 
                                                                     skypeid=bool(skypeid),
                                                                     Github_url=bool(Github_url),
                                                                     linkedin_url=bool(linkedin_url), 
                                                                     current_location=bool(current_location), 
                                                                     firstname=full_name == 'True',
                                                                     lastname=full_name == 'True', 
                                                                     state=current_location == 'True', 
                                                                     city=current_location == 'True',
                                                                     pincode=current_location == 'True',
                                                                     street=current_location == 'True', 
                                                                     portfolio_url=bool(portfolio_url),
                                                                     resume=bool(resume),
                                                                     experience=bool(experience),
                                                                     skills=bool(skills),
                                                                     email=bool(email),
                                                                     notice=bool(notice),
                                                                     job_ref=job)
               
          candidate_application_form.save()
     return render(request,'create_application_form.html')

def Create_Publish(request):
     return render(request,'create_publish.html')

def Job_Templete(request):
     return render(request, 'job_templete.html')

def Candidate_profile_Edit(request):
     return render(request,'candidate_profile_edit.html')


def JobApplicationStatus(request, id):
     application = JobApplication.objects.filter(pk=id).prefetch_related('applied_by','jobId')
     notes = Notes.objects.filter(application_ref = application.first()).prefetch_related('added_by')
     feedbacks = FeedbackNotes.objects.filter(application_ref = application.first()).prefetch_related('given_by')

     if request.method == 'POST':
          user_note = request.POST.get('user_note')
          note= Notes(user_note = user_note, added_by = request.user, application_ref = application.first())
          note.save()

          if request.method == 'POST':
               user_feedback = request.POST.get('user_feedback')
               communication_rating = request.POST.get('communication_rating')
               logicalskills_rating = request.POST.get('logicalskills_rating')
               techinicalskills_rating = request.POST.get('techinicalskills_rating')
               feedback= FeedbackNotes(user_feedback = user_feedback,communication_rating=communication_rating, logicalskills_rating=logicalskills_rating, techinicalskills_rating=techinicalskills_rating,  given_by = request.user, application_ref = application.first())
               feedback.save()
     return render(request,'candidate_profile.html',{'notes':notes,'feedbacks':feedbacks, 'application':application.first()})


def Candidate_application(request, id):
     job = Job.objects.get(pk=id)
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

               candidate= Candidate(firstname=firstname,lastname=lastname, email=email, phonenumber=phonenumber,designation=designation,
                                   currentctc=currentctc, expectedctc=expectedctc, skypeid=skypeid, Github_url=Github_url,
                                   linkedin_url=linkedin_url,portfolio_url=portfolio_url, resume=resume, street=street,
                                        pincode=pincode,city=city, state=state, experience=experience, skills=skills)
               candidate.save()
               print(candidate)
          else:
               HttpResponse("You have already applied for this job")

          jobApplication = JobApplication(jobId = job, applied_by = candidate, status = 'accepted')
          jobApplication.save()
          print(jobApplication)
          return redirect('jobss') 
     return render(request, 'candidate_application.html')

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

# def update_jobs(request, pk):
#     updatejobs= Job.objects.get(pk=pk)
#     if request.method == 'POST':
#           role = request.POST.get('role')
#           jobtype= request.POST.get('jobtype')
#           salary = request.POST.get('salary')
#           select_template = request.POST.get('select_template')
#           experience_min = request.POST.get('experience_min')
#           experience_max = request.POST.get('experience_max')
#           description = request.POST.get('description')
#           requirements = request.POST.get('requirements')
#           about_company = request.POST.get('about_company')
#           created_by = request.user

#           updatejobs.role = role
#           updatejobs.jobtype = jobtype
#           updatejobs.salary = salary
#           updatejobs.select_template = select_template
#           updatejobs.experience_min = experience_min
#           updatejobs.experience_max = experience_max
#           updatejobs.description = description
#           updatejobs.requirements = requirements
#           updatejobs.about_company = about_company
#           updatejobs.created_by = created_by
#           updatejobs.save()
#           return JsonResponse({'success': True})
