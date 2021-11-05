from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    users = models.ManyToManyField(User, related_name='courses')


    def __str__(self):
        return self.name
