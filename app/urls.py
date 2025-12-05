from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-college/',views.register_college,name="register_college"),
    path('login/', views.login_college, name='login_college'),
    path('user-page/',views.userpage,name="userpage"),
    path('stats/',views.stats,name="stats"),
    path('students/register/', views.register_student, name='register_student'),
    path('students/<int:id>/docs/issue/', views.issue_document, name='issue_document'),
    path('students/<int:id>/docs/upload/', views.upload_document, name='upload_document'),
    path('students/<int:id>/docs/', views.view_documents, name='view_documents'),
    path('students/<int:id>/delete/', views.delete_student, name='delete_student'),

]