from telnetlib import STATUS
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from core.forms import ChargesForm, EmployeeForm, IngredientForm, LoginForm, SupplierForm, FoodForm, CategoryForm
from django.contrib.auth import login, logout, authenticate
from core.models import Charges, Food, FoodIngBridge, Ingredient, Order, OrderFood, Supplier, User, Employee, Category
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic import UpdateView


@login_required(login_url="/")
def dashboard_view(request):
    return render(request, "index.html")

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


def get_total_stock_and_price():
    total_price = 0 
    ingredients = Ingredient.objects.all()  
    total_stock = ingredients.count() 
    for ingredient in ingredients:
        price = ingredient.quantity * ingredient.price_per_unit
        total_price+=price
    return total_stock, total_price    
       

@login_required(login_url="/")
def add_ingredient_view(request):
    total_stock, total_price = get_total_stock_and_price() 
    if request.method == "POST":
        form = IngredientForm(request.POST)
        if form.is_valid():
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

@login_required(login_url="/")
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

@login_required(login_url="/")
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

@login_required(login_url="/")
def add_food_view(request):
    if request.method == 'POST':
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            form_data = form.cleaned_data
            image = request.FILES['image']
            name = form_data.get("name")
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

@login_required(login_url="/")
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()            
            return redirect('add_category')
        else:
            return render(request, 'pages/add_category.html', {'form':form, 'categories': Category.objects.all()})
    return render(request, 'pages/add_category.html', {'form':CategoryForm, 'categories': Category.objects.all()})

@login_required(login_url="/")
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

@login_required(login_url="/")
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


@login_required(login_url="/")
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
        

    return render(request, 'pages/charges.html',{
        'form': ChargesForm,
        'charge': Charges.objects.get(id=1)
    })

#orders
@login_required(login_url="/")
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
            print("Order Doesn't exist")          
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

@login_required(login_url="/")
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

@login_required(login_url="/")
def save_order_detail(request):
    if request.method == "POST":    
        order = request.POST.get("order")
        if order:
            order_obj = Order.objects.get(id=request.POST.get('order_id'))
            order_obj.ordered = True     
            order_obj.save()
            calculate_grand_total(request.POST.get('order_id'))

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
                    remaining_quantity = int(ing.quantity)

                    if remaining_quantity < used_quantity:
                        print("Out of stock")
                    else:
                        ing.quantity = remaining_quantity - used_quantity
                        ing.save()  

                
        return HttpResponseRedirect(reverse('order_view', args=(order_obj.id,)))

    else:
        return HttpResponse(status=404)

@login_required(login_url="/")
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
        else:
            order_obj.payment = False
        order_obj.save()
        calculate_grand_total(order_id)
        return HttpResponseRedirect(reverse('order_view', args=(order_obj.id,)))
    if not id:
        return HttpResponse(status=404)
    context = {
        'foods': OrderFood.objects.filter(order__id=id),
        'order': Order.objects.get(id=id)
    }
    return render(request, 'pages/edit_order.html', context)


#qr scanner
def scanner_view(request):
    return render(request, 'pages/qr_scan.html')

def decrease_stock(request, id):
    ing = Ingredient.objects.get(id=id)

    if request.method == "POST":
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            curr_quantity = int(ing.quantity )
            ing.quantity = curr_quantity-quantity
            ing.save()
        except:
            return render(request, 'pages/decrease_stock.html',{
                'ingredient': ing,
                'message': 'Stock is less than entered number.' 
            })

        return redirect('ingredient')

    return render(request, 'pages/decrease_stock.html',{
        'ingredient': ing 
    })