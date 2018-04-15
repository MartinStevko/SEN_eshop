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

    try:
        message = request.session['message']
    except(KeyError):
        message = None;

    if message:
        del request.session['message']
        return render(request, template, {'message':message, 'menu':menu})
    else:
        return render(request, template, {'menu':menu})

def nothing(request):
    return redirect('eshop:index')

def contact_us(request):
    template = 'eshop/contact_us.html'

    menu = []
    divisions = Division.objects.all()
    for divis in divisions:
        temp = []
        categories = Category.objects.filter(idDivision=divis)
        temp.append(divis)
        temp.append(categories)
        menu.append(temp)

    if request.method == "POST":
        # name not null (html)
        # mail not null (html)
        # subject not null (html)
        subject = str(request.POST['subject'])
        adress = str(request.POST['adress'])
        house = str(request.POST['house'])
        # text not null (html)
        mail_text = str(request.POST['text'])

        try:
            name = str(request.POST['name'])
        except(SyntaxError, NameError, KeyError):
            message = 'Zadajte vaše meno!'
            return render(request, template, {'menu':menu, 'message':message})

        try:
            from_mail = str(request.POST['from'])
        except(SyntaxError, NameError, KeyError):
            message = 'Zadajte správnu emailovú adresu!'
            return render(request, template, {'menu':menu, 'message':message})

        text = "E-mail from: %s\nAdress: %s\nHouse number: %s\n \nText: %s" % (name, adress, house, mail_text)

        send_mail(subject, text, from_mail, ['mstevko10@gmail.com', 'matkon1999@gmail.com'], fail_silently=True)

        return redirect('eshop:contact')
    else:
        return render(request, template, {'menu':menu})

def categories(request, division_id):
    template = 'eshop/categories.html'

    menu = []
    try:
        dvsn = Division.objects.get(pk=division_id)
    except(Division.DoesNotExist):
        mes = 'Hľadaná skupina kategórií neexistuje.'
        request.session['message'] = mes
        return redirect('eshop:index')
    ctgr = Category.objects.filter(idDivision=dvsn)
    divisions = Division.objects.all()

    for divis in divisions:
        if divis != dvsn:
            temp = []
            categories = Category.objects.filter(idDivision=divis)
            temp.append(divis)
            temp.append(categories)
            menu.append(temp)

    try:
        ctgr[0]
    except(IndexError):
        mes = 'Vo vybranej skupine momentálne neexistujú žiadne kategórie produktov.'
        request.session['message'] = mes
        return redirect('eshop:index')

    return render(request, template, {'ctgr':ctgr, 'dvsn':dvsn, 'categories':categories, 'menu':menu})

def products(request, category_id):
    template = 'eshop/products.html'

    menu = []
    try:
        category = Category.objects.get(pk=category_id)
    except(KeyError, ValueError, NameError, SyntaxError, Category.DoesNotExist):
        mes = 'Hľadaná kategória neexistuje.'
        request.session['message'] = mes
        return redirect('eshop:index')

    dvsn = category.idDivision
    ctgr = Category.objects.filter(idDivision=dvsn)
    divisions = Division.objects.all()

    for divis in divisions:
        if divis != dvsn:
            temp = []
            categories = Category.objects.filter(idDivision=divis)
            temp.append(divis)
            temp.append(categories)
            menu.append(temp)

    products = Product.objects.filter(idCategory=category)

    try:
        products[0]
    except(IndexError):
        mes = 'Vo vybranej kategórii neexistujú žiadne produkty.'
        request.session['message'] = mes
        return redirect('eshop:index')

    return render(request, template, {'ctgr':ctgr, 'dvsn':dvsn, 'category':category, 'products':products, 'menu':menu})

def product_view(request, product_id):
    the_product = ''
    pass

def basket(request):
    pass

def order(request):
    pass
