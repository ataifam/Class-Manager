from django.shortcuts import render, redirect, get_object_or_404
from .forms import SchoolForm, SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm
from .models import School, Subject, Class, Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .gameFunctions import computeAvgSalary, computeAvgSkill, computeAvgGradeDist

# Create your views here.

def home(request):
    user = get_object_or_404(User, id=request.user.id)
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    classes = Class.objects.filter(user_id=user.id)
    teachers = Teacher.objects.filter(user_id=user.id)
    students = Student.objects.filter(user_id=user.id)
    schoolForm = SchoolForm(instance=user_school)
    subjectForm = SubjectForm()
    
    if request.method == 'POST':
        if 'school_form' in request.POST:
            schoolForm = SchoolForm(instance=user_school, data=request.POST)
            if schoolForm.is_valid:
                schoolForm.save()
                messages.success(request, "School successfully edited!")
                redirect('main:home')
        elif 'subject_form' in request.POST:
            subjectForm = SubjectForm(request.POST)
            if subjectForm.is_valid():
                subject = subjectForm.save(commit=False)
                subject.user = user
                subject.save()
                messages.success(request, "Building successfully created!")
                redirect('main:home')
        messages.error(request, "An error has occured, please try again!")
        redirect('main:home')

    return render(request, "main/home.html", {
        'school': user_school,
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'schoolForm': schoolForm,
        'subjectForm': subjectForm,
    })

@login_required(login_url="main:login_view")
def search(request):
    user = request.user
    q = request.GET.get('q') if bool(request.GET.get('q', False)) else None
    if q is not None:
            subjects = Subject.objects.filter(user_id=user.id, name__icontains=q)[0:15]
            classes = Class.objects.filter(user_id=user.id, name__icontains=q)[0:15]
            teachers = (Teacher.objects.filter(user_id=user.id, first_name__icontains=q) | Teacher.objects.filter(user_id=user.id, last_name__icontains=q))[0:15]
            students = (Student.objects.filter(user_id=user.id, first_name__icontains=q) | Student.objects.filter(user_id=user.id, last_name__icontains=q))[0:15]
    else:
        messages.error(request, "Invalid search entry. Please try again!")

    return render(request, "main/search.html", {
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
            password = form.cleaned_data['password1']
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
        subject = get_object_or_404(Subject, id=pk)
        subject.delete()
        messages.success(request, "Subject successfully deleted!")
    elif option == 'class':
        user_class = get_object_or_404(Class, id=pk)
        user_class.delete()
        messages.success(request, "Class successfully deleted!")
    elif option == 'teacher':
        teacher = get_object_or_404(Teacher, id=pk)
        teacher.delete()
        messages.success(request, "Teacher successfully deleted!")
    elif option == 'student':
        student = get_object_or_404(Student, id=pk)
        student.delete()
        messages.success(request, "Student successfully deleted!")
    elif option == 'school':
        school = get_object_or_404(School, id=pk)
        school.name = "My New School"
        # everything will cascade by deleting all subjects
        Subject.objects.filter(user_id=user.id).delete()
    return redirect('main:home')

@login_required(login_url="main:login_view")
def building(request, pk):
    user = get_object_or_404(User, id=request.user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    building = get_object_or_404(Subject, user=user.id, id=pk)
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
        'subjects': subjects,
        'form': classForm,
    })

@login_required(login_url="main:login_view")
def class_view(request, name):
    user = get_object_or_404(User, id=request.user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    user_class = get_object_or_404(Class, user_id=user.id, name=name)
    students = Student.objects.filter(user_id=user.id)
    teacherForm = TeacherForm()
    studentForm = StudentForm()
    if request.method == 'POST':
        # register student for class button clicked
        if 'register' in request.POST:
            pk = request.POST.get('register', '')
            student = get_object_or_404(Student, user_id=user.id, id=pk)
            user_class.students.add(student)
            messages.success(request, 'Student registered successfully!')
        # deregister student for class button clicked
        elif 'unregister' in request.POST:
            pk = request.POST.get('unregister', '')
            student = get_object_or_404(Student, user_id=user.id, id=pk)
            user_class.students.remove(student)
            messages.success(request, 'Student unregistered successfully!')
        elif 'substitute' in request.POST:
            pk = request.POST.get('substitute', '')
            teacher = get_object_or_404(Teacher, user_id=user.id, id=pk)
            user_class.teacher = teacher
            user_class.save()
            messages.success(request, 'Teacher changed successfully!')
        return redirect('main:class', name)

    return render(request, "main/class.html", {
        'class': user_class,
        'students': students,
        'subjects': subjects,
        'teacherForm': teacherForm,
        'studentForm': studentForm,
    })

@login_required(login_url="main:login_view")
def create_teacher(request, name):
    user = request.user
    if request.method == 'POST':
       teacherForm = TeacherForm(request.POST)
       if teacherForm.is_valid():
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            if name is not None:
                user_class = get_object_or_404(Class, user_id=user.id, name=name)
                teacher.subject = user_class.building
            else:
                subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
                if subject is None:
                    messages.error(request, "Subject cannot be blank!")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                subject, created = Subject.objects.get_or_create(user_id=user.id, name=subject)
                teacher.subject = subject
            teacher.save()
            messages.success(request, "Teacher creation successful!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="main:login_view")
def all_teachers(request):
    user = request.user
    subjects = Subject.objects.filter(user_id=user.id)
    teachers = Teacher.objects.filter(user_id=user.id)
    teacherForm = TeacherForm()
    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    if filter is not None:
        try:
            subject = Subject.objects.get(user_id=user.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_teachers')
        teachers = Teacher.objects.filter(user_id=user.id, subject=subject)

    avgSkill = computeAvgSkill(teachers)
    avgSalary = computeAvgSalary(teachers)
    
    return render(request, "main/all_teachers.html", {
        'teachers': teachers,
        'subjects': subjects,
        'filter': filter,
        'avgSkill': avgSkill,
        'avgSalary': avgSalary,
        'form': teacherForm
    })

@login_required(login_url="main:login_view")
def teacher(request, pk):
    user = request.user
    subjects = Subject.objects.filter(user_id=user.id)
    teacher = get_object_or_404(Teacher, user_id=user.id, id=pk)
    classes = Class.objects.filter(user_id=request.user.id, teacher=teacher)
    teacherForm = TeacherForm(instance=teacher)
    if request.method == 'POST':
        teacherForm = TeacherForm(request.POST, instance=teacher)
        if teacherForm.is_valid():
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
            if subject is None:
                messages.error(request, "Subject cannot be blank!")
                return redirect('main:teacher', pk)
            subject, created = Subject.objects.get_or_create(user_id=user.id, name=subject)
            teacher.subject = subject
            teacher.save()
            messages.success(request, "Teacher creation successful!")
        return redirect('main:teacher', pk)


    return render(request, "main/teacher.html", {
        'teacher': teacher,
        'classes': classes,
        'subjects': subjects,
        'form': teacherForm
    })

@login_required(login_url="main:login_view")
def create_student(request):
    user = request.user
    if request.method == 'POST':
        studentForm = StudentForm(request.POST)
        if studentForm.is_valid():
            student = studentForm.save(commit=False)
            student.user = user
            # check for empty input
            major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
            if major is None:
                messages.error(request, "Major cannot be blank!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            subject, created = Subject.objects.get_or_create(user=user, name=major)
            student.major = subject
            student.save()
            messages.success(request, "Student creation successful!")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="main:login_view")
def all_students(request):
    user = request.user
    subjects = Subject.objects.filter(user_id=user.id)
    students = Student.objects.filter(user_id=user.id)
    studentForm = StudentForm()
    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    if filter is not None:
        try:
            major = Subject.objects.get(user_id=user.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_students')
        students = Student.objects.filter(user_id=user.id, major=major)

    gradeDist = computeAvgGradeDist(students)
    
    return render(request, "main/all_students.html", {
        'students': students,
        'subjects': subjects,
        'filter': filter,
        'distribution': gradeDist, 
        'form': studentForm
    }) 

@login_required(login_url="main:login_view")
def student(request, pk):
    user = request.user
    subjects = Subject.objects.filter(user_id=user.id)
    student = get_object_or_404(Student, user_id=user.id, id=pk)
    classes = Class.objects.filter(user_id=user.id)
    studentForm = StudentForm(instance=student)
    if request.method == 'POST':
        studentForm = StudentForm(request.POST, instance=student)
        if studentForm.is_valid:
            student = studentForm.save(commit=False)
            major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
            if major is None:
                messages.error(request, "Major cannot be blank!")
                return redirect('main:student', pk)
            subject, created = Subject.objects.get_or_create(user_id=user.id, name=major)
            student.major = subject
            student.save()
            messages.success(request, "Student modification successful!")
        return redirect('main:student', pk)


    return render(request, "main/student.html", {
        'student': student,
        'classes': classes,
        'subjects': subjects,
        'form': studentForm
    })

@login_required(login_url="main:login_view")
def nextYear(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    students = Student.objects.all()

    user_school.advanceYear()
    for student in students:
        student.progressYear()
    
    messages.success(request, "Successfully advanced to school year!")
    return redirect(request.META.get('HTTP_REFERER', '/'))
