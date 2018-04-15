from django.db import models

from django.utils import timezone

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

    description = models.TextField()

    in_storage = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

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
