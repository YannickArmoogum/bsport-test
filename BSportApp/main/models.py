from django.db import models
from django.utils import timezone
import datetime
import json
# Create your models here.

class User(models.Model):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    dateJoined = models.DateTimeField(default=timezone.now )
    telephone = models.CharField(max_length=12)

    def __str__(self):
        obj = {"id":self.id,"name":self.firstName}
        response = json.dumps(obj)
        return response

class Appointment(models.Model):
    user_FK = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='appointments')
    date = models.DateField(default=datetime.date.today)
    description = models.CharField(max_length=140)
