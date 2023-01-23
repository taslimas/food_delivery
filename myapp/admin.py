from django.contrib import admin
from .models import Food,Customer,Cart
# Register your models here.

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    
    list_display=('id','name','price','category','food_image')
    

@admin.register(Customer)    
class CustomerModelaAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','pincode']
   
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','product_qty']    

