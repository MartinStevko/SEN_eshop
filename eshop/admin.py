from django.contrib import admin

from .models import *

admin.site.register(Division)
admin.site.register(Category)

admin.site.register(Product)
admin.site.register(Galery)

admin.site.register(Review)