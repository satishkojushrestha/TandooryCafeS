from cgitb import reset
from re import L
from turtle import position
from urllib import response
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.contrib import auth
from django.urls import reverse
from core.forms import EmployeeForm
from core.models import Category, Charges, Employee, Food, Ingredient, Supplier

# Create your tests here.

# class TestPage(TestCase):

#    def setUp(self):
#        self.client = Client()

#    def test_index_page(self):
#        url = reverse('dashboard')
#        response = self.client.get(url)
#        self.assertEqual(response.status_code, 200)
#     #    self.assertTemplateUsed(response, 'index.html')
#     #    self.assertContains(response, 'Company Name XYZ')

# class SignInViewTest(TestCase):

#     def setUp(self):
#         self.user = get_user_model().objects.create_user(username='test',
#                                                         password='12test12',
#                                                         email='test@example.com')

#     def tearDown(self):
#         self.user.delete()

#     def test_correct(self):
#         response = self.client.post('', {'username': 'test', 'password': '12test12'})
#         self.assertTrue(response.data['authenticated'])

#     def test_wrong_username(self):
#         response = self.client.post('', {'username': 'wrong', 'password': '12test12'})
#         self.assertFalse(response.data['authenticated'])

#     def test_wrong_pssword(self):
#         response = self.client.post('', {'username': 'test', 'password': 'wrong'})
#         self.assertFalse(response.data['authenticated'])


class ViewTest(TestCase):    

    def test_login_username_or_password_not_correct(self):
        print('******************test_login_username_or_password_not_correct()**********************')
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
        print('Response status code : ' + str(response.status_code))
        # self.assertNotIn(b'User name or password is not correct', response.content)
        # self.assertIn(b'Search', response.content)

class dashboardViewTest(TestCase):

    def test_home_page(self):
        print('******************test_home_page()**********************')
        # send GET request.
        response = self.client.get('/dashboard/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        #returns htm content of the page
        # print('Response content : ' + str(response.content))


# class addEmployeeViewTest(TestCase):

#     def add_employee_test(self):
#         print('******************test_add_employee_page()**********************')
#         # epmForm = EmployeeForm(
#         #     first_name="Satish",
#         #     last_name="Shrestha",
#         #     position="cook",
#         #     age="21",
#         #     salary='20000'
#         # )
#         new_emp_data = {'first_name': ['Saroj'], 'last_name': ['Manandhar'], 'position': ['Cook'], 'age': ['22'], 'salary': ['20000']}
#         # empForm = EmployeeForm()
#         # print(empForm)

        
#         # empForm["first_name"]="Satish"
#         # empForm["last_name"] ="Shrestha",
#         # empForm["position"] ="cook",
#         # empForm["age"] ="21",
#         # empForm["salary"] ='20000'

#         response = self.client.get(path='/employee/new/')
#         # response = self.client.post(path='/employee/new/', data=new_emp_data)
#         print('Response status code : ' + str(response.status_code))
#         self.assertEqual(response.status_code, 200)

class employeeView(TestCase):

    def test_employees_page(self):
        print('******************test_home_page()**********************')
        # send GET request.
        response = self.client.get('/employee/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        #returns htm content of the page
        # print('Response content : ' + str(response.content))

class addEmployeeView(TestCase):
 
    def test_add_employee_view(self):
        print('******************test_add_employee_view()**********************')
        add_employee_test_data = {'first_name': 'Saroj', 'last_name': 'Manandhar', 'position': 'Cook', 'age': '22', 'salary': '20000'}
        response = self.client.post(path='/employee/new/', data=add_employee_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        # print('Response message : ' + str(response.context["message"]))
        self.assertEqual(response.status_code, 200)
        # if the provided string exist in the response content html, then pass.
        # self.assertIn(b'Invalid Credential', response.content)


# class editEmployee(TestCase):
    
#     def test_edit_employee_view(self):
#         print('******************test_edit_employee_view()**********************')
#         edit_employee_test_data = {'first_name': 'Saroj', 'last_name': 'Manandhar', 'position': 'Cook', 'age': '22', 'salary': '20000'}
#         response = self.client.post(path='/employee/edit/3/', data=edit_employee_test_data, follow=True)
#         print('Response status code : ' + str(response.status_code))
#         # print('Response message : ' + str(response.context["message"]))
#         self.assertEqual(response.status_code, 200)


class editEmployeeView(TestCase):

    def setUp(self) -> None:
        Employee.objects.create(
            first_name = 'Saroj',
            last_name = 'Manandhar',
            position = 'Helper',
            age = '20',
            salary = 11000
        )

    def test_edit_employee(self):
        edit_employee_test_data = {'first_name': 'Saroj', 'last_name': 'Manandhar', 'position': 'Cook', 'age': '22', 'salary': '20000'}
        response = self.client.post('/employee/edit/1/',data=edit_employee_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        # print('Response message : ' + str(response.context["employees"]))
        self.assertEqual(response.status_code, 200)



class deleteEmployee(TestCase):
    def setUp(self) -> None:
        Employee.objects.create(
            first_name = 'Saroj',
            last_name = 'Manandhar',
            position = 'Cook',
            age = '22',
            salary = 20000
        )

    def test_delete_employee(self):
        # response = self.client.delete(path='/ajax/crud/delete/', data=edit_employee_test_data, follow=True)
        response= self.client.get(reverse('crud_ajax_delete'),data={'id':1})
        print('Response status code : ' + str(response.status_code))
        # print('Response message : ' + str(response.context["message"]))
        self.assertEqual(response.status_code, 200)


class viewProfile(TestCase):

    def test_view_profile_view(self):
        response = self.client.get('/profile/')
        print('Response status code: ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class addOrderTest(TestCase):

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
        response= self.client.get(reverse('c_ajax_create_order'),data={'id':1,'quantity':1})
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
        print('Response content : ' + str(response.content))


class foodsDetailView(TestCase):

    def test_food_detail_view(self):
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


class editFoodView(TestCase):

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
        edit_food_test_data = {'price': '100'}
        response = self.client.post('/food/edit/1/',data=edit_food_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class deleteFoodView(TestCase):
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
        # response = self.client.delete(path='/ajax/crud/delete/', data=edit_employee_test_data, follow=True)
        response= self.client.get(reverse('crud_ajax_delete_food'),data={'id':1})
        print('Response status code : ' + str(response.status_code))
        # print('Response message : ' + str(response.context["message"]))
        self.assertEqual(response.status_code, 200)      



#supplier
class supplierDetailView(TestCase):

    def test_supplier_detail_view(self):
        response = self.client.get('/supplier/')
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)
 

class addSupplierViewTest(TestCase):

    def test_add_food_test(self):        
        print('******************test_add_food_view()**********************')
        add_supplier_test_data = {'first_name': 'Satish', 'last_name': 'Shrestha', 'address': 'Bhaktapur', 'contact_number': '123456789'}
        response = self.client.post(path='/supplier/new/', data=add_supplier_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)


class editSupplierView(TestCase):

    def setUp(self) -> None:
        Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

    def test_edit_food(self):
        edit_supplier_test_data = {'address': 'Katunje', 'contact_number': '1122334555'}
        response = self.client.post('/supplier/edit/1/',data=edit_supplier_test_data, follow=True)
        print('Response status code : ' + str(response.status_code))
        self.assertEqual(response.status_code, 200)



class deleteSupplierView(TestCase):
    def setUp(self) -> None:
        Supplier.objects.create(
            first_name = 'Satish', 
            last_name = 'Shrestha', 
            address = 'Bhaktapur',
            contact_number = 123456789
        )

    def test_delete_employee(self):       
        response= self.client.get(reverse('crud_ajax_delete_supplier'),data={'id':1})
        print('Response status code : ' + str(response.status_code))        
        self.assertEqual(response.status_code, 200)     


#ingredient
class ingredientDetailView(TestCase):

    def test_supplier_detail_view(self):
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

    def test_add_ingredient_test(self):        
        print('******************test_add_ingredient_test()**********************')
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

    def test_edit_food(self):
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

    def test_delete_employee(self):       
        response= self.client.get(reverse('crud_ajax_delete_ingredient'),data={'id':1})
        print('Response status code : ' + str(response.status_code))        
        self.assertEqual(response.status_code, 200)      