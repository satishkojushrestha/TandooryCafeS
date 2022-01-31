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
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'First Name'
        }), max_length=15, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Last Name'
        }), max_length=15, required=True)
    position = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Position'
        }), max_length=30, required=True)
    age = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Age'
        }), max_length=3, required=True)
    salary = forms.IntegerField(widget=forms.NumberInput(
        attrs={
        'class':'form-control',
        'placeholder':'Salary'
        }), max_value=500000)

class SupplierForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'First Name'
        }), max_length=15, required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Last Name'
        }), max_length=15, required=True)
    address = forms.CharField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Address'
        }), max_length=40, required=True)
    contact = forms.IntegerField(widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Contact Number'
        }), required=True)

