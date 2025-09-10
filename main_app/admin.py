from django.contrib import admin
from .models import Cart, Cartitem, Product, Order, Category
# Register your models here.
admin.site.register(Cart)
admin.site.register(Cartitem)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
