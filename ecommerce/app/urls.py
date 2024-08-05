from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('home/', home , name='home'),
    path('about/', about , name='about'),
    path('contact/', contact, name='contact'),
    path('category/<slug:val>', category_view, name='category'),
    path('product-detail/<int:pk>', Product_detail_view.as_view(), name='product-detail'),
    path('address/', address_view, name='address'),
    path('update-address/<int:pk>', UpdateAddressView.as_view(), name='update-address'),
    path('delete-ad/<int:pk>', delete_view, name='delete-ad'),

    #cart
    path('add-to-cart', add_to_cart, name="add-to-cart"),
    path('show-cart/', show_cart, name="show-cart"),
    path('delete-cart/<int:pk>', remove_cart, name="delete-cart"),
    path('checkout/', Checkout_view.as_view(), name="checkout"),
    path('plusc/', plus_cart, name="plusc"),

    #search
    path('search', search, name='search'),


    #login authentication urls
    path('registration/', CustomerRegistrationView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password_change/', Password_Change_View.as_view(template_name='app/password_change.html'), name="password-change" ),
    path('password_success/', password_success, name="password-success" )

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)