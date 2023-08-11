from django import forms
from .models import School, Subject, Teacher, Student, Class

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = '__all__'
        exclude = ['user', 'year', 'actionTokens', 'money']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['user']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user', 'subject', 'salary']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'major', 'year', 'average_grade']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        exclude = ['user', 'building', 'students', 'teacher']

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)