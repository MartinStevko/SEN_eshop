from django.shortcuts import render, redirect

from django.utils import timezone
from django.core.mail import send_mail

from .models import *

def index(request):
    template = 'eshop/index.html'

    divisions = Division.objects.all()
    categories = Category.objects.all()

    return render(request, template, {'divisions':divisions, 'categories':categories})

def contact_us(request):
    template = 'eshop/contact_us.html'

    divisions = Division.objects.all()
    categories = Category.objects.all()

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
        return render(request, template, {'divisions':divisions, 'categories':categories})

def categories(request):
    template = 'eshop/categories.html'

    divisions = Division.objects.all()
    categories = Category.objects.all()

    return render(request, template, {'divisions':divisions, 'categories':categories})

def products(request):
    pass

def product_view(request, number):
    pass

def basket(request):
    pass

def order(request):
    pass
