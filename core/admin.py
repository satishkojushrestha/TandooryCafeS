from django.contrib import admin
from .models import User, Employee, Supplier, Ingredient, Food, Category
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Food)
admin.site.register(Category)