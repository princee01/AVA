import uuid
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CollegeRegistrationForm,StudentForm,DocumentForm,UploadDocumentForm, IssueDocumentForm
from datetime import date
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import College,Student,Document
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

from django.db.models import Q
from django.db.models import Count
@login_required
def stats(request):
    college = College.objects.get(user=request.user)
    query = request.GET.get('query', '')

    students = college.students.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(course__icontains=query)|
            Q(location__icontains=query)
        )

    # Count students grouped by course
    course_counts = (
        college.students.values('course')
        .annotate(total=Count('id'))
        .order_by('course')
    )    

    return render(request, "stats.html", {"students": students,"course_counts": course_counts,})

from django.utils import timezone
def student_docs(request, id):
    student = get_object_or_404(Student, id=id)
    college = College.objects.get(user=request.user)

    documents = Document.objects.filter(student=student)

    add_form = UploadDocumentForm()
    issue_form = IssueDocumentForm()

    if request.method == "POST":

        # ---------------------------
        # CASE 1 → Upload Document
        # ---------------------------
        if "issue_document" not in request.POST:
            add_form = UploadDocumentForm(request.POST, request.FILES)

            if add_form.is_valid():
                doc = add_form.save(commit=False)
                doc.student = student
                doc.college = college

                # NEW: Store issuing college properly
                doc.issued_by_college = college
                doc.issued_by_name = college.college_name
                doc.issued_to = student.name
                doc.status = "Uploaded"

                # DOC_NO VERIFICATION LOGIC
                matching_doc = Document.objects.filter(doc_no=doc.doc_no).first()
                if matching_doc:
                    if matching_doc.issued_by_college == college:
                        doc.status = "Verified"
                    else:
                        doc.status = "Fake"
                else:
                    doc.status = "Pending"

                doc.save()
                return redirect("student_docs", id=student.id)

        # ---------------------------
        # CASE 2 → Issue Document
        # ---------------------------
        else:
            issue_form = IssueDocumentForm(request.POST, request.FILES)

            if issue_form.is_valid():
                doc = issue_form.save(commit=False)
                doc.student = student
                doc.college = college

                doc.issued_by_college = college
                doc.issued_by_name = college.college_name
                doc.issued_to = student.name
                doc.status = "Issued"

                # DOC_NO VERIFICATION LOGIC
                matching_doc = Document.objects.filter(doc_no=doc.doc_no).first()
                if matching_doc:
                    if matching_doc.issued_by_college == college:
                        doc.status = "Verified"
                    else:
                        doc.status = "Fake"
                else:
                    doc.status = "Pending"

                doc.save()
                return redirect("student_docs", id=student.id)

    return render(request, "docs.html", {
        "student": student,
        "documents": documents,
        "add_form": add_form,
        "issue_form": issue_form,
    })




from django.contrib import messages
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == "POST":
        student.delete()
        messages.success(request, f"{student.name} has been deleted successfully.")
        return redirect("stats")  # redirect to your stats page
    return redirect("stats")

def verify_doc(request, doc_no):
    document = get_object_or_404(Document, doc_no=doc_no)

    # Check if issued_by matches a registered college
    if College.objects.filter(college_name=document.issued_by).exists():
        document.status = "Verified"
    else:
        document.status = "Fake"

    document.save()

    messages.success(request, f"Document {doc_no} status updated to {document.status}")

    # Redirect to that student's document list
    return redirect('student_docs', id=document.student.id)
