from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from django.views import View
from django.urls import reverse_lazy
from .models import Product, UserProfile, Cart
from . forms import CustomerRegistrationForm, CustomerProfileForm, PasswordChangingForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'app/home.html')

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def category_view(request, val):
    products = Product.objects.filter(category=val)
    title = Product.objects.filter(category=products[0].category).values('title')

    return render (request, 'app/category.html', locals())

class Product_detail_view(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render (request, 'app/product_detail.html', locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, 'app/CustomerRegistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation, You have register successfully.")

        else:
            messages.error(request, "Invalid Input Data..! Please try again.")

        return render(request, 'app/CustomerRegistration.html', locals())
    

def login_view(request):
    if request.method == "POST":
        un = request.POST.get('uname')
        pw = request.POST.get('passw')
        user = authenticate(username=un, password=pw)
        print('user----', user)

        if user is not None:
            login(request, user)
           
            return redirect('home')
    return render(request, 'app/login.html')




class Password_Change_View(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password-success')

def password_success(request):
    return render(request, 'app/password_change_success.html')



def logout_view(request):
    logout(request)
    return redirect ('login')

def profile_view(request):
    #obj = UserProfile.objects.get(user=request.user)
    # form = CustomerProfileForm(instance=obj)
    form = CustomerProfileForm()
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            pincode = form.cleaned_data['pincode']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            country = form.cleaned_data['country']
            reg = UserProfile(user=user, name=name, locality=locality, city=city,mobile=mobile, pincode=pincode, state=state, country=country)
            reg.save()
            messages.success(request, "Your profile has been saved successfully!")
    
    return render (request, 'app/profile.html', locals())


def address_view(request):
    # print("----",UserProfile.city)
    add = UserProfile.objects.filter(user = request.user)
    return render(request, 'app/address.html', locals())


class UpdateAddressView(View):
    def get(self, request, pk):
        obj = UserProfile.objects.get(pk = pk)
        form = CustomerProfileForm(instance = obj)
        return render(request, 'app/updateaddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = UserProfile.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.pincode = form.cleaned_data['pincode']
            add.country = form.cleaned_data['country']
            add.save()
            messages.success(request, "Address updated successfully..!!")
            return redirect ('address')
        return render(request, 'app/updateaddress.html', locals())
    
    
    
    
def delete_view(request, pk):
    obj = UserProfile.objects.get(pk=pk)
    obj.delete()
    return redirect('address')
    # return render( request, 'app/updateaddress.html', locals())


#cart
@login_required()
def add_to_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            if (Cart.objects.filter(user = request.user, product=product)):
                print('hi')
                return JsonResponse({'status':'Product already in Cart.'})
            else:
                product = Product.objects.get(pk=product_id)
                Cart(user=request.user, product=product).save()
                return redirect('show-cart')

def show_cart(request):
    products = Cart.objects.filter(user=request.user)
    count = len(products)
    amount = 0
    for p in products:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    total_amount = amount + 40

    return render(request, 'app/show_cart.html', locals())

def remove_cart(request, pk):
    obj = Cart.objects.get(product_id=pk)
    obj.delete()
    return redirect("show-cart")


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print("n:",prod_id)
        data = {

        }
        return JsonResponse(data)


class Checkout_view(View):
    def get(self, request):
        user = request.user
        add = UserProfile.objects.filter(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        total_amount = amount + 40
        return render (request, 'app/checkout.html', locals())
    

def search(request):
    query = request.GET.get('query')
    products = Product.objects.filter(title__icontains=query)
    return render(request, 'app/search.html', {'products': products})


    



