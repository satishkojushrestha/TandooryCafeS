from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view, name="Base"),
]