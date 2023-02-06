from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.models import Group
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    
    list_display=('id','name','price','category','food_image')
    

@admin.register(Customer)    
class CustomerModelaAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','state','pincode']
   
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','product_qty']    
    
@admin.register(Payment)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','razorpay_order_id','amount','razorpay_payment_status','razorpay_payment_id','paid']    

@admin.register(OrderPlaced)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer','product','quantity','ordered_date','status','payment']    

admin.site.unregister(Group)