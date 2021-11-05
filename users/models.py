from django.db import models
from django.contrib.auth.models import AbstractUser
# from rest_framework.permissions import BasePermission


# class User(AbstractUser):
#     is_staff = models.BooleanField()
#     is_superuser = models.BooleanField()


# class Instructor(BasePermission):
#     def allowed(self, request):
#         if request.method == 'GET':
#             return True
#         return request.user.is_superuser


# class Facilitator(BasePermission):
#     def allowed(self, request):
#         if request.method == 'GET':
#             return True
#         return request.user.is_staff
