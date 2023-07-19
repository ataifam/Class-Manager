from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm
from .models import Subject, Class, Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):

    return render(request, "main/home.html", {
        
    })

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('main:home')
            else:
                messages.error(request, 'Error logging in. Please try again.')
                return redirect('social:login')

    return render(request, "main/login.html", {
        'form': form,
    })

def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()


    return render(request, "main/register.html", {
        'form': form,
    })

def create(request, pk):
    user = get_object_or_404(User, id=pk)
    subjectForm = SubjectForm
    classForm = ClassForm
    studentForm = StudentForm
    teacherForm = TeacherForm
    
    if request.method == 'POST':
        subjectForm = SubjectForm(request.POST)
        classForm = ClassForm(request.POST)
        studentForm = StudentForm(request.POST)
        teacherForm = TeacherForm(request.POST)
        if 'subject' in request.POST:
            if subjectForm.is_valid():
                subject = subjectForm.save(commit=False)
                subject.user = user
                subject.save()
        elif 'student' in request.POST:
            if studentForm.is_valid():
                student = studentForm.save(commit=False)
                student.user = user
                student.save()
        elif 'class' in request.POST:
            if classForm.is_valid():
                schoolClass = classForm.save(commit=False)
                schoolClass.user = user
                schoolClass.save()
        elif 'teacher' in request.POST:
            if teacherForm.is_valid():
                teacher = teacherForm.save(commit=False)
                teacher.user = user
                teacher.save()


    return render(request, "main/create.html", {
        'subjectForm': subjectForm,
        'classForm': classForm,
        'studentForm': studentForm,
        'teacherForm': teacherForm,
    })
