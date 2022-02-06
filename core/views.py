from django.shortcuts import render, redirect
from core.forms import EmployeeForm, IngredientForm, LoginForm, SupplierForm
from django.contrib.auth import login, logout, authenticate
from core.models import Supplier, User, Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponse, JsonResponse


@login_required(login_url="/")
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

@login_required(login_url="/")
def profile_view(request):
    return render(request,"profile.html")

# @permission_required('can_add_user', login_url="/")
@login_required(login_url="/")
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

@login_required(login_url="/")
def employee_view(request):    
    return render(request, "pages/employee_detail.html", {
        'employees': Employee.objects.all(),
    })

@login_required(login_url="/")
def add_employee_view(request):
    if request.method == "POST":
        employeeForm = EmployeeForm(request.POST)
        if employeeForm.is_valid():
            first_name = employeeForm.cleaned_data.get("first_name")
            last_name = employeeForm.cleaned_data.get("last_name")
            position = employeeForm.cleaned_data.get("position")
            age = employeeForm.cleaned_data.get("age")
            salary = employeeForm.cleaned_data.get("salary")
            new_employee = Employee(
                first_name = first_name,
                last_name = last_name,
                position = position,
                age = age,
                salary = salary
            )     
            new_employee.save()
            return redirect("add_employee") 
     
    return render(request, "pages/add_employee.html", {
        'form': EmployeeForm(),
    })

@login_required(login_url="/")
def edit_employee_view(request, id):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        position = request.POST.get("position")
        age = request.POST.get("age")
        salary = request.POST.get("salary")
        try:
            update_employee = Employee.objects.get(id=id)
            if first_name:
                update_employee.first_name = first_name
            if last_name:
                update_employee.last_name = last_name
            if position:
                update_employee.position = position
            if age:
                update_employee.age = age
            if salary:
                update_employee.salary = salary
            update_employee.save()
            return redirect("employee")
        except:
            return HttpResponse(status=404)
    try:
        get_employee = Employee.objects.get(id=id)   
        return render(request, "pages/edit_employee.html", {
            'form': EmployeeForm(),
            'edit_user': get_employee,
        })  
    except:
        return HttpResponse(status=404)
   
@login_required(login_url="/")
def supplier_view(request):  
    return render(request, "pages/supplier_detail.html", {
        'suppliers': Supplier.objects.all(),
    })


@login_required(login_url="/")
def add_ingredient_view(request):  
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return render(request, "pages/add_ingredient.html", {
                "form":form
            })
        return redirect("add_ingredient")

    return render(request, "pages/add_ingredient.html", {
        "form":IngredientForm
    })

@login_required(login_url="/")
def add_supplier_view(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            address = form.cleaned_data.get("address")
            contact = form.cleaned_data.get("contact")
            new_supplier = Supplier(
                first_name = first_name,
                last_name = last_name,
                address = address,
                contact_number = contact,
            )     
            new_supplier.save()
            return redirect("add_supplier")
        else:
            return render(request,"pages/add_supplier.html",{
                "form":form
            })     
    return render(request, "pages/add_supplier.html",{
        "form":SupplierForm()
    })

@login_required(login_url="/")
def edit_supplier_view(request, id):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        contact = request.POST.get("contact")
        print(request.POST)
        try:
            update_supplier = Supplier.objects.get(id=id)
            if first_name:
                update_supplier.first_name = first_name
            if last_name:
                update_supplier.last_name = last_name
            if address:
                update_supplier.address = address
            if contact:
                update_supplier.contact_number = contact
            update_supplier.save()
            return redirect("supplier")
        except:
            return HttpResponse(status=404)
    try:
        get_supplier = Supplier.objects.get(id=id)   
        return render(request, "pages/edit_supplier.html", {
            'form': SupplierForm(),
            'edit_user': get_supplier,
        })  
    except:
        return HttpResponse(status=404)


class DeleteCrudUserEmployee(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Employee.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class DeleteCrudUserSupplier(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Supplier.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


def ingredient_view(request):
    return render(request, )