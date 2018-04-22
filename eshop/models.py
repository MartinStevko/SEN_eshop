from django.db import models

from django.utils import timezone
from random import randint

class Division(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return "{}".format(self.name)

class Category(models.Model):
    idDivision = models.ForeignKey(Division, on_delete=models.PROTECT)

    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField(upload_to="categories")
    description = models.TextField()

    def __str__(self):
        return "{} - {}".format(self.idDivision, self.name)

class Product(models.Model):
    idCategory = models.ForeignKey(Category, on_delete=models.PROTECT)

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="products")

    short_description = models.CharField(max_length=300, default="", unique=False)
    description = models.TextField()
    price = models.PositiveSmallIntegerField(default=10)

    in_storage = models.BooleanField(default=False)

    def __str__(self):
        if self.in_storage:
            return "{} (na sklade)".format(self.name)
        else:
            return "Chýba! - {}".format(self.name)

class Specification(models.Model):
    idProduct = models.ForeignKey(Product, on_delete=models.PROTECT)

    name = models.CharField(max_length=50, unique=False)
    value = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return "{} - {}".format(self.name, self.idProduct)

class Gallery(models.Model):
    idProduct = models.ForeignKey(Product, on_delete=models.PROTECT)

    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to="gallery")

    def __str__(self):
        return "Image{} - {}".format(self.id, self.idProduct)

class Review(models.Model):
    idProduct = models.ForeignKey(Product, on_delete=models.PROTECT)

    author = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=250)

    text = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{} - {}".format(self.id, self.idProduct)

class Order(models.Model):
    serial_number = models.CharField(max_length=10, unique=True, default='0000000000')

    products = models.ManyToManyField(Product)
    amount = models.TextField()
    price = models.IntegerField(default=0, unique=False)

    getting = models.CharField(max_length=10, unique=False)

    first_name = models.CharField(max_length=50, unique=False)
    surname = models.CharField(max_length=50, unique=False)
    phone = models.CharField(max_length=20, unique=False)

    street = models.CharField(max_length=100, unique=False)
    house = models.CharField(max_length=10, unique=False)
    town = models.CharField(max_length=50, unique=False)
    pdn = models.CharField(max_length=10, unique=False)

    note = models.TextField()

    def __str__(self):
        return "Order {}".format(self.serial_number)
