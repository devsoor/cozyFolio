from django.shortcuts import render, redirect
from .models import User, Portfolio, Project, Skill, SocialMedia
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timezone, timedelta
import pytz
import pprint
from django.db.models import Q


# Skill.objects.create(languages = langList, frameworks = frameworkList, databases = databaseList, other = otherList)


def index(request):
    return render(request, "index.html")

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

        User.objects.create(firstName=registerFormFirstName, lastName=registerFormLastName, email=registerFormEmail, password=hashPassword)
        request.session["firstName"] = registerFormFirstName
        request.session['userEmail'] = registerFormEmail
        return redirect("/dashboard")

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

def dashboard(request):
    this_user = User.objects.get(email=request.session['userEmail'])
    this_user.city = "Seattle"
    this_user.state = "WA"
    this_user.title = "Full Stack Developer"
    this_user.resume = "static/img/resume_sample.pdf"
    this_user.resume.name = f"{this_user.firstName}_{this_user.lastName}.pdf"
    this_user.skillSet = {
        "Languages": ["Python", "JavaScript", "C#", "Java", "PHP", "Ruby", "C/C++", "SQL", "Swift", "Go"],
        "Frameworks": ["Angular", "Django", "Vue", "React", ".NET"],
        "Databases": ["MySQL", "MariaDB", "MongoDB", "PostgreSQL", "DynamoDB", "Amazon Aurora"],
        "Other":["other skills"]
    }
    this_user.headShot = "https://mdbootstrap.com/img/Photos/Others/men.jpg"
    this_user.profileHighlight = "There are many variations of passages of Lorem Ipsum available, but the majority have suffered alteration in some form, by injected humour, or randomised words which don't look even slightly believable. If you are going to use a passage of Lorem Ipsum, you need to be sure there isn't anything embarrassing hidden in the middle of text. All the Lorem Ipsum generators on the Internet tend to repeat predefined chunks as necessary, making this the first true generator on the Internet."
    # create a temp portfolio and list of projects

    portfolios = ["Full-Stack Developer", "Front-end Developer", "Product Manager"]
    projects = [
        {
            "id": 1,
            "name":"Python Stack",
            "type": "Bootcamp",
            "image": "https://mdbootstrap.com/img/Photos/Horizontal/Nature/8-col/img%20(73).jpg",
            "description":"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry'sstandard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages"
        },
        {
            "id": 2,
            "name":"C-Sharp Stack",
            "type": "Bootcamp",
            "image": "https://mdbootstrap.com/img/Photos/Others/images/31.jpg",
            "description":"It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy."
        },
        {
            "id": 3,
            "name":"MEAN Stack",
            "type": "Bootcamp",
            "image": "https://mdbootstrap.com/img/Photos/Others/images/52.jpg",
            "description":"Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source."
        },
   ]

    socialMedia = {"linkedin": "https://www.linkedin.com/in/devsoor/", "gitHub":"https://github.com/devsoor/PythonStack"}
    context = {
        "this_user": this_user,
        "portfolios": portfolios,
        "projects": projects,
        "socialMedia": socialMedia,
    }
    return render(request, "dashboard.html", context)

#
# Portfolio functions
#
def portfolioEdit(request, id):
    return render(request, "portfolio.html")


#
# Project functions
#
def projectEdit(request, id):
    return render(request, "editProject.html")

#
# User functions
#
def userProfile(request):
    #create arr of lang list create arr of social media, two methods initializing the two models
    langList =["Python","JavaScript", "HTML/CSS","Java", "C/C++","Swift","TypeScript","Go","SQL","Ruby","R",
    "PHP","Perl","Kotlin","C#","Rust","Scheme","Erlang","Scala","Elixir","Haskell","Basic"]
    frameworkList = ["Ruby on Rails", 'Django', "Laravel", 'Symfony', 'Meteor', "Angular", "Yii", "Play", "React", "Flask", "Phoenix", 
    "Spring", "CakePHP", "Vue", "TensorFlow", "PyTorch","Sonnet","Keras","MXNet", "Gluon","Chainer","DL4J","ONNX"]
    databaseList = ["MySQL", "Microsoft SQL Server", "PostgreSQL", "IBM Db2 Family", "Microsoft Access", "MariaDB", 
    "SQLite", "IBM Informix", "MongoDB", "Redis"]

    this_user = User.objects.get(email=request.session['userEmail'])
    context = {
        "langList": langList,
        "frameworkList": frameworkList,
        "databaseList": databaseList,
        "this_user": this_user,
    }
    return render(request, "userProfile.html", context)


def userCreate(request):
    pprint.pprint(request.POST)
    print("request.method = ", request.method)
    errors = User.objects.userProfile_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        this_user = User.objects.get(email=request.session['userEmail'])

        profileFormFirstName = request.POST["profileFormFirstName"]
        profileFormLastName = request.POST["profileFormLastName"]
        profileFormEmail = request.POST["profileFormEmail"]
        profileFormTitle = request.POST["profileFormTitle"]
        profileFormAddress = request.POST["profileFormAddress"]
        country = request.POST["country"]
        state = request.POST["state"]
        city = request.POST["city"]
        profileFormResume = request.POST["profileFormResume"]
        profileFormHeadshot = request.POST["profileFormHeadshot"]
        profileFormLinkedIn = request.POST["profileFormLinkedIn"]
        profileFormGithub = request.POST["profileFormGithub"]
        profileFormStackoverflow = request.POST["profileFormStackoverflow"]
        languages = request.POST.getlist("languages", None)
        frameworks = request.POST.getlist("frameworks")
        databases = request.POST.getlist("databases")
        profileHighlight = request.POST["profileHighlight"]

        this_user.firstName = profileFormFirstName
        this_user.lastName = profileFormLastName
        this_user.email = profileFormEmail
        this_user.title = profileFormTitle
        this_user.address = profileFormAddress
        this_user.country = country
        this_user.state = state
        this_user.city = city
        this_user.profileHighlight = profileHighlight
        this_user.resume = profileFormResume
        this_user.headshot = profileFormHeadshot

        smLinkedIn = SocialMedia.objects.create(name="LinkedIn", url=profileFormLinkedIn, logo="/static/img/linkedin.png")
        smGithub = SocialMedia.objects.create(name="GitHub", url=profileFormGithub, logo="/static/img/github.png")
        smStackoverflow = SocialMedia.objects.create(name="StackOverflow", url=profileFormStackoverflow, logo="/static/img/stackoverflow.png")
        smLinkedIn.user = this_user
        smGithub.user = this_user
        smStackoverflow.user = this_user

        this_user.skill.languages = languages
        this_user.skill.databases = databases
        this_user.skill.frameworks = frameworks
        
        this_user.save()
        request.session["firstName"] = profileFormFirstName
        request.session['userEmail'] = profileFormEmail

        return redirect("/dashboard")
