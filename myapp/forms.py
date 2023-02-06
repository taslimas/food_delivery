from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordResetForm,SetPasswordForm
from django import forms
from django.contrib.auth.models import User
from .models import Customer,Food,Cart


class CustomerRegistrationForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
    def save(self, commit=True):
        user = super(CustomerRegistrationForm, self).save(commit=False)
        user.username=self.cleaned_data['username']
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    

class LoginForm(AuthenticationForm):
    username=UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))




class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','mobile','state','pincode']
        widget={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'})
        }

#forgot password

class MypasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
        
class MySetPasswordForm(SetPasswordForm):
    new_password1=forms.CharField(label='New Password',widget=forms.PasswordInput(attrs={'autocomplte':'current-password','class':'form-control'}))
    new_password2=forms.CharField(label='Confirm New Password',widget=forms.PasswordInput(attrs={'autocomplte':'current-password','class':'form-control'}))  
 
PRODUCT_QUANTITY=[(i,str(i)) for i in range(1,21)] 
class CartAddproductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY,coerce=int)
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)
    
    
        