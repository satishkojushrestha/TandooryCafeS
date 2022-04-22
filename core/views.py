from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.forms import ChargesForm, EmployeeForm, IngredientForm, LoginForm, SupplierForm, FoodForm, CategoryForm
from django.contrib.auth import login, logout, authenticate
from core.models import Charges, Food, FoodIngBridge, FoodIngredient, FoodOrderCount, Ingredient, Order, OrderFood, Supplier, User, Employee, Category, QRHistory, YearlyReport, ReportType
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import UpdateView
from datetime import datetime, timedelta
from django.core.mail import send_mail

def yearly_report(year, month, total_earnings):
    try:
        report_obj = YearlyReport.objects.get(year=year)
        if month == '1':
            report_obj.jan = total_earnings
        elif month == '2':
            report_obj.feb = total_earnings
        elif month == '3':
            report_obj.mar = total_earnings
        elif month == '4':
            report_obj.apr = total_earnings
        elif month == '5':
            report_obj.may = total_earnings
        elif month == '6':
            report_obj.jun = total_earnings
        elif month == '7':
            report_obj.jul = total_earnings
        elif month == '8':
            report_obj.aug = total_earnings
        elif month == '9':
            report_obj.sep = total_earnings
        elif month == '10':
            report_obj.oct = total_earnings
        elif month == '11':
            report_obj.nov = total_earnings
        elif month == '12':
            report_obj.dec = total_earnings
        else:
            pass        
    except:
        report_obj = YearlyReport(year=year)
        if month == '1':
            report_obj.jan = total_earnings
        elif month == '2':
            report_obj.feb = total_earnings
        elif month == '3':
            report_obj.mar = total_earnings
        elif month == '4':
            report_obj.apr = total_earnings
        elif month == '5':
            report_obj.may = total_earnings
        elif month == '6':
            report_obj.jun = total_earnings
        elif month == '7':
            report_obj.jul = total_earnings
        elif month == '8':
            report_obj.aug = total_earnings
        elif month == '9':
            report_obj.sep = total_earnings
        elif month == '10':
            report_obj.oct = total_earnings
        elif month == '11':
            report_obj.nov = total_earnings
        elif month == '12':
            report_obj.dec = total_earnings

    report_obj.save()


def calculations_report(current_orders, current_ingredient):
    total_earnings = 0
    total_payments = 0

    total_order = current_orders.count()
    total_stock = current_ingredient.count()
    current_order_with_payment = current_orders.filter(payment=True)
    for payed_order in current_order_with_payment:
        total_earnings+=int(payed_order.grand_total)

    for ingredient in current_ingredient:
        price = ingredient.quantity * ingredient.price_per_unit
        total_payments = price + total_payments 

    # print(f"Monthly report: total order:{total_order}, total stock:{total_stock}, total earning:{total_earnings}, total payments:{total_payments}")

    return total_stock, total_order, total_earnings, total_payments


def monthly_report_second():
    current_date = str(datetime.now().date())
    full_date = datetime.strptime(current_date, "%Y-%m-%d")
    year = full_date.year
    month = full_date.month
    startmonth = f'{year}-{month}-1'
    endmonth = f'{year}-{month}-30'
    current_orders = Order.objects.filter(order_date__gte=startmonth).filter(order_date__lte=endmonth).filter(ordered=True)
    current_ingredient = Ingredient.objects.filter(time_stamp__gte=startmonth).filter(time_stamp__lte=endmonth)

    total_stock, total_order, total_earnings, total_payments = calculations_report(current_orders, current_ingredient)

    yearly_report(year, str(month), total_earnings)

    return total_stock, total_order, total_earnings, total_payments    
    
from datetime import date    
import calendar
def weekly_report():
    monthly_report_second()
    day = str(datetime.now().date())
    dt = datetime.strptime(day, '%Y-%m-%d')
    
    curr_date = date.today()
    today = calendar.day_name[curr_date.weekday()]

    if today == "Sunday" or today == "Sun":
        start = dt
    else:
        start = dt - timedelta(days=dt.weekday()) - timedelta(days=1)

    end = start + timedelta(days=6)
    startday = start.strftime('%Y-%m-%d')
    endday = end.strftime('%Y-%m-%d')
    # print(start.strftime('%Y-%m-%d'))
    # print(end.strftime('%Y-%m-%d'))
    current_orders = Order.objects.filter(order_date__gte=startday).filter(order_date__lte=endday).filter(ordered=True)
    current_ingredient = Ingredient.objects.filter(time_stamp__gte=startday).filter(time_stamp__lte=endday)
    total_stock, total_order, total_earnings, total_payments = calculations_report(current_orders, current_ingredient)
    return total_stock, total_order, total_earnings, total_payments
    

def yearly_():
    monthly_report_second()
    current_date = str(datetime.now().date())
    full_date = datetime.strptime(current_date, "%Y-%m-%d")
    year = full_date.year
    startyear = f'{year}-1-1'
    endyear = f'{year}-12-30'
    current_orders = Order.objects.filter(order_date__gte=startyear).filter(order_date__lte=endyear).filter(ordered=True)
    current_ingredient = Ingredient.objects.filter(time_stamp__gte=startyear).filter(time_stamp__lte=endyear)
    total_stock, total_order, total_earnings, total_payments = calculations_report(current_orders, current_ingredient)
    return total_stock, total_order, total_earnings, total_payments

def daily_():
    monthly_report_second()
    current_date = str(datetime.now().date())
    full_date = datetime.strptime(current_date, "%Y-%m-%d")
    current_orders = Order.objects.filter(order_date=full_date).filter(ordered=True)
    current_ingredient = Ingredient.objects.filter(time_stamp__gte=full_date)
    total_stock, total_order, total_earnings, total_payments = calculations_report(current_orders, current_ingredient)
    return total_stock, total_order, total_earnings, total_payments    


def get_low_ingredients():
    ingredients = Ingredient.objects.filter(quantity__lte=5).order_by('quantity')
    low_ing_count = ingredients.count()
    ingredient_list = []
    count = 0
    for ingredient in ingredients:
        ingredient_list.append(ingredient)
        count+=1

        if count == 5:
            break
    return ingredient_list, low_ing_count

#loginrequired
def low_ingredients(request):
    ingredients = Ingredient.objects.filter(quantity__lte=5).order_by('quantity')
    ingredient_list, low_ing_count = get_low_ingredients()

    if low_ing_count > 5:
        return render(request,"pages/low_ingredient.html",{
            'ingredients': ingredients
        })
    else:
        return redirect('dashboard')
    

# #loginrequired
def dashboard_view(request):    
    # total_stock, expense = get_total_stock_and_price()
    # total_orders = Order.objects.filter(ordered=True).count()
    current_date = str(datetime.now().date())
    full_date = datetime.strptime(current_date, "%Y-%m-%d")
    current_year = full_date.year #from here we gotcurrent year
    counter = 0
    food_list = FoodOrderCount.objects.all().order_by('-count')
    new_list = []
    report_type = ''
    for foods in food_list:
        new_list.append(foods)
        counter+=1
        if counter == 4:
            break
    # print(new_list)

    ingredient_list, low_ing_count = get_low_ingredients()

    if low_ing_count > 5:
        low_ing_count = low_ing_count
    else:
        low_ing_count = 0

    try:
        selected_report = ReportType.objects.get(id=1)
    except:
        ReportType.objects.create(
            yearly=False,
            monthly=True,
            weekly=False
        )
        selected_report = ReportType.objects.get(id=1)

    if selected_report.yearly:
        total_stock, total_order, total_earnings, total_payments = yearly_()
        report_type = 'Yearly'
    elif selected_report.monthly:
        total_stock, total_order, total_earnings, total_payments = monthly_report_second()
        report_type = 'Monthly'
    elif selected_report.weekly:
        total_stock, total_order, total_earnings, total_payments = weekly_report() 
        report_type = 'Weekly'
    elif selected_report.daily:
        total_stock, total_order, total_earnings, total_payments = daily_()   
        report_type = 'Daily' 

    try:
        yearly_report_ = YearlyReport.objects.get(year=current_year)        
        context = {
            'total_stock': total_stock,
            'total_order': total_order,
            'total_payments': total_payments,
            'total_earnings': total_earnings, 
            'yearly_report': yearly_report_,
            'top_foods': new_list,   
            'report_type': report_type,
            'low_ingredient': ingredient_list,
            'low_ing_count': low_ing_count    
        }
        return render(request, "index.html", context)
    except:          
        context = {
            'total_stock': total_stock,
            'total_order': total_order,
            'total_payments': total_payments,
            'total_earnings': total_earnings,  
            'top_foods': new_list, 
            'report_type': report_type,
            'low_ingredient': ingredient_list,
            'low_ing_count': low_ing_count     
        }
        return render(request, "index.html", context)


#loginrequired
def report_type(request, selected):
    selected_report = ReportType.objects.get(id=1)  
    # print("URL hit")
    # print(selected)   
    if selected == "yearly":
        # print("Inside yearly")
        selected_report.yearly=True
        selected_report.monthly=False
        selected_report.weekly=False
        selected_report.daily=False
    elif selected == "monthly":
        selected_report.yearly=False
        selected_report.monthly=True
        selected_report.weekly=False
        selected_report.daily=False
    elif selected == "weekly":
        selected_report.yearly=False
        selected_report.monthly=False
        selected_report.weekly=True
        selected_report.daily=False
    elif selected == "daily":
        selected_report.yearly=False
        selected_report.monthly=False
        selected_report.weekly=False
        selected_report.daily=True
    else:
        return HttpResponse(status=404)
    selected_report.save()
    return redirect('dashboard')

def logoutView(request):
    logout(request)
    return redirect("login")

def loginView(request):
    if request.user.is_authenticated:        
        return redirect("dashboard")

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
                    return redirect("dashboard")
                else:
                    return render(request, "authentication/login.html", {
                        'message': 'Invalid Credential',
                        'forms': LoginForm(request.POST),
                    })
            except:
                return render(request, "authentication/login.html", {
                        'message': 'Invalid Credential',
                        'forms': LoginForm(request.POST),
                    })

    return render(request, "authentication/login.html", {"forms":LoginForm})

#loginrequired
def profile_view(request):
    return render(request,"profile.html")

# @permission_required('can_add_user', login_url="/")
#loginrequired
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

#loginrequired
def employee_view(request):    
    return render(request, "pages/employee_detail.html", {
        'employees': Employee.objects.all(),
    })

#loginrequired
def add_employee_view(request):
    if request.method == "POST":        
        employeeForm = EmployeeForm(request.POST)
        print(request.POST)
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

#loginrequired
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
   
#loginrequired
def supplier_view(request):  
    return render(request, "pages/supplier_detail.html", {
        'suppliers': Supplier.objects.all(),
    })


def get_total_stock_and_price():
    total_price = 0 
    ingredients = Ingredient.objects.all()  
    total_stock = ingredients.count() 
    for ingredient in ingredients:
        price = ingredient.quantity * ingredient.price_per_unit
        total_price+=price
    return total_stock, total_price    
       

#loginrequired
def add_ingredient_view(request):
    ing_found = False
    total_stock, total_price = get_total_stock_and_price() 
    if request.method == "POST":
        form = IngredientForm(request.POST)
        ing_obj = Ingredient.objects.all()
                    
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            if quantity <= 0:
                return render(request, "pages/add_ingredient.html", {
                    "form":form,
                    "total_stock":total_stock,
                    "total_price":total_price,
                    "message": 'Quantity Should be greater than 1',
                })                
            ingredient_name = request.POST.get('name')
            price_per_unit = form.cleaned_data.get('price_per_unit')
            for ing in ing_obj:
                if ingredient_name == ing.name:
                    currquantity = int(ing.quantity)
                    new_quantity = currquantity + int(quantity)
                    ing.quantity = new_quantity
                    ing.price_per_unit = price_per_unit
                    ing.time_stamp = datetime.now().date()                    
                    ing_found = True
                    ing.save()
                    break
            if not ing_found:
                form.save()
        else:
            return render(request, "pages/add_ingredient.html", {
                "form":form,
                "total_stock":total_stock,
                "total_price":total_price
            })
        return redirect("add_ingredient")

    return render(request, "pages/add_ingredient.html", {
        "form":IngredientForm,
        "total_stock":total_stock,
        "total_price":total_price
    })

#loginrequired
def add_supplier_view(request):
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            address = form.cleaned_data.get("address")
            contact = form.cleaned_data.get("contact")
            try:    
                get_contact = Supplier.objects.get(contact_number=contact) 
                return render(request,"pages/add_supplier.html",{
                    "form":form,
                    "message": "Supplier with that contact number already exist."
                })      
            except:                
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

#loginrequired
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

#loginrequired
def ingredient_view(request):
    return render(request, "pages/ingredient_detail.html",{
        'ingredients':Ingredient.objects.all(),
    })

class DeleteCrudIngredient(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Ingredient.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

#loginrequired
def edit_ingredient_view(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        unit = request.POST.get("unit")
        price_per_unit = request.POST.get("price-per-unit")
        supplier_id = request.POST.get("supplier")
        quantity = request.POST.get("quantity")
        print(request.POST)
        try:
            update_ingredient = Ingredient.objects.get(id=id)
            if name:
                update_ingredient.name = name
            if unit:
                update_ingredient.unit = unit
            if price_per_unit:
                update_ingredient.price_per_unit = price_per_unit
            if supplier_id:
                get_supplier = Supplier.objects.get(id=supplier_id)
                update_ingredient.supplier = get_supplier
            if quantity:
                update_ingredient.quantity = quantity
            update_ingredient.save()
            return redirect("ingredient")
        except:
            return HttpResponse(status=404)
    try:
        get_ingredient = Ingredient.objects.get(id=id)   
        return render(request, "pages/edit_ingredient.html", {
            'edit_ingredient': get_ingredient,
            'suppliers': Supplier.objects.all(),
        })  
    except:
        return HttpResponse(status=404)

#loginrequired
def add_food_view(request):
    foods = Food.objects.all()
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            try:
                image = request.FILES['image']
            except:
                return render(request, 'pages/add_food.html', {
                        'form':form,
                        'img_message': 'You should upload an image.'
                    })
            name = form_data.get("name")
            for food in foods:
                if name == food.name:
                    return render(request, 'pages/add_food.html', {
                        'form':form,
                        'message': 'Food Already Added!'
                    })
            category = form_data.get("category")
            price = form_data.get("price")
            get_category = Category.objects.get(name=category)
            new_food = Food(
                name = name,
                category = get_category,
                price = price,
                image=image
            )
            new_food.save()
            return redirect('add_food')
        return render(request, 'pages/add_food.html', {'form':form})

    return render(request, 'pages/add_food.html', {'form':FoodForm})

#loginrequired
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()            
            return redirect('add_category')
        else:
            return render(request, 'pages/add_category.html', {'form':form, 'categories': Category.objects.all()})
    return render(request, 'pages/add_category.html', {'form':CategoryForm, 'categories': Category.objects.all()})

#loginrequired
def category_view(request):
    return render(request, 'pages/category_detail.html',{
        'categorys': Category.objects.all(),
    })

class DeleteCrudUserCategory(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Category.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)

#loginrequired
def food_view(request):
    return render(request, "pages/food_detail.html",{
        'foods':Food.objects.all(),
    })


class DeleteCrudFood(View):
    def get(self, request):
        id1 = request.GET.get('id', None)
        Food.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


#loginrequired
def edit_food_view(request, id):
    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category")
        price = request.POST.get("price")
        try:
            update_food = Food.objects.get(id=id)
            if name:
                update_food.name = name
            if price:
                update_food.price = price
            if category_id:
                get_category = Category.objects.get(id=category_id)
                update_food.category = get_category
            update_food.save()
            return redirect("food")
        except:
            return HttpResponse(status=404)
    try:
        get_food = Food.objects.get(id=id)
        print(get_food)
        return render(request, "pages/edit_food.html", {
            'edit_food': get_food,
            'categories': Category.objects.all(),
        }) 
    except:
        return HttpResponse(status=404)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'pages/edit_category.html'

    def get_success_url(self):
        return reverse('category_detail')
    
def delete_category(request, id):
    category = Category.objects.get(id=id).delete()
    return redirect('add_category')

def charges_view(request):
    if request.method == "POST":
        form = ChargesForm(request.POST)
        if form.is_valid():    
            vat = form.cleaned_data.get('vat')        
            try:
                charges = Charges.objects.get(id=1)
                charges.vat=vat
                charges.save()
            except:
                charges = Charges(vat=vat)
                charges.save()
            return redirect('charges')
        else:
            return render(request, 'pages/charges.html',{
                'form': form,
                'charge': Charges.objects.get(id=1)
            })
        
    try:    
        charges = Charges.objects.get(id=1)
    except:
        Charges.objects.create(
            vat=13
        )
    return render(request, 'pages/charges.html',{
        'form': ChargesForm,
        'charge': Charges.objects.get(id=1)
    })

#orders
#loginrequired
def order_view(request):
    return render(request,'pages/order.html', {
        'foods':Food.objects.all(),
    })

def calculate_charges(total_amount):
    print(f"Order_total: {total_amount}")
    try:
        charges = Charges.objects.get(id=1)
    except:
        charges = Charges(
            vat=13
        )
        charges.save()
    vat = charges.vat  
    vat_amt =(total_amount*vat)/100
    # print(f"VAT: {vat_amt}")
    net_price = total_amount + int(vat_amt)
    return net_price


class AddOrder(View):
    def get(self, request):
        id = request.GET.get('id', None)
        quantity = request.GET.get('quantity', None)
        order_id = request.GET.get('order_id', None)
        food = Food.objects.get(id=id)  
        try:
            get_food_count = FoodOrderCount.objects.get(food=food)
            get_food_count.count = get_food_count.count+1
            get_food_count.save()
        except:
            new_food_order_counter = FoodOrderCount(food=food)
            new_food_order_counter.count = new_food_order_counter.count+1
            new_food_order_counter.save()

        if order_id:
            print("Order Exist")
            order = Order.objects.get(id=order_id)
            print(order.id)
            food_order = OrderFood.objects.filter(order=order)
            food_order_found = 0
            for orders in food_order:
                if orders.food.id == food.id:
                    food_order_found += 1
                    orders.quantity += 1
                    orders.price = orders.food.price * orders.quantity
                    orders.save()
                    order.sub_total += food.price
                    order.save()
                    break

            if food_order_found == 0:
                order_food = OrderFood(order=order, food=food, quantity=1, price=food.price)
                order_food.save()
                order.sub_total += food.price
                order.save()
            
        else:        
            # print("Order Doesn't exist")          
            vat = Charges.objects.get(id=1).vat
            order = Order(order_description="Order in process.", sub_total=0, ordered=False, status=False, vat=vat)
            order.sub_total += food.price        
            order.save()                
            order_food = OrderFood(order=order, food=food, quantity=1, price=food.price)
            order_food.save()
        
        total_price = calculate_charges(order.sub_total)
        # order_ = Order.objects.get(id=order_id)
        # order_.grand_total = total_price        
        print(f" Total price:  {total_price}")        
        charges = Charges.objects.get(id=1)        
        c_data = {
            'id':food.id,
            'food_name': food.name,
            'quantity': quantity,
            'price': food.price,
            'order_id': order.id,
            'order_total': order.sub_total,
            'vat': charges.vat,
            'total_price': total_price
        }

        order_data = {
            'order': c_data
        }
        return JsonResponse(order_data)

#loginrequired
def order_detail_view(request, id):
    order_obj = get_object_or_404(Order, id=id)
    if order_obj.ordered:
        order_foods = OrderFood.objects.filter(order=order_obj)        
        return render(request, 'pages/order_detail.html', {
            'order': order_obj,
            'order_food': order_foods,
        })
    else:
        return HttpResponse(status=404)

def calculate_grand_total(id):
    order_obj = Order.objects.get(id=id)
    net_price = 0
    discount = int(order_obj.discount)
    vat = int(order_obj.vat)                          
    currprice = int(order_obj.sub_total)

    #calculating discounted amount
    disc_amt = round((currprice*discount)/100)
    net_price = currprice - int(disc_amt)

    #calculating vat amount
    vat = Charges.objects.get(id=1).vat
    vat_amt =round((net_price*vat)/100)
    net_price = net_price + int(vat_amt)

    order_obj.grand_total=net_price
    order_obj.save()

#loginrequired
def save_order_detail(request):
    if request.method == "POST":    
        order = request.POST.get("order")
        if order:
            order_obj = Order.objects.get(id=request.POST.get('order_id'))
            order_obj.ordered = True     
            order_obj.save()
            calculate_grand_total(request.POST.get('order_id'))

                
        return HttpResponseRedirect(reverse('order_view', args=(order_obj.id,)))

    else:
        return HttpResponse(status=404)

#loginrequired
def order_table_view(request):
    return render(request, "pages/order_table.html",{
        'order_obj': Order.objects.filter(ordered=True),
    })


def calculatePrice(order_id, discount):
    net_price = 0
    discount = int(discount)
    order = Order.objects.get(id=order_id)  
    currprice = int(order.sub_total)
    disc_amt = round((currprice*discount)/100)
    net_price = currprice - int(disc_amt)

    vat = Charges.objects.get(id=1).vat
    vat_amt =round((net_price*vat)/100)
    net_price = net_price + int(vat_amt)
    
    return int(net_price)

class UpdatePrice(View):
    def get(self, request):
        order_id = request.GET.get('order_id', None)
        discount = request.GET.get('discount', None)
        order = Order.objects.get(id=order_id)
        order.discount = int(discount)        
        order.vat = Charges.objects.get(id=1).vat
        order.save()

        new_total = calculatePrice(order_id, discount)
        c_data = {
            'total':new_total,            
        }

        price_data = {
            'price': c_data
        }
        return JsonResponse(price_data)

#loginrequired
def update_order(request,id):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        order_obj = Order.objects.get(id=order_id)
        payment = request.POST.get('payment')
        discount = request.POST.get('discount')
        # print(type(discount))
        # print(request.POST)
        # print(payment)           
        try:
            discount = int(discount)
            if discount > 0:
                order_obj.discount = discount
                print("discounted")
        except:
            return reverse('update_order')     
        if payment:
            order_obj.payment = True
            order_foods = OrderFood.objects.filter(order=order_obj)        
            #decreasing ingredient quantity according to order..
            for food in order_foods: 
                order_food_quantity = food.quantity               
                food_ingredient = FoodIngBridge.objects.filter(food_ing__food=food.food)                
                # print(food_ingredient)
                for ingredients in food_ingredient:
                    food_ing_quantity = ingredients.quantity
                    ing = Ingredient.objects.get(id=ingredients.ingredient.id)
                    used_quantity = order_food_quantity * food_ing_quantity
                    remaining_quantity = ing.quantity
                    super_user = User.objects.filter(is_superuser=True)[0]                                        
                    email = super_user.email                    

                    if remaining_quantity < used_quantity:                        
                        print("Out of stock")
                    else:
                        ing.quantity = remaining_quantity - used_quantity
                        ing.save() 

                        if int(ing.quantity) <= 5:
                            send_mail(
                                'Stock Update!!',
                                f'Your stock for {ing.name} is getting low, You may contact {ing.supplier.contact_number}.',
                                from_email=None,
                                recipient_list=[f'{email}'],
                                fail_silently=False,
                            )
                            print('Send mail stock low')
        else:
            order_obj.payment = False
        order_obj.save()
                 
        return HttpResponseRedirect(reverse('order_view', args=(order_obj.id,)))
    if not id:
        return HttpResponse(status=404)
    context = {
        'foods': OrderFood.objects.filter(order__id=id),
        'order': Order.objects.get(id=id)
    }
    return render(request, 'pages/edit_order.html', context)

#loginrequired
#qr scanner
def scanner_view(request):
    return render(request, 'pages/qr_scan.html')

#loginrequired
def decrease_stock(request, id):
    ing = Ingredient.objects.get(id=id)
    super_user = User.objects.filter(is_superuser=True)[0]                                        
    email = super_user.email   
    if request.method == "POST":
        quantity = request.POST.get('quantity')
        try:
            quantity = float(quantity)
            curr_quantity = ing.quantity
            if curr_quantity < quantity:
                return render(request, 'pages/decrease_stock.html',{
                    'ingredient': ing,
                    'message': 'Stock is less than entered number.' 
                })  
            else:            
                ing.quantity = curr_quantity-quantity
                ing.save()
                if int(ing.quantity) <= 5:
                    send_mail(
                        'Stock Update!!',
                        f'Your stock for {ing.name} is getting low, You may contact {ing.supplier.contact_number}.',
                        from_email=None,
                        recipient_list=[f'{email}'],
                        fail_silently=False,
                    )
                    print('Send mail stock low')
                newQRHist = QRHistory(
                    ing_name = ing.name,
                    quantity = quantity
                )
                newQRHist.save()
        except:
            return render(request, 'pages/decrease_stock.html',{
                'ingredient': ing,
                'message': 'Please enter a number.' 
            })

        return redirect('ingredient')

    return render(request, 'pages/decrease_stock.html',{
        'ingredient': ing 
    })

#loginrequired
def qr_history_view(request):
    return render(request,"pages/qr_history_detail.html",{
        'qrhistories': QRHistory.objects.all(),
    })

#loginrequired
def food_ing_view(request):
    foods = Food.objects.all()
    ingredients = Ingredient.objects.all()

    context = {
        'foods': foods,
        'ingredients': ingredients
    }
    if request.method == "POST":
        food = foods.get(id=request.POST.get("foods"))
        ingredient = ingredients.get(id=request.POST.get("ing"))
        quantity = request.POST.get("quantity")
        try:
            quantity = float(quantity)
            if quantity <= 0:
                context['message'] = "The quantity should be greater than 0."
                return render(request, "pages/fooding.html",context)
        except:
            context['message'] = "Quantity should be in number."
            return render(request, "pages/fooding.html",context)

        try:
            food_ing = FoodIngredient.objects.get(food=food)
            FoodIngBridge.objects.create(
                food_ing=food_ing,
                ingredient=ingredient,
                quantity=quantity,
            ) 
        except:
            new_fooding_obj = FoodIngredient(food=food)
            new_fooding_obj.save()
            FoodIngBridge.objects.create(
                food_ing=new_fooding_obj,
                ingredient=ingredient,
                quantity=quantity,
            ) 

    return render(request,"pages/fooding.html", context)

#loginrequired
def food_ing_detail_view(request):
    return render(request,"pages/food_ing_detail.html",{
        'food_ings': FoodIngBridge.objects.all(),
    })

#loginrequired
def delete_food_ing(request,id):
    food_ing = FoodIngBridge.objects.get(id=id)
    food_ing.delete()
    return redirect('food_ing_detail_view')