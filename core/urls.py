from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view, name="base"),
    path('', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile_view, name="profile"),
    path('profile/update/', update_profile, name="profileUpdate"),
    path('employee/', employee_view, name="employee"),
    path('supplier/', supplier_view, name="supplier"),
    path('ajax/crud/create/', CreateCrudUser.as_view(), name='crud_ajax_create'),
]