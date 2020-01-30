from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('home', views.signin),	      
    path('', views.index),	      
    path('register', views.register),	      
    path('registerUser', views.registerUser),	      
    path('login', views.login),	      
    path('signin', views.signin),	      
    path('logout', views.logout),
    path('forgotPassword', views.forgotPassword),
    path('forgotPasswordSendEmail', views.forgotPasswordSendEmail),
    path('setNewPassword', views.setNewPassword),
    path('dashboard', views.dashboard),
    path('userProfile', views.userProfile),
    path('userCreate', views.userCreate),
    path('portfolioNew', views.portfolioNew),
    path('portfolioCreate', views.portfolioCreate),
    path('portfolioEdit/<int:id>', views.portfolioEdit),
    path('portfolioEdit/portfolioUpdate/<int:id>', views.portfolioUpdate),
    path('portfolioEdit/assignProject/<int:val>',views.assignProject),
    path('pickPortfolio/<int:id>', views.pickPortfolio),
    # path('portfolioSave/<int:id>', views.portfolioSave),
    path('projectCreate', views.projectCreate),
    path('projectNew', views.projectNew),
    path('projectEdit/<int:id>', views.projectEdit),
    path('projectEdit/projectUpdate/<int:id>', views.projectUpdate),
    # path('projectSave/<int:id>', views.projectSave),
    path('websitePreview', views.websitePreview),
    path('websiteCreate', views.websiteCreate),
    path('applyJob', views.applyJob),
    path('viewJob', views.viewJob),
    path('jobStatistic', views.jobStatistic),
    path('updateJob/<int:id>', views.updateJob),
    path('newJob/<int:id>', views.newJob),

]

if settings:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)