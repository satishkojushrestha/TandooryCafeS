from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)