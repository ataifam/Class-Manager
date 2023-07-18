from django.shortcuts import render, redirect, get_object_or_404
from .forms import SubjectForm, ClassForm, StudentForm, TeacherForm
from .models import Subject, Class, Student, Teacher

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
