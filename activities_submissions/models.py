from django.db import models
from django.contrib.auth.models import User


class Activity(models.Model):
    title = models.CharField(max_length=255, unique=True)
    point = models.IntegerField()

    submissions = models.ManyToManyField(User, related_name='activities', through='activities.Submission')


class Submission(models.Model):
    grape = models.IntegerField(null=True)
    repo = models.TextField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
