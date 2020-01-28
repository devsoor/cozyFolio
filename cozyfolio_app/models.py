from django.db import models

# Create your models here.
from django.db import models
import re
import bcrypt
from datetime import date, datetime, timedelta
import pprint

# Create your models here.
class UserManager(models.Manager):
    def register_validator(self, postData):
        if not postData:
            return
        errors = {}
        NAME_REGEX = re.compile ('[a-zA-Z_]')

        if NAME_REGEX.match(postData['registerFormFirstName']) == None or len(postData['registerFormFirstName']) < 2:
            errors["registerFormFirstName"] = "First name must be all letters and length atleast 2 characters long"

        if NAME_REGEX.match(postData['registerFormLastName']) == None or len(postData['registerFormLastName']) < 2:
            errors["registerFormLastName"] = "Last name must be all letters and length atleast 2 characters long"


        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['registerFormEmail']) or len(postData['registerFormEmail']) == 0:           
            errors['registerFormEmail'] = "Invalid email address!"

        # regular email uniqueness check
        if User.objects.filter(email=postData['registerFormEmail']).exists():
            errors['usertaken'] = "This user email already exists"

        if len(postData['registerFormPassword']) < 8:
            errors['registerFormPassword'] = "Password must be atleast 8 characters long"

        if len(postData['registerFormConfirmPassword']) < 8:
            errors['confirmregisterFormConfirmPassword_pw'] = "Confirm Password must be atleast 8 characters long"

        if postData['registerFormConfirmPassword'] != postData['registerFormConfirmPassword']:
            errors['pw_match'] = "Passwords do not match"

        return errors

    def login_validator(self, postData):
        if not postData:
            return
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['loginFormEmail']) or len(postData['loginFormEmail']) == 0:           
            errors['loginFormEmail'] = "Invalid email address!"

        current_emails = User.objects.filter(email=postData['loginFormEmail'])
        if len(current_emails) == 0:
                errors['userunknown'] = "This user email does not exist"

        if len(postData['loginFormPassword']) < 8:
            errors['loginFormPassword'] = "Password must be atleast 8 characters long"

        return errors

    def userProfile_validator(self, postData):
        if not postData:
            return
        errors = {}
        NAME_REGEX = re.compile ('[a-zA-Z_]')

        if NAME_REGEX.match(postData['profileFormFirstName']) == None or len(postData['profileFormFirstName']) < 2:
            errors["profileFormFirstName"] = "First name must be all letters and length atleast 2 characters long"

        if NAME_REGEX.match(postData['profileFormLastName']) == None or len(postData['profileFormLastName']) < 2:
            errors["profileFormLastName"] = "Last name must be all letters and length atleast 2 characters long"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['profileFormEmail']) or len(postData['profileFormEmail']) == 0:           
            errors['profileFormEmail'] = "Invalid email address!"

        if len(postData['profileFormEmail']) < 8:
            errors['profileFormEmail'] = "Password must be atleast 8 characters long"

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=75)
    lastName = models.CharField(max_length=75)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    # password = models.EMailField()
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=10, null=True)
    city = models.CharField(max_length=100, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    title = models.CharField(max_length=100, null=True)
    profileHighlight = models.TextField(null=True)
    resume = models.FileField(upload_to='uploads/', null=True)
    headshot = models.ImageField(upload_to='uploads/', null=True)
    # skillLanguages = models.TextField(null=True) #using json to 'cast' list into a string
    # skillFrameWorks = models.TextField(null=True) #using json to 'cast' list into a string
    # skillDatabases = models.TextField(null=True) #using json to 'cast' list into a string
    # skillOther = models.TextField(null=True) #using json to 'cast' list into a string
    # socialM = models.TextField(null=True) #using json to 'cast' list into a string
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"User object: {self.id} {self.firstName} {self.lastName}"

class Portfolio(models.Model):
    name = models.CharField(max_length=75)
    title = models.CharField(max_length=100, null=True)
    portfolioSummary = models.TextField(null=True)
    resume = models.FileField(upload_to='uploads/', null=True)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name = "portfolio", on_delete = models.CASCADE, null = True)
    
class Project(models.Model):
    name = models.CharField(max_length=75)
    summary = models.TextField(null=True)
    techUsed = models.TextField(null=True)
    team = models.TextField(null=True)
    process = models.TextField(null=True)
    # video and slide best field?
    # projectVideo = models.ImageField(upload_to='uploads/', null=True)
    # slides = models.FileField(upload_to='uploads/', null=True)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    portfolio = models.ManyToManyField(Portfolio, related_name = "project")

class Skill(models.Model):
    languages = models.TextField(null=True) #using json to 'cast' list into a string
    frameworks = models.TextField(null=True) #using json to 'cast' list into a string
    databases = models.TextField(null=True) #using json to 'cast' list into a string
    other = models.TextField(null=True) #using json to 'cast' list into a string
    # clouds was added
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True)
    portfolio = models.OneToOneField(Portfolio, on_delete = models.CASCADE, null = True)
    project = models.OneToOneField(Project, on_delete = models.CASCADE, null = True)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)

class SocialMedia(models.Model):
    name = models.CharField(max_length = 100, null=True)
    url = models.CharField(max_length = 255, null=True)
    logo = models.ImageField(upload_to='uploads/', null=True)
    created_at = models.DateField(default=datetime.now)
    updated_at = models.DateField(auto_now=True)
    user = models.ForeignKey(User, related_name = "socialMedia", on_delete = models.CASCADE, null = True)
