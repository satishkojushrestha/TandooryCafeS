from django.shortcuts import render, redirect
from core.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from core.models import User


def base_view(request):
    return render(request, "base.html")

def logoutView(request):
    logout(request)
    return redirect("Login")


def loginView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            try:                
                user = User.objects.get(email=email)
                auth_user = authenticate(request, username=user.username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    return redirect("Base")
                else:
                    return render(request, "login.html", {
                        'message': 'Invalid Credential',
                        'froms': LoginForm(request.POST),
                    })
            except:
                return render(request, "login.html", {
                        'message': 'Invalid Username and Password',
                        'forms': LoginForm(request.POST),
                    })
            

    return render(request, "login.html", {"forms":LoginForm})