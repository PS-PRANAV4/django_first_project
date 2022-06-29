import email
from django.contrib import messages
from django.shortcuts import redirect, render
from admins.models import Accounts
from cart_orders.models import Cart,CartProduct,Order,ProductOrders
from wallet.models import Wallet
from .models import Profile
from django.contrib.auth.hashers import check_password
import os

# Create your views here.

def user_profile(request,id):
    user = Accounts.objects.get(id = id )
    count = Order.objects.filter(user = user ).count
    cart = Cart.objects.get(user = user)
    product_count = CartProduct.objects.filter(cart = cart).count()
    profile_count  = Profile.objects.filter(accounts=user).count()
    wallet = Wallet.objects.get(user = user)
    return render(request,'user_profile/user_details.html',
    {"total_orders":count,'total_products':product_count,"profile_count": profile_count,"wallet":wallet})


def user_address(request,id):
    user = Accounts.objects.get(id=id)
    address = Profile.objects.filter(accounts=user)
    return render(request,'user_profile/user_address.html',{'address':address})



def add_address(request,id):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    country_name = request.POST.get('country_name')
    address = request.POST.get('address')
    town_city = request.POST.get('town_city')
    state = request.POST.get('state')
    post_code = request.POST.get('post_code')
    phone_number = request.POST.get('phone_number')
    email = request.POST.get('email')
    notes = request.POST.get('notes')
    user = Accounts.objects.get(id=id)
    
    new_address = Profile.objects.create(first_name = first_name, last_name = last_name,
     country_name = country_name, address = address,
     town_city = town_city, state = state, post_code = post_code,
     phone_number = phone_number, email = email, notes = notes,accounts = user)
    return redirect(user_address,id)

def orders(request,id):
    user = Accounts.objects.get(id=id)
    order = Order.objects.filter(user = user)
    return render(request,'user_profile/order.html',{'orders':order})


def cancel(request,id):
    order = Order.objects.get(id=id)
    order.status = "CANCEL"
    order.save()
    user = order.user
    id = user.id
    return redirect(orders,id)

def account(request,id):
    user = Accounts.objects.get(id=id)
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        a = user.check_password(old_password)
        print(len(password),password)
        if a:
            user.set_password(password)
            user.save()
            print(user.check_password(old_password))
        elif password == confirm_password:
            print('reached2')
            messages.error(request, "password doesn't match")
        else:
            print('match')
            messages.error(request,"paswords doesn't match")
    return render(request,'user_profile/account_settings.html')


def pic(request):
    if request.method == "POST":
        user = request.user
        print(user)
        pro = Accounts.objects.get(email =user)
        if len(request.FILES)!=0:
            print('entered1')
            if len(pro.profile_pic)>0:
                print('entered2')
                os.remove(pro.profile_pic.path)
                print('removed')
            pro.profile_pic = request.FILES['pic']
            pro.save()
            print('saved')
        return redirect(user_profile,pro.id)
