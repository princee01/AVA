from django import forms
from .models import College,Student,Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CollegeRegistrationForm(UserCreationForm):
    college_id = forms.CharField(required=True)
    college_location = forms.CharField(required=True)
    estab_year = forms.IntegerField(required=True)
    college_email = forms.EmailField(required=True)
    college_photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2'] 