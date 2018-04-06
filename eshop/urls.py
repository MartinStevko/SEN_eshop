from django.urls import path

from . import views

app_name = 'eshop'

urlpatterns = [
    path('index', views.index, name='index'),
    path('contact', views.contact_us, name='contact'),
    path('categories', views.categories, name='categories'),
    path('products', views.products, name='products'),
    path('product/<int:number>', views.product_view, name='product'),
    path('basket', views.basket, name='basket'),
    path('order', views.order, name='order'),
    path('', views.index),
]
