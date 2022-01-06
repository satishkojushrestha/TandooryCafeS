from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view, name="Base"),
    path('login/', loginView, name="Login"),
    path('logout/', logoutView, name="Logout"),
]