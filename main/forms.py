from django import forms
from .models import Subject, Teacher, Student, Class

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['user']

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['user', 'subject']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user', 'major']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        exclude = ['user', 'building']

        widgets = {
            'start_time': forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"]),
            'end_time': forms.DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])
        }

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)