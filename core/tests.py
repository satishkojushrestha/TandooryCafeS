from django.test import TestCase
from django.urls import reverse
from core.models import Category, Charges, Employee, Food, Ingredient, Supplier


class LoginViewTest(TestCase):    

    def test_login_password_not_correct(self):
        print('******************test_login_password_not_correct()**********************')
        login_account_test_data = {'email': 'admin@gmail.com', 'password': 'qqqqqq'}
        response = self.client.post(path='', data=login_account_test_data)
        print('Response status code : ' + str(response.status_code))
        print('Response message : ' + str(response.context["message"]))
        self.assertEqual(response.status_code, 200)
        # if the provided string exist in the response content html, then pass.
        self.assertIn(b'Invalid Credential', response.content)
        

    def test_login_success(self):
        print('******************test_login_success()**********************')
        login_account_test_data = {'email': 'admin@gmail.com', 'password': 'admin'}
        response = self.client.post(path='', data=login_account_test_data)
        self.assertEqual(response.status_code, 200)
        print('Response status code : ' + str(response.status_code))


class DashboardViewTest(TestCase):

    def test_home_page(self):
        print('******************test_home_page()**********************')
        # send GET request.
        response = self.client.get('/dashboard/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class EmployeeViewTest(TestCase):

    def test_employees_page(self):
        print('******************test_employees_page()**********************')
        response = self.client.get('/employee/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class AddEmployeeViewTest(TestCase):
 
    def test_add_employee_view(self):
        print('******************test_add_employee_view()**********************')
        add_employee_test_data = {'first_name': 'Saroj', 'last_name': 'Manandhar', 'position': 'Cook', 'age': '22', 'salary': '20000'}
        response = self.client.post(path='/employee/new/', data=add_employee_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class EditEmployeeViewTest(TestCase):

    def setUp(self) -> None:
        #creating employee at the start
        Employee.objects.create(
            first_name = 'Saroj',
            last_name = 'Manandhar',
            position = 'Helper',
            age = '20',
            salary = 11000
        )

    def test_edit_employee(self):
        print('******************test_edit_employee()**********************')
        edit_employee_test_data = {'position': 'Cook', 'age': '22', 'salary': '20000'}
        response = self.client.post('/employee/edit/1/',data=edit_employee_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        #after editing the employee edit employee view redirects to employee page where we can access all the available employees objects
        print('Response message : ' + str(response.context["employees"]))
        self.assertEqual(response.status_code, 200)



class DeleteEmployeeViewTest(TestCase):

    def setUp(self) -> None:
        Employee.objects.create(
            first_name = 'Saroj',
            last_name = 'Manandhar',
            position = 'Cook',
            age = '22',
            salary = 20000
        )

    def test_delete_employee(self):
        print('******************test_delete_employee()**********************')
        response= self.client.get(reverse('crud_ajax_delete'),data={'id':1})
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class viewProfileTest(TestCase):

    def test_view_profile_view(self):
        print('******************test_view_profile_view()**********************')        
        response = self.client.get('/profile/')
        print('Response status code: ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class addOrderViewTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="Beverage"
        )

        Food.objects.create(
            name = "Coke",
            category = self.category,
            price = 80
        )

        Charges.objects.create(
            vat=15
        )

    def test_add_order_test(self):
        print('******************test_add_order_test()**********************')                
        response= self.client.get(reverse('c_ajax_create_order'),data={'id':1,'quantity':1})
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        print('Response content : ' + str(response.content))


class foodsDetailViewTest(TestCase):

    def test_food_detail_view(self):
        print('******************test_food_detail_view()**********************')
        response = self.client.get('/food/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
 

class addFoodViewTest(TestCase):

    def setUp(self) -> None:
        Category.objects.create(
            name="Fast Food"
        )

    def test_add_food_test(self):        
        print('******************test_add_food_view()**********************')
        add_food_test_data = {'name': 'MoMo', 'category': 'Fast Food', 'price': '80'}
        response = self.client.post(path='/addfood/', data=add_food_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class editFoodViewTest(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="Fast Food"
        )

        Food.objects.create(
            name = 'MoMo', 
            category = self.category, 
            price = 80
        )

    def test_edit_food(self):
        print('******************test_edit_food()**********************')
        edit_food_test_data = {'price': '100'}
        response = self.client.post('/food/edit/1/',data=edit_food_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class deleteFoodViewTest(TestCase):
    
    def setUp(self) -> None:
        self.category = Category.objects.create(
            name="Fast Food"
        )

        Food.objects.create(
            name = 'MoMo', 
            category = self.category, 
            price = 80
        )

    def test_delete_employee(self):
        #calling the url with url name and passing data id in it.
        #crud_ajax_delete_food , is a url name..
        print('******************test_delete_employee()**********************')
        response= self.client.get(reverse('crud_ajax_delete_food'),data={'id':1})
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)      


class supplierDetailViewTest(TestCase):

    def test_supplier_detail_view(self):
        print('******************test_supplier_detail_view()**********************')
        response = self.client.get('/supplier/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
 

class addSupplierViewTest(TestCase):

    def test_add_supplier_view(self):        
        print('******************test_add_supplier_view()**********************')
        add_supplier_test_data = {'first_name': 'Satish', 'last_name': 'Shrestha', 'address': 'Bhaktapur', 'contact_number': '123456789'}
        response = self.client.post(path='/supplier/new/', data=add_supplier_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class editSupplierViewTest(TestCase):

    def setUp(self) -> None:
        Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

    def test_edit_supplier(self):
        print('******************test_edit_supplier()**********************')
        edit_supplier_test_data = {'address': 'Katunje', 'contact_number': '1122334555'}
        response = self.client.post('/supplier/edit/1/',data=edit_supplier_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class deleteSupplierViewTest(TestCase):

    def setUp(self) -> None:
        Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

    def test_delete_supplier(self):      
        print('******************test_delete_supplier()**********************')
        response= self.client.get(reverse('crud_ajax_delete_supplier'),data={'id':1})
        print('Response status code : ' + str(response.status_code))        
        self.assertEqual(response.status_code, 200)     


class ingredientDetailViewTest(TestCase):

    def test_ingredient_detail_view(self):
        print('******************test_ingredient_detail_view()**********************')
        response = self.client.get('/ingredient/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
 

class addIngredientViewTest(TestCase):

    def setUp(self) -> None:
        Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

    def test_add_ingredient_view(self):        
        print('******************test_add_ingredient_view()**********************')
        add_ingredient_test_data = {'name': 'Frozen MoMo', 'unit': 'Pkts', 'price_per_unit': '50', 'supplier': Supplier.objects.get(id=1), 'quantity': 12.0}
        response = self.client.post(path='/addingredient/', data=add_ingredient_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))       
        self.assertEqual(response.status_code, 200)


class editIngredientView(TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

        Ingredient.objects.create(
            name = 'Frozen MoMo', 
            unit = 'Pkts', 
            price_per_unit = '50', 
            supplier = self.supplier, 
            quantity = 12.0
        )

    def test_edit_ingredent_view(self):
        print('******************test_edit_ingredent_view()**********************')
        edit_ingredient_test_data = {'price_per_unit': '70', 'quantity': 10.0}
        response = self.client.post('/ingredient/edit/1/',data=edit_ingredient_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class deleteIngredientView(TestCase):

    def setUp(self) -> None:
        self.supplier = Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

        Ingredient.objects.create(
            name = 'Frozen MoMo', 
            unit = 'Pkts', 
            price_per_unit = '50', 
            supplier = self.supplier, 
            quantity = 12.0
        )

    def test_delete_ingredient_view(self):       
        print('******************test_delete_ingredient_view()**********************')
        response= self.client.get(reverse('crud_ajax_delete_ingredient'),data={'id':1})
        print('Response status code : ' + str(response.status_code))        
        self.assertEqual(response.status_code, 200)      