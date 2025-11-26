from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-college/',views.register_college,name="register_college"),
    path('login/', views.login_college, name='login_college'),
    path('user-page/',views.userpage,name="userpage")
    
]