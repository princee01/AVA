from django import forms
from .models import College,Student,Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CollegeRegistrationForm(UserCreationForm):
    college_name = forms.CharField(required=True)
    college_id = forms.CharField(required=True)
    college_location = forms.CharField(required=True)
    estab_year = forms.IntegerField(required=True)
    college_email = forms.EmailField(required=True)
    college_photo = forms.ImageField(required=False)
    bgimage=forms.ImageField()
    description=forms.CharField()
    contact1=forms.IntegerField()
    contact2=forms.IntegerField()
    contact3=forms.IntegerField()
    #achievement section
    Aimage1=forms.ImageField()
    Atext1=forms.CharField()
    Aimage2=forms.ImageField()
    Atext2=forms.CharField()
    Aimage3=forms.ImageField()
    Atext3=forms.CharField()
    #for advantage section
    Advimage=forms.ImageField()
    Advtext=forms.CharField()
    #for awards/ranking section
    awardtext=forms.CharField()
    p_detail1=forms.CharField()
    p_detail2=forms.CharField()


    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'college_name', 'college_email']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'enroll_no','course', 'dob', 'location', 'email_id']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'})
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['doc_no','document_name', 'doc_id', 'issued_date', 'file']  # removed issued_by, issued_to
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }



class UploadDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["doc_no","document_name", "doc_id", "issued_date", "file"]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }

class IssueDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["doc_no","document_name", "doc_id", "issued_date", "file"]
        widgets = {
            'issued_date': forms.DateInput(attrs={'type': 'date'}),
        }
