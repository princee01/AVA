from django.shortcuts import render, redirect
from .forms import CollegeRegistrationForm
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import College
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')


def register_college(request):
    if request.method == "POST":
        form = CollegeRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the User object
            user = form.save(commit=False)
            user.email = form.cleaned_data['college_email']
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Create College profile linked to this user
            College.objects.create(
                user=user,
                college_name=form.cleaned_data.get('college_name') or user.username,
                college_id=form.cleaned_data['college_id'],
                college_location=form.cleaned_data['college_location'],
                estab_year=form.cleaned_data['estab_year'],
                college_email=form.cleaned_data['college_email'],
                college_photo=form.cleaned_data.get('college_photo')
            )

            # Log in the newly registered college user
            login(request, user)
            return redirect('userpage')
        else:
            print("Form errors:", form.errors)
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
                return redirect('userpage')
        else:
            print("Login errors:", form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user(request):
    auth_logout(request)
    return redirect('home')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required  
def userpage(request):
    college = None
    if hasattr(request.user, 'college'):  # safer check
        college = request.user.college

    return render(request, 'userpage.html', {'college': college})

