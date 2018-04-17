from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.utils import timezone
from django.core.mail import send_mail

from json import dumps, loads
from string import ascii_uppercase, digits
from random import choice

from .models import *

##### Not views #####
def generate_serial():
    numA = ''
    numB = ''

    for i in range(6):
        numA += choice(ascii_uppercase)

    for i in range(4):
        numB += choice(digits)

    num = numA[:4] + numB[:1] + numA[4:] + numB[1:]

    return num

def validate_serial(number):
    try:
        f = open('serial_numbers.txt', 'r')
    except(FileNotFoundError):
        return True

    valid = True
    for line in f:
        if number in line:
            valid = False
            break

    f.close()

    return valid

def register_serial(number):
    with open('serial_numbers.txt', 'a') as f:
        f.write(number + '\n')

def get_serial():
    num = generate_serial()

    while validate_serial(num) != True:
        num = generate_serial()

    register_serial(num)
    return num
####################

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
                            prod[1] = int(request.POST[item])
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
    template = 'eshop/order.html'

    menu = []
    divisions = Division.objects.all()
    for divis in divisions:
        temp = []
        categories = Category.objects.filter(idDivision=divis)
        temp.append(divis)
        temp.append(categories)
        menu.append(temp)

    try:
        cart = request.session['cart']
    except(KeyError):
        cart = []

    if cart == []:
        mes = 'V košíku nemáte žiadne položky. Nie je si čo objednať.'
        request.session['message'] = mes
        return redirect('eshop:index')

    else:
        price = 0
        ocb = []

        for item in cart:
            prod = Product.objects.get(pk=item[0])
            temp = [prod.name, item[1]]
            ocb.append(temp)
            price += prod.price*item[1]

        if request.method == "POST":
            if "order" in request.POST:
                serial_number = get_serial()
                amount = dumps(cart)

                first_name = request.POST['fname']
                surname = request.POST['surname']
                phone_number = request.POST['phone']

                manner = request.POST['getting']

                street = request.POST['street']
                house_number = int(request.POST['house'])
                city_town = request.POST['town']
                pdn = request.POST['pdn']

                note = request.POST['note']

                ord = Order.objects.create(
                    serial_number = serial_number,
                    amount = amount,
                    price = price,
                    getting = manner,
                    first_name = first_name,
                    surname = surname,
                    phone = phone_number,
                    street = street,
                    house = house_number,
                    town = city_town,
                    pdn = pdn,
                    note = note
                )

                for item in cart:
                    prod = Product.objects.get(pk=item[0])
                    ord.products.add(prod)
                ord.save()

                request.session['cart'] = []

                mes = "Vaša odjednávka bola zaznamenaná pod číslom " + serial_number + ". Budeme vás kontaktovať formou SMS správy. Ďakujeme!"
                request.session['message'] = mes

                return redirect('eshop:index')

            else:
                return redirect('eshop:order')

        else:
            return render(request, template, {'menu':menu, 'price':price, 'cart':ocb})
