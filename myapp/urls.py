from django.urls import path
from django.contrib import admin
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,MypasswordResetForm,MySetPasswordForm


urlpatterns=[
    path('',views.index,name='index'),
   
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('category/<slug:val>',views.category,name='category'),
    path('food-detail/<int:pk>',views.fooddetails,name='fooddetail'),
    path('category-title/<val>',views.category_title,name='category-title'),
    path('profile',views.ProfileView,name='profile'),
    path('address',views.Address,name='address'),
    path('update_address/<int:pk>',views.UpdateAddress,name='update_address'),
    # user authentication
    path('customer-registration',views.customerregistration,name='customer-registration'),
    path('login/',views.LoginView,name='login'),
    path('changepassword',views.ChangePassword,name='changepassword'),
    path('passwordchangedone',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),
    path('otp/',views.otp,name='otp'),
    path('email/',views.email,name='email'),
     #cart
    path('add-to-cart/<int:pk>',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.show_cart,name='cart'),
    path('checkout/',views.checkout.as_view(),name='checkout'),
    path('paymentdone/',views.payment_done,name='paymentdone'),
    path('removeitem/<int:pk>',views.removeItem,name='removeitem'),
    # path('update-post',views.updateCart,name='updatecart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    # path('removecart/',views.removecart),
    path('update-cart',views.updatecart,name='updatecart'),
    path('orders/',views.orders,name='orders'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:pk>/', views.submit_review, name='review'),
    
    path('delete-review/<int:pk>/',views.DeleteReview, name='review_delete'),

    
    # forgot password
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MypasswordResetForm),name='password_reset'),
    path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'),
        name='password_reset_complete'),
  
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header="Food Express"
admin.site.site_title="Food Express"
admin.site.site_index_title="Welcome to Food Express"