from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class School(AbstractUser):
    name = models.CharField(max_length=30, default="My New School")
    year = models.IntegerField(default=1)
    actionTokens = models.IntegerField(default=3)
    money = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000000000)], blank=True, null=True, default=500000)
    tuition = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100000)], blank=True, null=True, default=50000)

    def advanceYear(self, costs):
        self.year+=1
        # reset user action tokens every year
        self.actionTokens = 3
        self.payCosts(costs)
        self.save()

    def payCosts(self, cost):
        self.money+=cost
        self.save()

    def checkTokens(self):
        return self.actionTokens
    
    def useToken(self):
        self.actionTokens-=1
        self.save()
    
    def startOver(self):
        self.name = "My New School"
        self.year = 1
        self.money = 500000
        self.tuiton = 50000
        Subject.objects.filter(school_id=self.id).delete()
        self.save()

    # creating requires > 0 tokens and > 0 current funds
    def canCreate(self):
        return self.actionTokens > 0 and self.money > 0


class Subject(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return (
                f"{self.name}"
        )

class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    salary = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(999999)], blank=True, null=True)

    SKILL = [
        (1, 'Lecturer'),
        (2, 'Senior Lecturer'),
        (3, 'Assistant Professor'),
        (4, 'Associate Professor'),
        (5, 'Professor'),
    ]

    skill = models.IntegerField(choices=SKILL, default=1, blank=False, null=True)

    def __str__(self):
        return (
                f"{self.first_name+' '+self.last_name}"
        )
    
    def train(self):
        if self.skill == 5:
            return
        self.skill+=1
        self.updateSalary()
        self.save()
    
    def updateSalary(self):
        if self.skill == 1:
            self.salary = 30000
        elif self.skill == 2:
            self.salary = 40000
        elif self.skill == 3:
            self.salary = 60000
        elif self.skill == 4:
            self.salary = 80000
        else:
            self.salary = 100000

# when a new teacher is created update their salary
@receiver(post_save, sender=Teacher)
def NewTeacher(sender, instance, created, **kwargs):
    if created:
        teacher = instance
        teacher.updateSalary()
        teacher.save()
    
class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    major = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    year = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(4)], blank=True, null=True, default=1)
    average_grade = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], default='70')

    def __str__(self):
        return (
                f"{self.first_name+' '+self.last_name}"
        )
    
    def progressYear(self):
        if self.year == 4:
            self.delete()
        else:
            self.year+=1
            self.save()
    
    def getYear(self):
        if self.year == 1:
            return 'Freshman'
        elif self.year == 2:
            return 'Sophomore'
        elif self.year == 3:
            return 'Junior'
        else:
            return 'Senior'
    
    def getLetterGrade(self):
        if self.average_grade >= 90:
            return 'A'
        elif self.average_grade >= 80:
            return 'B'
        elif self.average_grade >= 70:
            return 'C'
        elif self.average_grade >= 60:
            return 'D'
        else:
            return 'F'
    
    def changeGrade(self, factor):
        self.average_grade+=(1.50*factor)
        self.save()

class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=60, unique=True)
    building = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    room = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)], blank=False, null=True)
    teacher = models.ForeignKey(Teacher, related_name="taught_by", on_delete=models.SET_NULL, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="taken_by", blank=True)

    def __str__(self):
        return (
                f"{self.name}"
        )




