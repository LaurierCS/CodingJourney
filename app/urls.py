from django.urls import path
from . import views

urlpatterns = [
    path('', views.langing_page, name="landing_page"),
    path('home', views.homepage, name='home_page'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.register, name="register"),
    path('projectInput/', views.projectInput, name="project_input"),
    path('projectList/', views.projectList, name="project_list"),
]
