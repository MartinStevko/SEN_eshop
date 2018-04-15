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

        mes = 'Správa bola úspešne odoslaná.'
        request.session['message'] = mes

        return redirect('eshop:contact')
    else:
        try:
            message = request.session['message']
        except(KeyError):
            message = None;

        if message:
            del request.session['message']
            return render(request, template, {'message':message, 'menu':menu})
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
    template = 'eshop/product_view.html'

    try:
        the_product = Product.objects.get(pk=product_id)
    except(KeyError, ValueError, NameError, SyntaxError, Product.DoesNotExist):
        mes = 'Hľadaný produkt neexistuje.'
        request.session['message'] = mes
        return redirect('eshop:index')

    the_specification = Specification.objects.filter(idProduct=the_product)
    the_gallery = Gallery.objects.filter(idProduct=the_product)
    the_review = Review.objects.filter(idProduct=the_product).order_by('-time')

    menu = []
    dvsn = the_product.idCategory.idDivision
    ctgr = Category.objects.filter(idDivision=dvsn)
    divisions = Division.objects.all()

    for divis in divisions:
        if divis != dvsn:
            temp = []
            categories = Category.objects.filter(idDivision=divis)
            temp.append(divis)
            temp.append(categories)
            menu.append(temp)

    if request.method == "POST":
        if "add_to_cart" in request.POST:
            amount = request.POST["amount"]
            temp_cart = [product_id, amount]

            try:
                cart = request.session['cart']
            except(KeyError):
                cart = []

            add = True
            for item in cart:
                if item[0] == temp_cart[0]:
                    item[1] = int(item[1])
                    item[1] += int(temp_cart[1])
                    add = False

            if add:
                cart.append(temp_cart)

            request.session['cart'] = cart

            return redirect('eshop:basket')
        elif "add_review" in request.POST:
            author = str(request.POST["author"])
            mail = request.POST["mail"]
            text = request.POST["text"]

            Review.objects.create(idProduct=the_product, author=author, email=mail, text=text)

            return redirect('eshop:product', product_id)
        else:
            return redirect('eshop:product', product_id)
    else:
        return render(request, template, {
            'the_product':the_product,
            'the_specification':the_specification,
            'the_gallery':the_gallery,
            'the_review':the_review,
            'dvsn':dvsn,
            'ctgr':ctgr,
            'menu':menu
        })

def basket(request):
    template = 'eshop/basket.html'

    try:
        cart = request.session['cart']
    except(KeyError):
        cart = []

    products = Product.objects.all()

    menu = []
    divisions = Division.objects.all()
    for divis in divisions:
        temp = []
        categories = Category.objects.filter(idDivision=divis)
        temp.append(divis)
        temp.append(categories)
        menu.append(temp)

    price_sum = 0
    for item in cart:
        temp_p = Product.objects.get(pk=item[0]).price
        price_sum += int(temp_p)*int(item[1])

    if request.method == "POST":
        for i in range(len(cart)):
            name = 'remove' + str(cart[i][0])

            if name in request.POST:
                del cart[i]
                request.session['cart'] = cart

                return redirect('eshop:basket')

        if "order" in request.POST:
            for item in request.POST:
                item = str(item)
                if 'amount' in item:
                    item_id = int(item[6:])
                    for prod in cart:
                        if prod[0] == item_id:
                            prod[1] = int(prod[1])
                            prod[1] += int(request.POST[item])
            request.session['cart'] = cart

            return redirect('eshop:order')
        else:
            return redirect('eshop:basket')

    else:
        return render(request, template, {
            'menu':menu,
            'cart':cart,
            'products':products,
            'price_sum':price_sum
        })

def order(request):
    pass
