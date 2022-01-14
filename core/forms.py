from django import forms
from core.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=150)
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('email', 'password')

class EmployeeForm(forms.Form):
    name = forms.CharField(max_length=30, required=True)
    position = forms.CharField(max_length=30, required=True)
    age = forms.CharField(max_length=3, required=True)
    salary = forms.IntegerField()
