from django.db import models
from Accounts.models import Profile
# Create your models here.

class Grade(models.Model):
    school = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Classroom(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.title}:{self.grade}"
    
class Student(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    total_absence = models.PositiveIntegerField(default=0)
    monthly_absence = models.PositiveBigIntegerField(default=0)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    registered = models.BooleanField(null=True, blank=True, default=False)
    attending = models.BooleanField(null=True, blank=True, default=True)

    
    def __str__(self):
        return f"{self.name} : {self.classroom}"
    
class Report(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    monthly_absences = models.PositiveBigIntegerField()
