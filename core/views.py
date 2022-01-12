from django.shortcuts import render, redirect
from core.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from core.models import User
from django.contrib.auth.decorators import login_required, permission_required


@permission_required('can_add_user', login_url="/login/")
def base_view(request):
    return render(request, "base.html")

def logoutView(request):
    logout(request)
    return redirect("login")

def loginView(request):
    if request.user.is_authenticated:
        return redirect("base")

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
                    return redirect("base")
                else:
                    return render(request, "authentication/login.html", {
                        'message': 'Invalid Credential',
                        'froms': LoginForm(request.POST),
                    })
            except:
                return render(request, "authentication/login.html", {
                        'message': 'Invalid Username and Password',
                        'forms': LoginForm(request.POST),
                    })
    return render(request, "authentication/login.html", {"forms":LoginForm})

@permission_required('can_add_user', login_url="/login/")
def profile_view(request):
    return render(request,"profile.html")

@permission_required('can_add_user', login_url="/login/")
def update_profile(request):
    if request.method == "POST":
        print(request.POST)
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("email")
        address = request.POST.get("address")
        contact_number = request.POST.get("number")

        if first_name=="":
            first_name=request.user.first_name
        if last_name=="":
            last_name=request.user.last_name
        if email=="":
            email=request.user.email
        if address=="":
            address=request.user.address
        if contact_number=="":
            contact_number=request.user.contact_number
        
        user_ac = User.objects.get(username=request.user.username)
        user_ac.first_name=first_name
        user_ac.last_name=last_name
        user_ac.email=email
        user_ac.address=address
        user_ac.contact_number=contact_number
        user_ac.save()

        return redirect("profile")

    return render(request, "update_profile.html")

def employee_view(request):
    return render(request, "pages/employee_detail.html")

def supplier_view(request):
    return render(request, "pages/supplier_detail.html")