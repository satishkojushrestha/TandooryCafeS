from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view, name="base"),
    path('', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile_view, name="profile"),
    path('profile/update/', update_profile, name="profileUpdate"),
    path('employee/', employee_view, name="employee"),
    path('employee/new/', add_employee_view, name="add_employee"),
    path('employee/edit/<int:id>/', edit_employee_view, name="edit_employee"),
    path('supplier/', supplier_view, name="supplier"),
    path('supplier/new/', add_supplier_view, name="add_supplier"),
    path('supplier/edit/<int:id>', edit_supplier_view, name="edit_supplier"),
    path('ajax/crud/delete/', DeleteCrudUserEmployee.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/delete/supplier/', DeleteCrudUserSupplier.as_view(), name='crud_ajax_delete_supplier'),
    path('addingredient/', add_ingredient_view, name="add_ingredient"),
    path('ingredient/', ingredient_view, name="ingredient"),
    path('ajax/crud/delete/ingredient/', DeleteCrudIngredient.as_view(), name='crud_ajax_delete_ingredient'),
    path('ingredient/edit/<int:id>', edit_ingredient_view, name="edit_ingredient"),
    path('addfood/', add_food_view, name="add_food"),
]