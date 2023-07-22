from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm
from .models import Subject, Class, Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    userID = request.user.id
    subjects = Subject.objects.filter(user_id=userID)
    classes = Class.objects.filter(user_id=userID)
    teachers = Teacher.objects.filter(user_id=userID)
    students = Student.objects.filter(user_id=userID)

    return render(request, "main/home.html", {
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
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
                return redirect('main:login_view')

    return render(request, "main/login.html", {
        'form': form,
    })

def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('main:home')

    return render(request, "main/register.html", {
        'form': form,
    })

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('main:login_view')

@login_required(login_url="main:login_view")
def create(request, pk):
    if pk != request.user.id:
        messages.error(request, "You cannot invade someone else's school!")
        redirect('main:home')
    user = get_object_or_404(User, id=pk)
    subjects = Subject.objects.all()
    subjectForm = SubjectForm
    classForm = ClassForm
    studentForm = StudentForm
    teacherForm = TeacherForm
    
    if request.method == 'POST':
        subjectForm = SubjectForm(request.POST)
        studentForm = StudentForm(request.POST)
        classForm = ClassForm(request.POST)
        teacherForm = TeacherForm(request.POST)
        if 'subject_form' in request.POST:
            if subjectForm.is_valid():
                subject = subjectForm.save(commit=False)
                subject.user = user
                subject.save()
        elif 'student_form' in request.POST:
            if studentForm.is_valid():
                student = studentForm.save(commit=False)
                student.user = user
                major = request.POST.get('major')
                subject, created = Subject.objects.get_or_create(user=user, name=major)
                student.major = subject
                student.save()
                messages.success(request, "Student creation successful!")
        elif 'class_form' in request.POST:
            if classForm.is_valid():
                schoolClass = classForm.save(commit=False)
                schoolClass.user = user
                building = request.POST.get('building')
                subject, created = Subject.objects.get_or_create(user=user, name=building)
                schoolClass.building = subject
                schoolClass.save()
                messages.success(request, "Class creation successful!")
        elif 'teacher_form' in request.POST:
            if teacherForm.is_valid():
                teacher = teacherForm.save(commit=False)
                teacher.user = user
                subject = request.POST.get('subject')
                teacher_subject, created = Subject.objects.get_or_create(user=user, name=subject)
                teacher.subject = teacher_subject
                teacher.save()
                print('p')
                messages.success(request, "Teacher creation successful!")
        return redirect('main:create', pk)
    return render(request, "main/create.html", {
        'subjectForm': subjectForm,
        'classForm': classForm,
        'studentForm': studentForm,
        'teacherForm': teacherForm,
        'subjects': subjects,
    })

@login_required(login_url="main:login_view")
def building(request, pk, subject):
    if pk != request.user.id:
        messages.error(request, "You cannot invade someone else's school!")
        redirect('main:home')
    user_subject = get_object_or_404(Subject, user_id=pk, name=subject)
    classes = Class.objects.filter(user_id=pk, building=user_subject)
    teachers = Teacher.objects.filter(user_id=pk)
    students = Student.objects.filter(user_id=pk)

    return render(request, "main/building.html", {
        'subject': user_subject,
        'classes': classes,
        'teachers': teachers,
        'students': students,
    })

@login_required(login_url="main:login_view")
def class_view(request, pk, name):
    if pk != request.user.id:
        messages.error(request, "You cannot invade someone else's school!")
        redirect('main:home')
    user_class = get_object_or_404(Class, user_id=pk, name=name)
    teachers = Teacher.objects.filter(user_id=pk)
    students = Student.objects.filter(user_id=pk)

    return render(request, "main/class.html", {
        'class': user_class,
        'teachers': teachers,
        'students': students,
    })
