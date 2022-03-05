from django.contrib import admin
from .models import FoodIngBridge, FoodIngredient, User, Employee, Supplier, Ingredient, Food, Category, Order, OrderFood, Charges
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Supplier)
admin.site.register(Ingredient)
admin.site.register(Food)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderFood)
admin.site.register(Charges)
admin.site.register(FoodIngBridge)
admin.site.register(FoodIngredient)