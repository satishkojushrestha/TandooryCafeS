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
    path('supplier/', supplier_view, name="supplier"),
    path('ajax/crud/create/', CreateCrudUserEmployee.as_view(), name='crud_ajax_create'),
    path('ajax/crud/update/', UpdateCrudUserEmployee.as_view(), name='crud_ajax_update'),
    path('ajax/crud/delete/', DeleteCrudUserEmployee.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/create/supplier', CreateCrudUserSupplier.as_view(), name='crud_ajax_create_supplier'),
    path('ajax/crud/update/supplier', UpdateCrudUserSupplier.as_view(), name='crud_ajax_update_supplier'),
    path('ajax/crud/delete/supplier', DeleteCrudUserSupplier.as_view(), name='crud_ajax_delete_supplier'),

]