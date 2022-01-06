from django import forms
from core.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=250)
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    class Meta:
        model = User
        fields = ('email', 'password')