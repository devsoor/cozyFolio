from django.shortcuts import render, redirect
from .models import User, Portfolio, Project, Skill, SocialMedia, Job
from .forms import LanguagesForm, FrameworksForm, DatabasesForm, CloudsForm, PDFForm
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timezone, timedelta
import pytz
import pprint
from django.db.models import Q
import json
import ast
import urllib.parse
import os
from datetime import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, 'cozyfolio_app/static/media/')

def index(request):
    return render(request, "index.html")

def deleteProject(request, id):
    to_delete = Project.objects.get(id = id)
    to_delete.delete()
    return redirect('/dashboard')

def deletePortfolio(request, id):
    to_delete = Portfolio.objects.get(id = id)
    to_delete.delete()
    return redirect('/dashboard')

def registerUser(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        registerFormFirstName = request.POST['registerFormFirstName']
        registerFormLastName = request.POST['registerFormLastName']
        registerFormEmail = request.POST['registerFormEmail']
        registerFormPassword = request.POST['registerFormPassword']
        registerFormConfirmPassword = request.POST['registerFormConfirmPassword']
        hashPassword = bcrypt.hashpw(registerFormPassword.encode(), bcrypt.gensalt()).decode()

        this_user = User.objects.filter(email=registerFormEmail)
        if len(this_user) != 0:
            return redirect("/")

        this_user = User.objects.create(firstName=registerFormFirstName, lastName=registerFormLastName, email=registerFormEmail, password=hashPassword)
        smLinkedIn = SocialMedia.objects.create(name="LinkedIn", user=this_user)
        smGithub = SocialMedia.objects.create(name="GitHub", user=this_user)
        smStackoverflow = SocialMedia.objects.create(name="Stack Overflow", user=this_user)
        this_skill = Skill.objects.create(user=this_user)

        request.session["firstName"] = registerFormFirstName
        request.session['userEmail'] = registerFormEmail
        request.session['pickPortfolioID'] = ""
        return redirect("/userProfile")

def signin(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        loginFormEmail = request.POST['loginFormEmail']
        loginFormPassword = request.POST['loginFormPassword']
        user = User.objects.filter(email=loginFormEmail)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(loginFormPassword.encode(), logged_user.password.encode()):
                request.session['userEmail'] = logged_user.email
                request.session["firstName"] = logged_user.firstName
                request.session['pickPortfolioID'] = ""
                return redirect("/dashboard")

        messages.error(request, "Password does not match")
        return redirect("/")

def logout(request):
    try:
        request.session.clear()
    except KeyError:
        print("Exception: ")
        pass
    return redirect("/")

def forgotPassword(request):
    return render(request, "forgotPassword.html")

def forgotPasswordSendEmail(request):
    # Send an email to user with password reset instructions
    return render(request, "newPassword.html")

def setNewPassword(request):
    return render(request, "login.html")

def convertStrToArray(obj):
    x = ast.literal_eval(obj)
    arr = []
    for item in x:
        arr.append(item)
    return arr

def dashboard(request):
    print('THIS FAR')
    this_user = User.objects.get(email=request.session['userEmail'])

    if this_user.skill.languages != None:
        langList = convertStrToArray(this_user.skill.languages) 
    else:
        langList = []

    if this_user.skill.frameworks != None:
        fwList = convertStrToArray(this_user.skill.frameworks)
    else:
        fwList = []

    if this_user.skill.databases != None:
        dbList = convertStrToArray(this_user.skill.databases)
    else:
        dbList = []

    if this_user.skill.clouds != None:    
        cloudList = convertStrToArray(this_user.skill.clouds)
    else:
        cloudList = []
       
    userPortfolios = this_user.portfolio.all()
    projects = Project.objects.all()
    jobs = Job.objects.all()

    all_resumes = this_user.resume
    print(all_resumes)
    
    if request.session['pickPortfolioID']:
        pickedPortfolio = Portfolio.objects.get(id=request.session['pickPortfolioID'])
        pickedProjects = Project.objects.filter(portfolio=pickedPortfolio)

    else:
        pickedProjects = []

    smLinkedIn = SocialMedia.objects.get(name="LinkedIn", user=this_user)
    smGithub = SocialMedia.objects.get(name="GitHub", user=this_user)
    smStackoverflow = SocialMedia.objects.get(name="Stack Overflow", user=this_user)

    context = {
        "this_user": this_user,
        "portfolios": userPortfolios,
        "projects": projects,
        "jobs": jobs,
        "langList": langList,
        "fwList": fwList,
        "dbList": dbList,
        "cloudList": cloudList,
        'resumes': all_resumes,
        "smLinkedIn": smLinkedIn,
        "smGithub": smGithub,
        "smStackoverflow":smStackoverflow,
        "pickedProjects": pickedProjects,
    }
    return render(request, "dashboard.html", context)

#
# Portfolio functions==========================================================================================
#
def portfolioCreate(request):
    newName  = request.POST['portfolioFormName']
    newTitle = request.POST['portfolioFormJobTitle']
    newSummary = request.POST['portfolioFormSummary']
    # newResume = request.POST['portfolioFormResume']
    projList = request.POST.getlist('checks[]')
    newUser = User.objects.get(email = request.session['userEmail'])
    newPort = Portfolio.objects.create(name = newName, title = newTitle, portfolioSummary = newSummary,user = newUser)

    for i in projList:
        if Project.objects.get(id = i) in newPort.project.all():
            continue
        newPort.project.add(Project.objects.get(id = i))
    return redirect('/dashboard')
    
def portfolioNew(request):
    currUser = User.objects.get(email = request.session['userEmail'])
    allProj = currUser.project.all()
    context = {
        'projects': allProj
    }
    return render(request, "portfolio.html",context)

def assignProject(request,val):
    projectToAdd = Project.objects.get(id = val)
    context = {
        'addedProjects': projectToAdd,
    }
    return render(request,'portfolioEdit.html',context)

def portfolioEdit(request, id):
    portfolioToEdit = Portfolio.objects.get(id = id)
    currUser = User.objects.get(email = request.session['userEmail'])
    allProj = currUser.project.all()
    assignedProjects = portfolioToEdit.project.all()
    #Below makes project available to portfolio
    context = {
        'portfolio' : portfolioToEdit,
        'projects':allProj,
        'assignedProjects':assignedProjects,
    }
    return render(request, "portfolioEdit.html",context)

def portfolioUpdate(request,id):
    updatedName  = request.POST['portfolioFormName']
    updatedTitle = request.POST['portfolioFormJobTitle']
    updatedSummary = request.POST['portfolioFormSummary']
    updatedResume = request.POST['portfolioFormResume']
    newProjList = request.POST.getlist('checks[]')
    portToBeUpdated = Portfolio.objects.get(id = id)
    for i in newProjList:
        if Project.objects.get(id = i) in portToBeUpdated.project.all():
            continue
        portToBeUpdated.project.add(Project.objects.get(id = i))
    portToBeUpdated.name = updatedName
    portToBeUpdated.title = updatedTitle
    portToBeUpdated.portfolioSummary = updatedSummary
    portToBeUpdated.resume = updatedResume
    portToBeUpdated.save()
    return redirect('/dashboard')

def pickPortfolio(request, id):
    request.session['pickPortfolioID'] = id

    return redirect('/dashboard')
#
# Project functions=============================================================================================
#
def projectCreate(request):
    newName  = request.POST['projectFormName']
    newSummary = request.POST['projectFormSummary']
    newTech = request.POST['projectFormTech']
    newTeam = request.POST['projectFormTeam'] 
    newProcess = request.POST['projectFormProcess']
    newURL = request.POST['projectFormURL']
    newUser = User.objects.get(email = request.session['userEmail'])
    Project.objects.create(name = newName, summary = newSummary, techUsed = newTech, team = newTeam, process = newProcess, url = newURL,user = newUser )
    return redirect('/dashboard')

def projectNew(request):
    return render(request, "project.html")

def projectUpdate(request,id):
    updatedName  = request.POST['projectFormName']
    updatedSummary = request.POST['projectFormSummary']
    updatedTech = request.POST['projectFormTech']
    updatedTeam = request.POST['projectFormTeam'] 
    updatedProcess = request.POST['projectFormProcess']
    updatedURL = request.POST['projectFormURL']
    projectToBeUpdated = Project.objects.get(id = id)
    projectToBeUpdated.name = updatedName
    projectToBeUpdated.summary = updatedSummary
    projectToBeUpdated.techUsed = updatedTech
    projectToBeUpdated.team = updatedTeam
    projectToBeUpdated.process = updatedProcess
    projectToBeUpdated.url = updatedURL
    projectToBeUpdated.save()
    return redirect('/dashboard')

def projectEdit(request, id):
    projectToEdit = Project.objects.get(id = id);
    context = {
        'project' : projectToEdit
    }
    return render(request, "projectEdit.html",context)

#
# User functions
#
def userProfile(request):
    this_user = User.objects.get(email=request.session['userEmail'])

    formLanguages = LanguagesForm
    formFrameworks = FrameworksForm
    formDatabases = DatabasesForm
    formClouds = CloudsForm
    pdfForm = PDFForm()
    this_user = User.objects.get(email=request.session['userEmail'])
    all_res = this_user.resume
    print("=============================================all_res",all_res)
    smLinkedIn = SocialMedia.objects.get(name="LinkedIn", user=this_user)
    smGithub = SocialMedia.objects.get(name="GitHub", user=this_user)
    smStackoverflow = SocialMedia.objects.get(name="Stack Overflow", user=this_user)

    context = {
        "this_user": this_user,
        "formLanguages": formLanguages,
        "formFrameworks": formFrameworks,
        "formDatabases": formDatabases,
        "formClouds": formClouds,
        'pdfForm':pdfForm,
        'resumes': all_res,
        "smLinkedInUrl": smLinkedIn.url,
        "smGithubUrl": smGithub.url,
        "smStackoverflowUrl": smStackoverflow.url,
    }
    return render(request, "userProfile.html", context)

def userCreate(request):
    errors = User.objects.userProfile_validator(request.POST, request.FILES)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        this_user = User.objects.get(email=request.session['userEmail'])

        this_user.firstName = request.POST["profileFormFirstName"]
        this_user.lastName = request.POST["profileFormLastName"]
        this_user.email = request.POST["profileFormEmail"]
        this_user.title = request.POST["profileFormTitle"]
        this_user.tagLine = request.POST["profileFormTagline"]
        this_user.address = request.POST["profileFormAddress"]
        this_user.country = request.POST["country"]
        this_user.state = request.POST["state"]
        this_user.city = request.POST["city"]
        this_user.profileHighlight = request.POST["profileHighlight"]


        # get social media
        profileFormLinkedIn = request.POST["profileFormLinkedIn"]
        profileFormGithub = request.POST["profileFormGithub"]
        profileFormStackoverflow = request.POST["profileFormStackoverflow"]
        smLinkedIn = SocialMedia.objects.get(name="LinkedIn", user=this_user)
        smLinkedIn.url = profileFormLinkedIn
        smLinkedIn.save()
        smGithub = SocialMedia.objects.get(name="GitHub", user=this_user)
        smGithub.url = profileFormGithub
        smGithub.save()
        smStackoverflow = SocialMedia.objects.get(name="Stack Overflow", user=this_user)
        smStackoverflow.url = profileFormStackoverflow
        smStackoverflow.save()

        formLanguages = LanguagesForm(request.POST)
        formFrameworks = FrameworksForm(request.POST)
        formDatabases = DatabasesForm(request.POST)
        formClouds = CloudsForm(request.POST)

        uploaded_file = request.FILES['profileFormResume']
        print("======================== uploaded file",uploaded_file)
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        this_user.resume = fs.url(name)
        print("======================== this_user.resume file",this_user.resume)


        # if request.method =='POST':
        #     resumefile = request.FILES['profileFormResume']
        #     fs = FileSystemStorage()
        #     resume_filename = fs.save(resumefile.name, resumefile)
        #     this_user.resume = fs.url(resume_filename)
        #     print("------------")

        # request.session['requestFiles'] = request.FILES

        headshotfile = request.FILES['profileFormHeadshot']
        fs = FileSystemStorage()
        headshot_filename = fs.save(headshotfile.name, headshotfile)
        this_user.headshot = fs.url(headshot_filename)

        if formLanguages.is_valid():
            languages = formLanguages.cleaned_data.get('languages')
        else:
            languages = []

        if formFrameworks.is_valid():
            frameworks = formFrameworks.cleaned_data.get('frameworks')
        else:
            frameworks = []

        if formDatabases.is_valid():
            databases = formDatabases.cleaned_data.get('databases')
        else:
            databases = []

        if formClouds.is_valid():
            clouds = formClouds.cleaned_data.get('clouds')
        else:
            clouds = []

        skill = Skill.objects.get(user=this_user)
        skill.languages = languages
        skill.frameworks = frameworks
        skill.databases = databases
        skill.clouds = clouds
        skill.save()

        this_user.save()
        request.session["firstName"] = this_user.firstName
        request.session['userEmail'] = this_user.email

        return redirect("/dashboard")


#
# Website stuff
#
def websitePreview(request):
    user = User.objects.get(email=request.session['userEmail'])
    portfolios = Portfolio.objects.all()
    projects = Project.objects.all()
    skills = Skill.objects.all()

    context = {
        "user": user,
        "portfolios": portfolios,
        "projects": projects,
        "skills": skills,
    }
    return render(request, "websitePreview.html", context)

def websiteCreate(request):
    this_user = User.objects.get(email=request.session['userEmail'])
    portfolios = Portfolio.objects.all()
    projects = Project.objects.all()
    if this_user.skill.languages != None:
        langList = convertStrToArray(this_user.skill.languages) 
    else:
        langList = []

    if this_user.skill.frameworks != None:
        fwList = convertStrToArray(this_user.skill.frameworks)
    else:
        fwList = []

    if this_user.skill.databases != None:
        dbList = convertStrToArray(this_user.skill.databases)
    else:
        dbList = []

    if this_user.skill.clouds != None:    
        cloudList = convertStrToArray(this_user.skill.clouds)
    else:
        cloudList = []

    context = {
        "this_user": this_user,
        "portfolios": portfolios,
        "projects": projects,
        "languages": langList,
        "fwList": fwList,
        "dbList": dbList,
        "cloudList": cloudList,
    }
    return render(request, "websiteCreate.html", context)

def applyJob(request):
    allPortfolios = Portfolio.objects.all()
    context = {
        "allPortfolios":allPortfolios,
    }
    return render(request, "applyJob.html", context)

def viewJob(request):
    this_user = User.objects.get(email=request.session['userEmail'])
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=  request.POST['JobFormforportfolio']", request.POST['JobFormforportfolio'])

    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/applyJob')

    title = request.POST['JobFormtitle']
    company = request.POST['JobFormCompanyName']
    applyDate = request.POST['JobFormforapplyDate']
    respondDate = request.POST['JobFormforrespondDate']
    response = request.POST['JobFormforresponse']
    estSalary = request.POST['JobFormforestSalary']
    portfolioId = request.POST['JobFormforportfolio']
    offerReject = request.POST['jobFormforreject']
    offerReceived = request.POST['jobFormforoffer']
    thisPortfolio = Portfolio.objects.get(id=portfolioId)

    newJob = Job.objects.create(jobTitle=title, company=company, applyDate=applyDate, respondDate=respondDate, response=response, estSalary=estSalary, portfolio=thisPortfolio, user=this_user, offerReject=offerReject, offerReceived=offerReceived)
    return redirect("/dashboard")

def updateJob(request,id):
    this_job = Job.objects.get(id=id)
    allPortfolios = Portfolio.objects.all()

    responseDate = datetime.strftime(this_job.respondDate, "%Y-%m-%d")
    appliedDate = datetime.strftime(this_job.applyDate, "%Y-%m-%d")

    context ={
        "this_job" : this_job,
        "allPortfolios": allPortfolios,
        "responseDate": responseDate,
        "appliedDate": appliedDate,
    }
    return render(request,"updateJob.html", context)


def newJob(request,id):
    this_user = User.objects.get(email=request.session['userEmail'])
    this_job = Job.objects.get(id=id)

    this_job.jobTitle = request.POST['JobFormtitle']
    this_job.company = request.POST['JobFormCompanyName']
    this_job.applyDate = request.POST['JobFormforapplyDate']
    this_job.respondDate = request.POST['JobFormforrespondDate']
    this_job.response = request.POST['JobFormforresponse']
    this_job.estSalary = request.POST['JobFormforestSalary']
    this_job.offerReject = request.POST['jobFormforreject']
    this_job.offerReceived = request.POST['jobFormforoffer']
    this_job.portfolio = Portfolio.objects.get(id=request.POST['JobFormforportfolio'])

    this_job.save()

    return redirect("/dashboard")

def jobStatistic(request):
    this_user = User.objects.get(email=request.session['userEmail'])
    this_job = Job.objects.all()
    numbofJobApplied = this_job.count()

    clist = Job.objects.order_by('company')
    companyList = []
    for c in clist:
        companyList.append(c.company)

    numbofCompanyApplied = len(set(companyList))

    offerReceived = len(Job.objects.filter(offerReceived=1))
    print("offerReceived", offerReceived)

    offerReject = len(Job.objects.filter(offerReject=1))
    print("offerReject", offerReject)


    response = len(Job.objects.filter(response=1))
    print("response", response)


    context ={
        "this_job" : this_job,
        "numbofJobApplied": numbofJobApplied,
        "numbofCompanyApplied": numbofCompanyApplied,
        "offerReceived": offerReceived,
        "offerReject": offerReject,
        "response": response,
    }

    return render(request,"jobStatistic.html", context)
