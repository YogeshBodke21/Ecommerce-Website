from django.contrib import admin
from .models import Product, UserProfile, Cart
# Register your models here.

@admin.register(Product)
class ProdectModelAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'selling_price', 'discounted_price', 'description','category', 'product_image']

@admin.register(UserProfile)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'locality', 'city', 'pincode','state', 'country']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']