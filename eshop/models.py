from django.db import models

from django.utils import timezone

class Division(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return "{}".format(self.name)

class Category(models.Model):
    idDivision = models.ForeignKey(Division, on_delete=models.PROTECT)

    name = models.CharField(max_length=30, unique=True)
    image = models.ImageField()

    def __str__(self):
        return "{} - {}".format(self.idDivision, self.name)

class Product(models.Model):
    idCategory = models.ForeignKey(Category, on_delete=models.PROTECT)

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    specification = models.TextField()

    in_storage = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

class Galery(models.Model):
    idProduct = models.ForeignKey(Product, on_delete=models.PROTECT)

    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField()

class Review(models.Model):
    idProduct = models.ForeignKey(Product, on_delete=models.PROTECT)

    author = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=250)

    text = models.TextField()
    time = models.DateTimeField(default=timezone.now)
