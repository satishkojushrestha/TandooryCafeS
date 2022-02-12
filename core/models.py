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
    salary = models.IntegerField()
    
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
    name = models.CharField(max_length=20, unique=True)
    unit = models.CharField(max_length=20)
    price_per_unit = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT)    
    time_stamp = models.DateField(auto_now_add=True)
    quantity = models.IntegerField()
    qr = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return str(self.pk)
        # return self.name

    def save(self, *args, **kwargs):
        db_count = Ingredient.objects.count()
        if db_count == 0:
            get_pk = 1
        else:
            last_pk = Ingredient.objects.last()
            get_pk = str(last_pk.pk+1)
            # print(get_pk)
        qr_url = f'{self.name}/{get_pk}'
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