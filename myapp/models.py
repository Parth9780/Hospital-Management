from django.db import models

# Create your models here.
class Register(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.BigIntegerField()

class Appointment(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    department = models.CharField(max_length=35)
    message = models.TextField()

class contact(models.Model):
    name = models.CharField(max_length=35)
    email = models.EmailField()
    message = models.TextField()
