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
    user = get_object_or_404(User, id=request.user.id)
    subjects = Subject.objects.filter(user_id=request.user.id)
    classes = Class.objects.filter(user_id=request.user.id)
    teachers = Teacher.objects.filter(user_id=request.user.id)
    students = Student.objects.filter(user_id=request.user.id)
    subjectForm = SubjectForm()
    
    if request.method == 'POST':
        subjectForm = SubjectForm(request.POST)
        if subjectForm.is_valid():
            subject = subjectForm.save(commit=False)
            subject.user = user
            subject.save()

    return render(request, "main/home.html", {
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'form': subjectForm,
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
def delete(request, pk, option):
    user = request.user
    if option == 'subject':
        subject = get_object_or_404(Subject, user_id=user.id, id=pk)
        subject.delete()
        messages.success(request, "Subject successfully deleted!")
    elif option == 'class':
        user_class = get_object_or_404(Class, user_id=user.id, id=pk)
        user_class.delete()
        messages.success(request, "Class successfully deleted!")
    elif option == 'teacher':
        teacher = get_object_or_404(Teacher, user_id=user.id, id=pk)
        teacher.delete()
        messages.success(request, "Teacher successfully deleted!")
    elif option == 'student':
        student = get_object_or_404(Student, user_id=user.id, id=pk)
        student.delete()
        messages.success(request, "Student successfully deleted!")
    return redirect('main:home')

@login_required(login_url="main:login_view")
def building(request, pk):
    user = get_object_or_404(User, id=request.user.id)
    building = get_object_or_404(Subject, user_id=request.user.id, id=pk)
    classes = Class.objects.filter(user_id=request.user.id, building=building)
    teachers = Teacher.objects.filter(user_id=request.user.id)
    students = Student.objects.filter(user_id=request.user.id)
    classForm = ClassForm()

    if request.method == 'POST':
        classForm = ClassForm(request.POST)
        if classForm.is_valid():
                    schoolClass = classForm.save(commit=False)
                    schoolClass.user = user
                    schoolClass.building = building
                    schoolClass.save()
                    messages.success(request, "Class creation successful!")

    return render(request, "main/building.html", {
        'subject': building,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'form': classForm,
    })

@login_required(login_url="main:login_view")
def class_view(request, name):
    user = get_object_or_404(User, id=request.user.id)
    user_class = get_object_or_404(Class, user_id=user.id, name=name)
    teachers = Teacher.objects.filter(user_id=user.id)
    subjects = Subject.objects.filter(user_id=request.user.id)
    students = Student.objects.filter(user_id=user.id)
    teacherForm = TeacherForm()
    studentForm = StudentForm()


    if request.method == 'POST':
        # register student for class button clicked
        if 'register' in request.POST:
            pk = request.POST.get('register', '')
            student = get_object_or_404(Student, user_id=request.user.id, id=pk)
            user_class.students.add(student)
            messages.success(request, 'Student registered successfully!')
        # deregister student for class button clicked
        elif 'unregister' in request.POST:
            pk = request.POST.get('unregister', '')
            student = get_object_or_404(Student, user_id=request.user.id, id=pk)
            user_class.students.remove(student)
            messages.success(request, 'Student unregistered successfully!')
        elif 'substitute' in request.POST:
            pk = request.POST.get('substitute', '')
            teacher = get_object_or_404(Teacher, user_id=request.user.id, id=pk)
            user_class.teacher = teacher
            user_class.save()
            messages.success(request, 'Teacher changed successfully!')
        elif 'teacher_form' in request.POST:
            teacherForm = TeacherForm(request.POST)
            if teacherForm.is_valid():
                teacher = teacherForm.save(commit=False)
                teacher.user = user
                teacher.subject = user_class.building
                teacher.save()
                messages.success(request, "Teacher creation successful!")
        elif 'student_form' in request.POST:
            studentForm = StudentForm(request.POST)
            if studentForm.is_valid():
                student = studentForm.save(commit=False)
                student.user = user
                # check for empty input
                major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
                if major is None:
                    messages.error(request, "Major cannot be blank!")
                    return redirect('main:create')
                subject, created = Subject.objects.get_or_create(user=user, name=major)
                student.major = subject
                student.save()
                messages.success(request, "Student creation successful!")

        return redirect('main:class', name)

    return render(request, "main/class.html", {
        'class': user_class,
        'teachers': teachers,
        'students': students,
        'subjects': subjects,
        'teacherForm': teacherForm,
        'studentForm': studentForm,
    })

@login_required(login_url="main:login_view")
def faculty(request, pk):
    teacher = get_object_or_404(Teacher, user_id=request.user.id, id=pk)
    classes = Class.objects.filter(user_id=request.user.id, teacher=teacher)
    subjects = Subject.objects.filter(user_id=request.user.id)
    teacherForm = TeacherForm(instance=teacher)
    if request.method == 'POST':
        teacherForm = TeacherForm(request.POST, instance=teacher)
        if teacherForm.is_valid:
            teacher = teacherForm.save(commit=False)
            subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
            if subject is None:
                messages.error(request, "Subject cannot be blank!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            teacher_subject, created = Subject.objects.get_or_create(user_id=request.user.id, name=subject)
            teacher.subject = teacher_subject
            teacher.save()
            messages.success(request, "Teacher creation successful!")


    return render(request, "main/faculty.html", {
        'teacher': teacher,
        'classes': classes,
        'subjects': subjects,
        'form': teacherForm
    })

def student(request, pk):
    student = get_object_or_404(Student, user_id=request.user.id, id=pk)
    classes = Class.objects.filter(user_id=request.user.id)
    subjects = Subject.objects.filter(user_id=request.user.id)
    studentForm = StudentForm(instance=student)
    if request.method == 'POST':
        studentForm = StudentForm(request.POST, instance=student)
        if studentForm.is_valid:
            student = studentForm.save(commit=False)
            major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
            if major is None:
                messages.error(request, "Major cannot be blank!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            subject, created = Subject.objects.get_or_create(user_id=request.user.id, name=major)
            student.major = subject
            student.save()
            messages.success(request, "Student modification successful!")


    return render(request, "main/student.html", {
        'student': student,
        'classes': classes,
        'subjects': subjects,
        'form': studentForm
    })
