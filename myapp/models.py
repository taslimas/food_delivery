
from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15)
    otp=models.CharField(max_length=100,null=True,blank=True)
    uid=models.CharField(default=f'{uuid.uuid4}',max_length=200)
    
    def __str__(self):
        return self.phone_number,self.otp
class Food(models.Model):
    CATEGORY_CHOICES=(
        ('bi','Biriyani'),
        ('pz','Pizza'),
        ('br','Burger'),
        ('sh','Shawarma'),
        ('ch','Chicken'),
        ('pr','Paratha'),
        ('sw','Sandwich'),
        ('ds','Dosa'),
        ('fr','Fried Rice'),
        ('nd','Noodles'),
        ('md','Mandhi'),
    )
    name=models.CharField(max_length=50)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    description=models.TextField()
    active=models.BooleanField()
    price=models.FloatField()
    discount_price=models.FloatField()
    is_veg=models.BooleanField()
    # quantity=models.PositiveIntegerField()
    food_image=models.ImageField(upload_to='Dishes')
    
    def __str__(self):
        return self.name
    
    
class Customer(models.Model):
    STATE_CHOICES=(("Select State","Select State"),
        ("Andhra Pradesh","Andhra Pradesh"),
                       ("Arunachal Pradesh ","Arunachal Pradesh "),
                       ("Assam","Assam"),
                       ("Bihar","Bihar"),
                       ("Chhattisgarh","Chhattisgarh"),
                       ("Goa","Goa"),
                        ("Gujarat","Gujarat"),
                       ("Haryana","Haryana"),
                       ("Himachal Pradesh","Himachal Pradesh"),
                       ("Jammu and Kashmir ","Jammu and Kashmir "),
                       ("Jharkhand","Jharkhand"),
                       ("Karnataka","Karnataka"),
                       ("Kerala","Kerala"),
                       ("Madhya Pradesh","Madhya Pradesh"),
                       ("Maharashtra","Maharashtra"),
                       ("Manipur","Manipur"),
                       ("Meghalaya","Meghalaya"),
                       ("Mizoram","Mizoram"),
                       ("Nagaland","Nagaland"),
                       ("Odisha","Odisha"),
                       ("Punjab","Punjab"),
                       ("Rajasthan","Rajasthan"),
                       ("Sikkim","Sikkim"),
                       ("Tamil Nadu","Tamil Nadu"),
                       ("Telangana","Telangana"),
                       ("Tripura","Tripura"),
                       ("Uttar Pradesh","Uttar Pradesh"),
                       ("Uttarakhand","Uttarakhand"),
                       ("West Bengal","West Bengal"),
                       ("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
                       ("Chandigarh","Chandigarh"),
                       ("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
                       ("Daman and Diu","Daman and Diu"),
                       ("Lakshadweep","Lakshadweep"),
                       ("National Capital Territory of Delhi","National Capital Territory of Delhi"),
                       ("Puducherry","Puducherry"))
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.CharField(max_length=10)
    pincode=models.CharField(max_length=6)
    state=models.CharField(choices=STATE_CHOICES,max_length=100,default="Select state")
        
    def ___str__(self):
        return self.name

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Food,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False,default=1)
   
    
    @property
    def total_cost(self):
        return self. product_qty * self.product.discount_price
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)
        
    
STATUS_CHOICES =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the Way','On the Way'),
    ('Delivered','Deliverd'),('Cancel','Cancel'),('Pending','Pending'),
)
class OrderPlaced(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product=models.ForeignKey(Food,on_delete=models.CASCADE,null=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES)
   
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discount_price
    
class ReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Food, on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.TextField(max_length=500,blank=True)
    rating = models.FloatField()
    ip=models.CharField(max_length=20,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject}, {self.rating}"    
        
        