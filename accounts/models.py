from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=50, blank=True)
    pass