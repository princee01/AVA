from django.shortcuts import render, redirect
from .forms import CollegeRegistrationForm,StudentForm
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import College,Student
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
                college_photo=form.cleaned_data.get('college_photo'),
                bgimage=form.cleaned_data.get('bgimage'),

                description=form.cleaned_data.get('description'),
                contact1=form.cleaned_data.get('contact1'),
                contact2=form.cleaned_data.get('contact2'),
                contact3=form.cleaned_data.get('contact3'),

                # Achievement Section
                Aimage1=form.cleaned_data.get('Aimage1'),
                Atext1=form.cleaned_data.get('Atext1'),
                Aimage2=form.cleaned_data.get('Aimage2'),
                Atext2=form.cleaned_data.get('Atext2'),
                Aimage3=form.cleaned_data.get('Aimage3'),
                Atext3=form.cleaned_data.get('Atext3'),

                # Advantage Section
                Advimage=form.cleaned_data.get('Advimage'),
                Advtext=form.cleaned_data.get('Advtext'),

                # Awards / Ranking Section
                awardtext=form.cleaned_data.get('awardtext'),
                p_detail1=form.cleaned_data.get('p_detail1'),
                p_detail2=form.cleaned_data.get('p_detail2'),
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





def register_student(request):
    college = College.objects.get(user=request.user)  # logged-in college

    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.college = college  # assign college automatically
            student.save()
            return redirect('stats')  # redirect to student list page

    else:
        form = StudentForm()

    return render(request, "registration/register_student.html", {"form": form})

@login_required
def stats(request):
    college = College.objects.get(user=request.user)
    students = college.students.all()

    return render(request, "stats.html", {"students": students})

def student_docs(request, id):
    student = Student.objects.get(id=id)
    return render(request, "docs.html", {"student": student})




    



