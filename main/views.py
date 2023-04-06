from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.conf.urls.static import static
from django.template import loader
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count


from .models import Recruiter, Job, Candidate, JobApplication, Notes, FeedbackNotes
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
     Job_list = Job.objects.all()
     Count_jobs = Job.objects.values_list('role').count()
     Count_cand = Candidate.objects.values_list('firstname').count()
     jobs= Job.objects.all()
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 

     return render(request, 'Dashboard.html',{'Job_list':Job_list,'Count_jobs':Count_jobs,'Count_cand':Count_cand,'jobs':job_objects})

def LogoutPage(request):
     logout(request)
     return redirect('login')

def JobDetails(request):
    return render(request,'job_details.html')

def Jobs(request):
     Count_jobs = Job.objects.values_list('role').count()
     jobs= Job.objects.all()
     job_objects = [{'count':JobApplication.objects.filter(jobId=job).count(), 'job':job} for job in jobs] 
     return render(request,'jobs.html', {'jobs':job_objects,'Count_jobs':Count_jobs})

def Jobs_List(request, id):
     job=Job.objects.get(pk=id)
     applications= JobApplication.objects.filter(jobId = job).prefetch_related('applied_by')
     return render(request,'jobs_list.html',{'applications':applications,'job':job})

def Candidates_list(request):
     Candidate_list = Candidate.objects.all()
     # applications = JobApplication.objects.filter(jobId=Candidate_list)
     # print(applications)
     # job=Candidate.objects.all()
     # applications= JobApplication.objects.prefetch_related('applied_by')
     Candidates_count = Candidate.objects.values_list('firstname').count()
     return render(request,'candidates_list.html',{'Candidate_list':Candidate_list  })

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
          return redirect('create_application_form') 
     return render(request,'create_jobs.html')


def Create_Application_Form(request):
     return render(request,'create_application_form.html')

def Create_Publish(request):
     return render(request,'create_publish.html')

def Job_Templete(request):
     return render(request, 'job_templete.html')

def Candidate_profile_Edit(request):
     return render(request,'candidate_profile_edit.html')


def Candidate_profile(request, id):
     job=Candidate.objects.get(pk=id)
     applications= JobApplication.objects.filter(applied_by = job).prefetch_related('jobId')
     print("Test", job,applications)

     # if request.method =='POST':
     #      note= user_note= request.POST.get(' user_note'), application_id=applications)
     #      note.save()
     #      return redirect('candidate_profile') 

     return render(request,'candidate_profile.html',{'applications':applications,'job':job})


def Candidate_application(request, id):
     job = Job.objects.get(pk=id)
     
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
