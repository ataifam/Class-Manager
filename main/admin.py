from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import School, Subject, Class, Student, Teacher

admin.site.unregister(Group)

class UserProfile(admin.StackedInline):
    model = School

admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)