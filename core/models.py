from email.policy import default
from http.cookiejar import DefaultCookiePolicy
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
#for generating qr code
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.conf import settings

class User(AbstractUser):
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    position = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    start_date = models.DateField(auto_now_add=True)
    salary = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Supplier(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=11)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)
    price_per_unit = models.PositiveIntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT)    
    time_stamp = models.DateField(auto_now_add=True)
    quantity = models.FloatField()
    qr = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        # return str(self.pk)
        return self.name

    def save(self, *args, **kwargs):
        db_count = Ingredient.objects.count()
        if db_count == 0:
            get_pk = 1
        else:
            last_pk = Ingredient.objects.last()
            get_pk = str(last_pk.pk+1)
            # print(get_pk)
                      
        # qr_url = f'http://192.168.1.130:8000/stock/decrease/{get_pk}'
        qr_url = f'http://127.0.0.1:8000/stock/decrease/{get_pk}'
        qrcode_img = qrcode.make(qr_url)
        qr_size = qrcode_img.pixel_size
        canvas = Image.new('RGB', (qr_size+8, qr_size+5), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}'+'.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr.save(fname, File(buffer), save=False)
        canvas.close()
        super(Ingredient, self).save(*args, **kwargs)        


class Category(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return str(self.name)


class Food(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='foods', default="foods/default3.svg", null=False, blank=False)

    def __str__(self) -> str:
        return str(self.name)


class Charges(models.Model):
    vat = models.IntegerField()


class Order(models.Model):
    order_description = models.CharField(max_length=150)
    time_stamp = models.DateTimeField(auto_created=True, auto_now_add=True)
    order_date = models.DateField(auto_created=True, auto_now_add=True)
    sub_total = models.IntegerField(default=0)
    grand_total = models.IntegerField(default=0)
    ordered = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    payment = models.BooleanField(default=False)
    discount = models.IntegerField(default=0)
    vat = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return f" {self.order.id} -> {self.food.name}"


class FoodIngredient(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)   

    def __str__(self):
        return self.food.name 


class FoodIngBridge(models.Model):
    food_ing = models.ForeignKey(FoodIngredient, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()   

    def __str__(self):
        return f"{self.food_ing} - {self.ingredient}" 


class QRHistory(models.Model):
    ing_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    scanned_date = models.DateTimeField(auto_now_add=True)


class YearlyReport(models.Model):
    year = models.CharField(max_length=20)
    jan = models.PositiveIntegerField(default=0)
    feb = models.PositiveIntegerField(default=0)
    mar = models.PositiveIntegerField(default=0)
    apr = models.PositiveIntegerField(default=0)
    may = models.PositiveIntegerField(default=0)
    jun = models.PositiveIntegerField(default=0)
    jul = models.PositiveIntegerField(default=0)
    aug = models.PositiveIntegerField(default=0)
    sep = models.PositiveIntegerField(default=0)
    oct = models.PositiveIntegerField(default=0)
    nov = models.PositiveIntegerField(default=0)
    dec = models.PositiveIntegerField(default=0)


class FoodOrderCount(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.food.name} -> {self.count}'
        

class ReportType(models.Model):
    yearly = models.BooleanField(default=False)
    monthly = models.BooleanField(default=False)
    daily = models.BooleanField(default=True)
    weekly = models.BooleanField(default=False)