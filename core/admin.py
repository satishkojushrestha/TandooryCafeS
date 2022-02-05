from django.contrib import admin
from .models import User, Employee, Supplier, Ingredient
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Ingredient)