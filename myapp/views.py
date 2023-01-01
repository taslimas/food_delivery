from django.shortcuts import render,redirect
from .models import Food,Customer,Cart
from django.http import JsonResponse
# Create your views here.
from .forms import CustomerRegistrationForm,LoginForm,CustomerProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages   
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.db.models import Q








def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def category(request,val):
    food=Food.objects.filter(category=val)
    name=Food.objects.filter(category=val).values('name')
    return render(request,'category.html',locals())


def fooddetails(request,pk):
    food1=Food.objects.all()
    food=Food.objects.get(pk=pk)
    return render(request,'fooddetail.html',locals())

def category_title(request,val):
    food=Food.objects.filter(name=val)
    name=Food.objects.filter(category=food[0].category).values('name')
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
    return render(request,'address.html',locals())

def UpdateAddress(request,pk):
    if request.method=="GET":
        address=Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=address)
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
def add_to_cart(request,pk):
    user=request.user
   
    food=Food.objects.get(pk=pk)
    Cart(user=user,food=food).save()
    return redirect('/cart')
    
def show_cart(request):
   user=request.user
   cart=Cart.objects.filter(user=user)
   amount=0
   for p in cart:
       value = p.quantity * p.food.discount_price
       amount= amount + value
       totalamount= amount + 40   
   return render(request,'addtocart.html',locals())

# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(food=prod_id) & Q(user=request.user))
#         c.quantity+=1
#         c.save()
#         user=request.user
#         cart=Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value = p.quantity * p.food.discount_price
#             amount= amount + value
#         totalamount= amount + 40  
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#             }
#         return JsonResponse(data)
        
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
