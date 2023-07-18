from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Subject, Class, Student, Teacher

admin.site.unregister(Group)

admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Teacher)