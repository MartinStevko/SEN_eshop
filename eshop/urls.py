from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'eshop'

urlpatterns = [
    path('index', views.index, name='index'),
    path('contact', views.contact_us, name='contact'),
    path('categories/<int:division_id>', views.categories, name='categories'),
    path('products/<int:category_id>', views.products, name='products'),
    path('product/<int:product_id>', views.product_view, name='product'),
    path('basket', views.basket, name='basket'),
    path('order', views.order, name='order'),
    url(r'^', views.nothing),
]

# Inside template:
# {{ request.META.HTTP_HOST }}
