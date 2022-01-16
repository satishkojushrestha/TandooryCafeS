from turtle import position
from django.shortcuts import render, redirect
from core.forms import EmployeeForm, LoginForm, SupplierForm
from django.contrib.auth import login, logout, authenticate
from core.models import Supplier, User, Employee
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import JsonResponse
from datetime import datetime


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

def employee_view(request):
    employeeForm = EmployeeForm()    
    return render(request, "pages/employee_detail.html", {
        'form': employeeForm,
        'employees': Employee.objects.all(),
    })

def supplier_view(request):
    supplierForm = SupplierForm()    
    return render(request, "pages/supplier_detail.html", {
        'form': supplierForm,
        'suppliers': Supplier.objects.all(),
    })


class CreateCrudUserEmployee(View):


    def get(self, request):
        name = request.GET.get('name', None)
        position = request.GET.get('position', None)
        age = request.GET.get('age', None)
        salary = request.GET.get('salary', None)

        new_employee = Employee(
            name = name,
            position = position,
            age = age,
            salary = salary
        )

        new_employee.save()

        user_data = {'id':new_employee.id,'name':new_employee.name,'position':new_employee.position,'age':new_employee.age,'start_date':new_employee.start_date.strftime("%b. %d, %Y"),'salary':new_employee.salary}

        data_user = {
            'user': user_data
        }

        return JsonResponse(data_user)


class UpdateCrudUserEmployee(View):

    def get(self, request):
        id = request.GET.get('id', None)
        name = request.GET.get('name', None)
        position = request.GET.get('position', None)
        age = request.GET.get('age', None)
        salary = request.GET.get('salary')
        user = Employee.objects.get(id=id)
        user.name = name
        user.position = position
        user.age = age
        user.salary = salary
        user.save()

        user_data = {'id':id, 'name':user.name,'position':user.position,'age':user.age,'salary':user.salary}

        data_user = {
            'user': user_data
        }

        return JsonResponse(data_user)

class DeleteCrudUserEmployee(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Employee.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class CreateCrudUserSupplier(View):


    def get(self, request):
        name = request.GET.get('name', None)
        address = request.GET.get('address', None)
        contact_number = request.GET.get('contact_number', None)

        new_supplier = Supplier(
            name = name,
            address = address,
            contact_number = contact_number,
        )

        new_supplier.save()

        user_data = {'id':new_supplier.id,'name':new_supplier.name,'address':new_supplier.address,'contact_number':new_supplier.contact_number}

        data_user = {
            'user': user_data
        }

        return JsonResponse(data_user)



class UpdateCrudUserSupplier(View):

    def get(self, request):
        id = request.GET.get('id', None)
        name = request.GET.get('name', None)
        address = request.GET.get('address', None)
        contact_number = request.GET.get('contact_number', None)

        user = Supplier.objects.get(id=id)
        user.name = name
        user.address = address
        user.contact_number = contact_number
        user.save()

        user_data = {'id':id, 'name':user.name,'address':user.address,'contact_number':user.contact_number}

        data_user = {
            'user': user_data
        }

        return JsonResponse(data_user)

class DeleteCrudUserSupplier(View):
    def  get(self, request):
        id1 = request.GET.get('id', None)
        Supplier.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)
