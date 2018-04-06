from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *

def index(request):
    template = 'eshop/index.html'

    divisions = Division.objects.all()
    categories = Category.objects.all()

    return render(request, template, {'divisions':divisions, 'categories':categories})

def contact_us(request):
    pass

def categories(request):
    pass

def products(request):
    pass

def product_view(request, number):
    pass

def basket(request):
    pass

def order(request):
    pass
