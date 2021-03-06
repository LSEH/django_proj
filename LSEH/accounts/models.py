from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender = models.BooleanField()
    nickname = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password_date = models.DateTimeField(auto_now_add=True)
    nickname_date = models.DateTimeField(auto_now_add=True)