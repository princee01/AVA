from django.shortcuts import render,redirect
from .forms import CollegeRegistrationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import College


# Create your views here.
def home(request):
    return render(request,'home.html')

def register_college(request):
    if request.method == "POST":
        form = CollegeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['college_email']
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            # Create College profile
            College.objects.create(
                user=user,
                college_name=user.username,
                college_id=form.cleaned_data['college_id'],
                college_location=form.cleaned_data['college_location'],
                estab_year=form.cleaned_data['estab_year'],
                college_email=form.cleaned_data['college_email'],
                college_photo=form.cleaned_data.get('college_photo')
            )
           

            login(request, user)
            return redirect('userpage')
    else:
        form = CollegeRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_college(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('userpage')  # redirect to home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def userpage(request):
    return render(request,'userpage.html')
