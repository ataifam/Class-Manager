from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return (
                f"{self.name}"
        )

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    skill = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(999999)], blank=True, null=True)
    salary = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)

    def __str__(self):
        return (
                f"{self.first_name+' '+self.last_name}"
        )
    
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    major = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    year = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], blank=True, null=True)
    average_grade = models.CharField(max_length=1)

    def __str__(self):
        return (
                f"{self.first_name+' '+self.last_name}"
        )

class Class(models.Model):
    name = models.CharField(max_length=60)
    building = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    room = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], blank=True, null=True)
    time = models.DateTimeField()
    teacher = models.ForeignKey(Teacher, related_name="taught_by", on_delete=models.DO_NOTHING, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="taken_by", blank=True, null=True)

    def __str__(self):
        return (
                f"{self.name}"
        )




