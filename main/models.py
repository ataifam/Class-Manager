from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=30, default="My New School")
    player_name = models.CharField(max_length=30, unique=True)

    #override save method to provide default for player name
    def setName(self, *args, **kwargs):
        self.player_name = self.user.username

@receiver(post_save, sender=User)
def NewSchool(sender, instance, created, **kwargs):
    if created:
        school = School(user=instance)
        school.setName()
        school.save()


class Subject(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return (
                f"{self.name}"
        )

class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    skill = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)
    salary = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(999999)], blank=True, null=True)

    def __str__(self):
        return (
                f"{self.first_name+' '+self.last_name}"
        )
    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    building = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    room = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], blank=True, null=True)
    teacher = models.ForeignKey(Teacher, related_name="taught_by", on_delete=models.DO_NOTHING, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="taken_by", blank=True)

    def __str__(self):
        return (
                f"{self.name}"
        )




