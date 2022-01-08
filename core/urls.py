from django.urls import path
from .views import *

urlpatterns = [
    path('base/', base_view, name="base"),
    path('login/', loginView, name="login"),
    path('logout/', logoutView, name="logout"),
    path('profile/', profile_view, name="profile"),
    path('profile/update/', update_profile, name="profileUpdate"),
]