from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    start_date = models.DateField(auto_now_add=True)
    salary = models.IntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supplier(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Ingredient(models.Model):
    name = models.CharField(max_length=20, unique=True)
    unit = models.CharField(max_length=20)
    price_per_unit = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT)    
    time_stamp = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name