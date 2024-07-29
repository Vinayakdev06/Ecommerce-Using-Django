from django.contrib import admin
from . models import Product
from .models import Customer, Product, Cart

# Register your models here.

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'discounted_price', 'category', 'product_image']

admin.site.register(Product, ProductModelAdmin)
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']    
    
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']