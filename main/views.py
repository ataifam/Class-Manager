from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm
from .models import Subject, Class, Student, Teacher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    subjectForm = SubjectForm
    classForm = ClassForm
    studentForm = StudentForm
    teacherForm = TeacherForm
    return render(request, "main/home.html", {
        'subjectForm': subjectForm,
        'classForm' : classForm,
        'studentForm': studentForm,
        'teacherForm': teacherForm
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
