from django.contrib import admin
from .models import Product, Registration, CustomUser, AddToCart

# Register your models here.
admin.site.register(Product)
admin.site.register(Registration)
admin.site.register(CustomUser)
admin.site.register(AddToCart)