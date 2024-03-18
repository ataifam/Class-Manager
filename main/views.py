from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, ClassForm, StudentForm, TeacherForm, LoginForm, SignUpForm
from .models import School, Subject, Class, Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .gameFunctions import computeAvgSalary, computeAvgSkill, computeAvgGradeDist, computeFinancials

# Create your views here.

def home(request):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    classes = Class.objects.filter(school_id=school.id)
    teachers = Teacher.objects.filter(school_id=school.id)
    students = Student.objects.filter(school_id=school.id)
    subjectForm = SubjectForm()

    # compute school financial information for menubar
    costs = computeFinancials(school)
    
    if request.method == 'POST':
            # if post request sent, store values in subject form
            subjectForm = SubjectForm(request.POST)
            if subjectForm.is_valid():
                subject = subjectForm.save(commit=False)
                # assign subject's user to current user
                subject.school = school
                subject.save()
                messages.success(request, "Building successfully created!")
                return redirect('main:home')
            messages.error(request, "An error has occured, please try again!")
            return redirect('main:home')

    return render(request, "main/home.html", {
        'school': school,
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'subjectForm': subjectForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def search(request):
    school = get_object_or_404(School, id=request.user.id)

    # school financial information for user's school
    costs = computeFinancials(school)

    # store user's get request query in q if valid
    q = request.GET.get('q') if bool(request.GET.get('q', False)) else None
    if q is not None:
            # find at most 15 possible queries matching some part of q
            subjects = Subject.objects.filter(school_id=school.id, name__icontains=q)[0:15]
            classes = Class.objects.filter(school_id=school.id, name__icontains=q)[0:15]
            # search both first and last names of teachers and students
            teachers = (Teacher.objects.filter(school_id=school.id, first_name__icontains=q) | Teacher.objects.filter(school_id=school.id, last_name__icontains=q))[0:15]
            students = (Student.objects.filter(school_id=school.id, first_name__icontains=q) | Student.objects.filter(school_id=school.id, last_name__icontains=q))[0:15]
    else:
        messages.error(request, "Invalid search entry. Please try again!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    return render(request, "main/search.html", {
        'school': school,
        'subjects': subjects,
        'classes': classes,
        'teachers': teachers,
        'students': students,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def settings(request):
    school = get_object_or_404(School, id=request.user.id)
    schoolForm = SignUpForm(instance=school)

    # financial info for user's school
    costs = computeFinancials(school)

    if request.method == 'POST':
            # if post request used on this page, store values in school form
            schoolForm = SignUpForm(instance=school, data=request.POST)
            if schoolForm.is_valid:
                schoolForm.save()
                messages.success(request, "School successfully edited!")
                return redirect('main:home')
            messages.error(request, "An error has occured, please try again!")
            return redirect('main:settings')

    return render(request, "main/settings.html", {
        'school': school,
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
    form = SignUpForm()

    if request.method == 'POST':
        # if post request used on this page store values in UCF
        form = SignUpForm(request.POST)
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
            return redirect('main:settings')

    return render(request, "main/register.html", {
        'form': form,
    })

def logout_view(request):
    if request.user.is_authenticated:
        # logout user
        logout(request)
        messages.success(request, 'Logged out successfully.')
        return school_id('main:login_view')


@login_required(login_url="main:login_view")
def delete(request, pk, option):
    school = get_object_or_404(School, id=request.user.id)
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
        school.startOver()
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="main:login_view")
def building(request, pk):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    building = get_object_or_404(Subject, school_id=school.id, id=pk)
    classForm = ClassForm()

    # user's financial info for school
    costs = computeFinancials(school)

    if request.method == 'POST':
        # if post request used on this page, store values in class form
        classForm = ClassForm(request.POST)
        if classForm.is_valid():
                    newClass = classForm.save(commit=False)
                    # assign class' user to current user
                    newClass.school = school
                    # assign class' building to argument building
                    newClass.building = building
                    newClass.save()
                    messages.success(request, "Class creation successful!")

    return render(request, "main/building.html", {
        'school': school,
        'subject': building,
        'subjects': subjects,
        'form': classForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def class_view(request, name):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    user_class = get_object_or_404(Class, school_id=school.id, name=name)
    students = Student.objects.filter(school_id=school.id)
    teacherForm = TeacherForm()
    studentForm = StudentForm()

    # user's financial info for school
    costs = computeFinancials(school)

    if request.method == 'POST':
        # register student for class button clicked
        if 'register' in request.POST:
            pk = request.POST.get('register', '')
            student = get_object_or_404(Student, school_id=school.id, id=pk)
            user_class.students.add(student)
            messages.success(request, 'Student registered successfully!')
        # deregister student for class button clicked
        elif 'unregister' in request.POST:
            pk = request.POST.get('unregister', '')
            student = get_object_or_404(Student, school_id=school.id, id=pk)
            user_class.students.remove(student)
            messages.success(request, 'Student unregistered successfully!')
        elif 'substitute' in request.POST:
            pk = request.POST.get('substitute', '')
            teacher = get_object_or_404(Teacher, school_id=school.id, id=pk)
            user_class.teacher = teacher
            user_class.save()
            messages.success(request, 'Teacher changed successfully!')
        return redirect('main:class', name)

    return render(request, "main/class.html", {
        'school': school,
        'class': user_class,
        'students': students,
        'subjects': subjects,
        'teacherForm': teacherForm,
        'studentForm': studentForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def create_teacher(request, name):
    school = get_object_or_404(School, id=request.user.id)
    # creating teacher requires tokens
    if request.method == 'POST' and school.canCreate():
       # if sufficient funds and post request sent, store values in teacher form
       teacherForm = TeacherForm(request.POST)
       if teacherForm.is_valid():
            teacher = teacherForm.save(commit=False)
            # assign teacher's user to current user
            teacher.school = school
            # if argument name is not new, the building is old, so query the building
            if name != 'new':
                existingClass = get_object_or_404(Class, school_id=school.id, name=name)
                teacher.subject = existingClass.building
            else:
                # if argument name is new, attempt to create new subject and assign
                subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
                if subject is None:
                    messages.error(request, "Subject cannot be blank!")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                subject, created = Subject.objects.get_or_create(school_id=school.id, name=subject)
                teacher.subject = subject
            teacher.save()
            # decrease token
            school.useToken()
            messages.success(request, "Teacher creation successful!")
    else:
        messages.error(request, "Insufficient amount of action tokens or funds! Advance Year to reset your tokens and cut costs to make money!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="main:login_view")
def all_teachers(request):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    teachers = Teacher.objects.filter(school_id=school.id)
    teacherForm = TeacherForm()

    # user's financial info for school
    costs = computeFinancials(school)

    # if get request used, access and assign 'filter' value if valid
    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    if filter is not None:
        # if subject exists, get the subject to filter the teachers on the page
        try:
            subject = Subject.objects.get(school_id=school.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_teachers')
        
        # filter teachers by the subject if input was valid
        teachers = Teacher.objects.filter(school_id=school.id, subject=subject)

    # continuously compute the average skill and salaries based on filter value
    avgSkill = computeAvgSkill(teachers)
    avgSalary = computeAvgSalary(teachers)
    
    return render(request, "main/all_teachers.html", {
        'school': school,
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
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    teacher = get_object_or_404(Teacher, school_id=school.id, id=pk)
    classes = Class.objects.filter(school_id=school.id, teacher=teacher)
    teacherForm = TeacherForm(instance=teacher)

    # user's financial info for school
    costs = computeFinancials(school)

    if request.method == 'POST':
        # if post request sent on this page, store values into the teacher form
        # with the instance corresponding to the specific teacher
        teacherForm = TeacherForm(request.POST, instance=teacher)
        if teacherForm.is_valid():
            teacher = teacherForm.save(commit=False)
            # set teacher's creator to current user
            teacher.school = school
            # get value from input field and make it a subject if not found
            subject = request.POST.get('subject') if bool(request.POST.get('subject', False)) else None
            if subject is None:
                # if error occurs, redirect back to teacher
                messages.error(request, "Subject cannot be blank!")
                return redirect('main:teacher', pk)
            subject, created = Subject.objects.get_or_create(school_id=school.id, name=subject)
            # assign teacher's subject to subject val
            teacher.subject = subject
            teacher.save()
            messages.success(request, "Teacher creation successful!")
        return redirect('main:teacher', pk)


    return render(request, "main/teacher.html", {
        'school': school,
        'teacher': teacher,
        'classes': classes,
        'subjects': subjects,
        'form': teacherForm,
        'costs': costs
    })

@login_required(login_url="main:login_view")
def create_student(request):
    school = get_object_or_404(School, id=request.user.id)
    # creating student requires tokens
    if request.method == 'POST' and school.canCreate():
        studentForm = StudentForm(request.POST)
        if studentForm.is_valid():
            student = studentForm.save(commit=False)
            student.school = school
            # check for empty input
            major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
            if major is None:
                messages.error(request, "Major cannot be blank!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            subject, created = Subject.objects.get_or_create(school_id=school.id, name=major)
            student.major = subject
            student.save()
            # spend a token
            school.useToken()
            messages.success(request, "Student creation successful!")
    else:
        messages.error(request, "Insufficient amount of action tokens or funds! Advance Year to reset your tokens and cut costs to make money!")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url="main:login_view")
def all_students(request):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    students = Student.objects.filter(school_id=school.id)
    studentForm = StudentForm()

    # user's financial info for school
    costs = computeFinancials(school)

    # if dropdown filtering functionality used, get the query value and
    # filter student major by it
    filter = request.GET.get('filter') if bool(request.GET.get('filter', False)) else None
    # if subject exists, filter by it; otherwise return error and abort
    if filter is not None:
        try:
            major = Subject.objects.get(school_id=school.id, name=filter)
        except Subject.DoesNotExist:
            messages.error(request, "Subject cannot be blank!")
            return redirect('main:all_students')
        # update students val
        students = Student.objects.filter(school_id=school.id, major=major)

    # recompute the grade distribution for students who are majoring
    # in that subject
    gradeDist = computeAvgGradeDist(students)
    sorted_gradeDist = dict(sorted(gradeDist.items()))
    
    return render(request, "main/all_students.html", {
        'school': school,
        'students': students,
        'subjects': subjects,
        'filter': filter,
        'distribution': sorted_gradeDist, 
        'form': studentForm,
        'costs': costs,
    }) 

@login_required(login_url="main:login_view")
def student(request, pk):
    school = get_object_or_404(School, id=request.user.id)
    subjects = Subject.objects.filter(school_id=school.id)
    student = get_object_or_404(Student, school_id=school.id, id=pk)
    classes = Class.objects.filter(school_id=school.id)
    studentForm = StudentForm(instance=student)

    # user's financial info for school
    costs = computeFinancials(school)

    if request.method == 'POST':
        # if post request used on this page, store values into the student
        # form in the specific student's form
        studentForm = StudentForm(request.POST, instance=student)
        if studentForm.is_valid:
            student = studentForm.save(commit=False)
            # attempt to get major from subject input field
            major = request.POST.get('major') if bool(request.POST.get('major', False)) else None
            if major is None:
                messages.error(request, "Major cannot be blank!")
                return redirect('main:student', pk)
            # if subject exists, use that subject for student's major; otherwise,
            # create the new subject
            subject, created = Subject.objects.get_or_create(school_id=school.id, name=major)
            student.major = subject
            student.save()
            messages.success(request, "Student modification successful!")
        return redirect('main:student', pk)


    return render(request, "main/student.html", {
        'school': school,
        'student': student,
        'classes': classes,
        'subjects': subjects,
        'form': studentForm,
        'costs': costs,
    })

@login_required(login_url="main:login_view")
def nextYear(request):
    school = get_object_or_404(School, id=request.user.id)
    teachers = Teacher.objects.filter(school_id=school.id)
    students = Student.objects.filter(school_id=school.id)
    classes = Class.objects.filter(school_id=school.id)

    school.advanceYear(computeFinancials(school))

    for currClass in classes:
        teacher = currClass.teacher
        if teacher is not None:
            for student in currClass.students.all():
                student.changeGrade(teacher.skill)
    for student in students:
        student.progressYear()
    
    messages.success(request, "Successfully advanced school year!")
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url="main:login_view")
def train(request, pk):
    school = get_object_or_404(School, id=school.id)
    teacher = get_object_or_404(Teacher, school_id=school.id, id=pk)
    # training teacher requires tokens
    if school.checkTokens() > 0:
        teacher.train()
        school.useToken()
        messages.success(request, "Teacher successfully trained!")
    else:
        messages.error(request, "No tokens left! Advance Year to reset your tokens!")
    return redirect(request.META.get('HTTP_REFERER', '/'))
