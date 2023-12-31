from django.shortcuts import render, redirect, get_object_or_404
from .forms import SchoolForm, SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm
from .models import School, Subject, Class, Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .gameFunctions import computeAvgSalary, computeAvgSkill, computeAvgGradeDist, computeFinancials

# Create your views here.

def home(request):
    user = get_object_or_404(User, id=request.user.id)
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    classes = Class.objects.filter(user_id=user.id)
    teachers = Teacher.objects.filter(user_id=user.id)
    students = Student.objects.filter(user_id=user.id)
    subjectForm = SubjectForm()

    # compute school financial information for menubar
    costs = computeFinancials(user, user_school)
    
    if request.method == 'POST':
            # if post request sent, store values in subject form
            subjectForm = SubjectForm(request.POST)
            if subjectForm.is_valid():
                subject = subjectForm.save(commit=False)
                # assign subject's user to current user
                subject.user = user
                subject.save()
                messages.success(request, "Building successfully created!")
                return redirect('main:home')
            messages.error(request, "An error has occured, please try again!")
            return redirect('main:home')

    return render(request, "main/home.html", {
        'school': user_school,
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'subjectForm': subjectForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def search(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)

    # school financial information for user's school
    costs = computeFinancials(user, user_school)

    # store user's get request query in q if valid
    q = request.GET.get('q') if bool(request.GET.get('q', False)) else None
    if q is not None:
            # find at most 15 possible queries matching some part of q
            subjects = Subject.objects.filter(user_id=user.id, name__icontains=q)[0:15]
            classes = Class.objects.filter(user_id=user.id, name__icontains=q)[0:15]
            # search both first and last names of teachers and students
            teachers = (Teacher.objects.filter(user_id=user.id, first_name__icontains=q) | Teacher.objects.filter(user_id=user.id, last_name__icontains=q))[0:15]
            students = (Student.objects.filter(user_id=user.id, first_name__icontains=q) | Student.objects.filter(user_id=user.id, last_name__icontains=q))[0:15]
    else:
        messages.error(request, "Invalid search entry. Please try again!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "main/search.html", {
        'school': user_school,
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def settings(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    schoolForm = SchoolForm(instance=user_school)

    # financial info for user's school
    costs = computeFinancials(user, user_school)

    if request.method == 'POST':
            # if post request used on this page, store values in school form
            schoolForm = SchoolForm(instance=user_school, data=request.POST)
            if schoolForm.is_valid:
                schoolForm.save()
                messages.success(request, "School successfully edited!")
                return redirect('main:home')
            messages.error(request, "An error has occured, please try again!")
            return redirect('main:home')

    return render(request, "main/settings.html", {
        'school': user_school,
        'schoolForm': schoolForm,
        'costs': costs,
    })

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        # store values from post request to login form
        form = LoginForm(request.POST)
        if form.is_valid():
            # get username and password values from login form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # attempt to authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                return redirect('main:settings')
            else:
                messages.error(request, 'Error logging in. Please try again.')
                return redirect('main:login_view')

    return render(request, "main/login.html", {
        'form': form,
    })

def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        # if post request used on this page store values in UCF
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # save before authenticating
            form.save()
            # get username and password values from login form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # authenticate
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('main:home')

    return render(request, "main/register.html", {
        'form': form,
    })

def logout_view(request):
    if request.user.is_authenticated:
        # logout user
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return redirect('main:login_view')


@login_required(login_url="main:login_view")
def delete(request, pk, option):
    user = request.user
    # delete path for all user's school objects; determine specific object to delete
    # by checking arguments
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
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    building = get_object_or_404(Subject, user=user.id, id=pk)
    classForm = ClassForm()

    # user's financial info for school
    costs = computeFinancials(user, user_school)

    if request.method == 'POST':
        # if post request used on this page, store values in class form
        classForm = ClassForm(request.POST)
        if classForm.is_valid():
                    schoolClass = classForm.save(commit=False)
                    # assign class' user to current user
                    schoolClass.user = user
                    # assign class' building to argument building
                    schoolClass.building = building
                    schoolClass.save()
                    messages.success(request, "Class creation successful!")

    return render(request, "main/building.html", {
        'school': user_school,
        'subject': building,
        'subjects': subjects,
        'form': classForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def class_view(request, name):
    user = get_object_or_404(User, id=request.user.id)
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    user_class = get_object_or_404(Class, user_id=user.id, name=name)
    students = Student.objects.filter(user_id=user.id)
    teacherForm = TeacherForm()
    studentForm = StudentForm()

    # user's financial info for school
    costs = computeFinancials(user, user_school)

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
        'school': user_school,
        'class': user_class,
        'students': students,
        'subjects': subjects,
        'teacherForm': teacherForm,
        'studentForm': studentForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def create_teacher(request, name):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    # creating teacher requires tokens
    if request.method == 'POST' and user_school.checkTokens() > 0 and user_school.money > 0:
       # if sufficient funds and post request sent, store values in teacher form
       teacherForm = TeacherForm(request.POST)
       if teacherForm.is_valid():
            teacher = teacherForm.save(commit=False)
            # assign teacher's user to current user
            teacher.user = user
            # if argument name is not new, the building is old, so query the building
            if name != 'new':
                user_class = get_object_or_404(Class, user_id=user.id, name=name)
                teacher.subject = user_class.building
            else:
                # if argument name is new, attempt to create new subject and assign
                subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
                if subject is None:
                    messages.error(request, "Subject cannot be blank!")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                subject, created = Subject.objects.get_or_create(user_id=user.id, name=subject)
                teacher.subject = subject
            teacher.save()
            # decrease token
            user_school.useToken()
            messages.success(request, "Teacher creation successful!")
    else:
        messages.error(request, "Insufficient amount of action tokens or funds! Advance Year to reset your tokens and cut costs to make money!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="main:login_view")
def all_teachers(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    teachers = Teacher.objects.filter(user_id=user.id)
    teacherForm = TeacherForm()

    # user's financial info for school
    costs = computeFinancials(user, user_school)

    # if get request used, access and assign 'filter' value if valid
    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    if filter is not None:
        # if subject exists, get the subject to filter the teachers on the page
        try:
            subject = Subject.objects.get(user_id=user.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_teachers')
        
        # filter teachers by the subject if input was valid
        teachers = Teacher.objects.filter(user_id=user.id, subject=subject)

    # continuously compute the average skill and salaries based on filter value
    avgSkill = computeAvgSkill(teachers)
    avgSalary = computeAvgSalary(teachers)
    
    return render(request, "main/all_teachers.html", {
        'school': user_school,
        'teachers': teachers,
        'subjects': subjects,
        'filter': filter,
        'avgSkill': avgSkill,
        'avgSalary': avgSalary,
        'form': teacherForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def teacher(request, pk):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    teacher = get_object_or_404(Teacher, user_id=user.id, id=pk)
    classes = Class.objects.filter(user_id=request.user.id, teacher=teacher)
    teacherForm = TeacherForm(instance=teacher)

    costs = computeFinancials(user, user_school)

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
        'school': user_school,
        'teacher': teacher,
        'classes': classes,
        'subjects': subjects,
        'form': teacherForm,
        'costs': costs
    })

@login_required(login_url="main:login_view")
def create_student(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    # creating student requires tokens
    if request.method == 'POST' and user_school.checkTokens() > 0 and user_school.money > 0:
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
            user_school.useToken()
            messages.success(request, "Student creation successful!")
    else:
        messages.error(request, "Insufficient amount of action tokens or funds! Advance Year to reset your tokens and cut costs to make money!")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="main:login_view")
def all_students(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    students = Student.objects.filter(user_id=user.id)
    studentForm = StudentForm()

    costs = computeFinancials(user, user_school)

    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    if filter is not None:
        try:
            major = Subject.objects.get(user_id=user.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_students')
        students = Student.objects.filter(user_id=user.id, major=major)

    gradeDist = computeAvgGradeDist(students)
    sorted_gradeDist = dict(sorted(gradeDist.items()))
    
    return render(request, "main/all_students.html", {
        'school': user_school,
        'students': students,
        'subjects': subjects,
        'filter': filter,
        'distribution': sorted_gradeDist, 
        'form': studentForm,
        'costs': costs,
    }) 

@login_required(login_url="main:login_view")
def student(request, pk):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    subjects = Subject.objects.filter(user_id=user.id)
    student = get_object_or_404(Student, user_id=user.id, id=pk)
    classes = Class.objects.filter(user_id=user.id)
    studentForm = StudentForm(instance=student)

    costs = computeFinancials(user, user_school)

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
        'school': user_school,
        'student': student,
        'classes': classes,
        'subjects': subjects,
        'form': studentForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def nextYear(request):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    teachers = Teacher.objects.filter(user_id=user.id)
    students = Student.objects.filter(user_id=user.id)

    user_school.advanceYear()
    for student in students:
        student.progressYear()

    user_school.payCosts(computeFinancials(user, user_school))
    
    messages.success(request, "Successfully advanced school year!")
    return redirect('main:home')

@login_required(login_url="main:login_view")
def train(request, pk):
    user = request.user
    user_school = get_object_or_404(School, user_id=user.id)
    teacher = get_object_or_404(Teacher, user_id=user.id, id=pk)
    # training teacher requires tokens
    if user_school.checkTokens() > 0:
        teacher.train()
        user_school.useToken()
        messages.success(request, "Teacher successfully trained!")
    else:
        messages.error(request, "No tokens left! Advance Year to reset your tokens!")
    return redirect(request.META.get('HTTP_REFERER', '/'))
