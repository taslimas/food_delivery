from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse,HttpResponse
# Create your views here.
from .forms import CustomerRegistrationForm,LoginForm,CustomerProfileForm,ReviewForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages   
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.db.models import Q
from django.views import View
from django.contrib.auth.decorators import login_required
from django.conf import settings
import razorpay
import random
from .helper import MessageHandler
from django.contrib.auth.models import User
from django.conf import  settings
from django.core.mail import send_mail
def index(request):
    
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'index.html',locals())

def about(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        
    return render(request,'about.html',locals())

def contact(request):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'contact.html',locals())

def category(request,val):
    totalitem=0
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    food=Food.objects.filter(category=val)
    name=Food.objects.filter(category=val).values('name')
    return render(request,'category.html',locals())


def fooddetails(request,pk):
    food=Food.objects.get(pk=pk)
    food1=Food.objects.all()
    totalitem=0
    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=food.id, status=True)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'fooddetail.html',locals())

def category_title(request,val):
    food=Food.objects.filter(name=val)
    name=Food.objects.filter(category=food[0].category).values('name')
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'category.html',locals())


def customerregistration(request):
    if request.method=='GET':
        form=CustomerRegistrationForm()
        return render(request,'customeregistration.html',locals())
    if request.method=='POST':
        form=CustomerRegistrationForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request,"Your account has been successfully created")
            return redirect("login")   
        else:
            messages.error(request,"Invalid input data")  
             
    return render(request,'customeregistration.html',locals())     


def LoginView(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            form=login(request,user)
            return redirect('/')
        else:
            messages.info(request, f'Username and Password are incorrect')
    form = AuthenticationForm()
    return render(request,'login.html',locals())

def ProfileView(request):
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    if request.method=='GET':
        form=CustomerProfileForm()
        return render(request,'profile.html',locals())
    if request.method=='POST':
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
              user=request.user
              name=form.cleaned_data['name']
              locality=form.cleaned_data['locality']
              city=form.cleaned_data['city']
              state=form.cleaned_data['state']
              mobile=form.cleaned_data['mobile']
              pincode=form.cleaned_data['pincode']
              reg=Customer(user=user,name=name,locality=locality,city=city,state=state,mobile=mobile,pincode=pincode)
              reg.save()
              messages.success(request,"Congratulations,Profile saved successfully")
        else:
              messages.warning(request,"Invalid input data")    
    return render(request,'profile.html',locals())

def Address(request):
    address=Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    return render(request,'address.html',locals())

def UpdateAddress(request,pk):
    if request.method=="GET":
        address=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=address)
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,"updateaddress.html",locals())
    if request.method=="POST":
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            address=Customer.objects.get(pk=pk)
            address.name=form.cleaned_data['name']
            address.locality=form.cleaned_data['locality']
            address.city=form.cleaned_data['city']
            address.state=form.cleaned_data['state']
            address.mobile=form.cleaned_data['mobile']
            address.pincode=form.cleaned_data['pincode']
            address.save()
            messages.success(request,"Congratulations,Profile Update successfully")
        else:
            messages.warning(request,"Invalid input data") 
        return redirect('address')    
       
       
def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)   
        if form.is_valid():
            user=form.save()      
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('passwordchangedone')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {'form': form}) 




        
#cart
@login_required(login_url='login')
def add_to_cart(request,pk):
    user=request.user
   
    food=Food.objects.get(pk=pk)
    Cart(user=user,product=food).save()
    return redirect('/cart')
@login_required(login_url='login')    
def show_cart(request):
   user=request.user
   cart=Cart.objects.filter(user=user)
   if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
   print(user)
   amount=0
   for p in cart:
       value = p.product_qty * p.product.discount_price
       amount= amount + value
       totalamount= amount + 40   
   return render(request,'addtocart.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.product_qty+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.product_qty * p.product.discount_price
            amount= amount + value
        totalamount= amount + 40  
        data={
            'quantity':c.product_qty,
            'amount':amount,
            'totalamount':totalamount
            }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.product_qty-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.product_qty * p.product.discount_price
            amount= amount + value
        totalamount= amount + 40  
        data={
            'quantity':c.product_qty,
            'amount':amount,
            'totalamount':totalamount
            }
        return JsonResponse(data)

            
        
  

def removeItem(request,pk):
    food=Food.objects.get(pk=pk)
    cart=Cart.objects.filter(product=food).delete()
    totalitem=0
    
    return redirect('cart')

def updatecart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        if(Cart.objects.filter(user=request.user,product_id=prod_id)):
            prod_qty=int(request.POST.get('product_qty'))
            cart=Cart.objects.get(product_id=prod_id,user=request.user)
            cart. product_qty=prod_qty
            cart.save()
            return JsonResponse({'status':"Updated Succeffuly"})
    return redirect('cart')           
    
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        order_placed=OrderPlaced.objects.filter(user=request.user)
        famount=0
        for p in cart_items:
            value = p.product_qty * p.product.discount_price
            famount=famount+value
        totalamount=famount+40  
        razoramount=int(totalamount*100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))  
        data = { "amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12" }
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id=payment_response['id']
        order_status=payment_response['status']
        if order_status=='created':
            payment=Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status,
                
            )
            payment.save()
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            
        return render(request,"checkout.html",locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')    
    cust_id=request.GET.get('cust_id')
    user=request.user
    print(user)
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid=True
    payment.razorpay_payment_id=payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.product_qty,payment=payment).save()
        c.delete()
    return redirect('orders')    


def orders(request):
    order_placed=OrderPlaced.objects.filter(user=request.user)
    
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        
    return render(request,'orders.html',locals())


def search(request):
     
    query=request.GET['search']
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
    product=Food.objects.filter(name__contains=query)
    
    return render(request,"search.html",locals())




    
    


def submit_review(request, pk):
    if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user)) 
    user=Food(request.user)
    product=Food.objects.get(pk=pk)
    review = ReviewRating.objects.filter(product=product)
    print(review)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST,instance=user)
        if form.is_valid():
            data = ReviewRating()
            data.subject = form.cleaned_data['subject']
            data.rating = form.cleaned_data['rating']
            data.review = form.cleaned_data['review']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = product.id
            data.user_id = request.user.id
            data.save()
           
            # messages.success(request, 'Thank you! Your review has been submitted.')
            return redirect('review',pk=product.id)
       
    context={'product':product,'review':review}
    return render (request,"review.html",context)      

def DeleteReview(request,pk):
    review = ReviewRating.objects.get(pk=pk)
    review.delete()
    return redirect('orders')

def email(request):
    if request.method=='POST':
        email=request.POST.get('email')
        if email=="tasliarshad11@gmail.com":
            messages.success(request,'Check Your Email!!')
            return redirect('otp')
        else: 
            messages.info(request,'Invalid Email')
            return redirect('email')
    return render(request,'email.html',locals())        
                
        
    
    
global no
no=0
def otp(request):
    global no
    
    if request.method=='POST':
        otp=request.POST.get('otp','')
        
        if otp=="{}".format(no):
            messages.success(request,"Email Verified!!!")
            return redirect('customer-registration')
        else:
            messages.info(request,"Invalid OTP")
            return redirect('otp')
    
    no=random.randrange(1000,9999) 
    send_mail("Your OTP Verification",'Your OTP is {}'.format(no),'tasliarshad11@gmail.com',['tasliarshad11@gmail.com'],fail_silently=False,)   
    return render(request,'otp.html',{})
      
    
    
    
    
    
    

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
