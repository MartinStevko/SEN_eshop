from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.utils import timezone
from django.core.mail import send_mail

from .models import *

def index(request, message=None):
    template = 'eshop/index.html'

    menu = []
    divisions = Division.objects.all()
    for divis in divisions:
        temp = []
        categories = Category.objects.filter(idDivision=divis)
        temp.append(divis)
        temp.append(categories)
        menu.append(temp)

    if message:
        return render(request, template, {'message':message, 'menu':menu})
    else:
        return render(request, template, {'menu':menu})

def nothing(request):
    return redirect('eshop:index')

def contact_us(request):
    template = 'eshop/contact_us.html'

    divisions_menu = Division.objects.all()
    categories_menu = Category.objects.all()

    if request.method == 'POST':
        # subject not null (html)
        subject = request.POST['subject']
        mail_text = request.POST['text']

        try:
            from_mail = request.POST['from']
        except():
            message = 'Zadajte správnu emailovú adresu!'
            return render(request, template, {'divisions':divisions, 'categories':categories, 'message':message})

        try:
            from_mail = str(from_mail)
        except():
            message = 'Zadajte správnu emailovú adresu!'
            return render(request, template, {'divisions':divisions, 'categories':categories, 'message':message})

        try:
            name = str(request.POST['name'])
        except():
            message = 'Zadajte vaše meno!'
            return render(request, template, {'divisions':divisions, 'categories':categories, 'message':message})

        text = 'E-mail from: ' + name + '\n \n' + 'Text: ' + str(mail_text)

        send_mail(subject, text, from_mail, ['mstevko10@gmail.com', 'matkon1999@gmail.com'], fail_silently=False)
    else:
        return render(request, template, {'divisions_menu':divisions_menu, 'categories_menu':categories_menu})

def categories(request, division_id):
    template = 'eshop/categories.html'

    divisions_menu = Division.objects.all()
    categories_menu = Category.objects.all()

    categories = Category.objects.filter(idDivision=division_id)

    return render(request, template, {'categories':categories, 'divisions_menu':divisions_menu, 'categories_menu':categories_menu})

def products(request, category_id):
    template = 'eshop/products.html'

    divisions_menu = Division.objects.all()
    categories_menu = Category.objects.all()

    try:
        category = Category.objects.get(pk=category_id)
        products = Product.object.filter(idCategory=category_id)
    except(TypeError, KeyError, ValueError, Product.DoesNotExist):
        mes = 'Kategória produktov neexistuje!'
        return redirect(index, message=mes)

    return render(request, template, {'products':products, 'category':category, 'divisions_menu':divisions_menu, 'categories_menu':categories_menu})

def product_view(request, product_id):
    the_product = ''
    pass

def basket(request):
    pass

def order(request):
    pass
