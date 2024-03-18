from django import forms
from .models import School, Subject, Teacher, Student, Class
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):

        class Meta:
                model = School
                fields = ['username', 'password1', 'password2', 'name', 'tuition']
                widgets = {
                    "sent_to" : forms.TextInput(attrs={'class':'form-control', 'placeholder':""}),
                }

                def __init__(self,*args,**kwargs):
                        super().__init__(*args,**kwargs)
                        for field in self.fields:
                                self.fields[field].widget.attrs.update({'class':'form-control','placeholder':self.fields[field].label})

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        exclude = ['school']

class TeacherForm(forms.ModelForm):
    
    class Meta:
        model = Teacher
        fields = '__all__'
        exclude = ['subject', 'salary', 'school']
        widgets = {'skill': forms.Select(attrs={'class': "skill_toggler"}, choices=Teacher.SKILL)}

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['school', 'major', 'year', 'average_grade']

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        exclude = ['school', 'building', 'students', 'teacher']

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)