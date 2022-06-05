from email.policy import default
from multiprocessing import context
from tokenize import Number
from unicodedata import name
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Accounts,Manager
from product.models import Category,Products
from cart_orders.models import Cart,CartProduct,Order,ProductOrders
import os
# Create your views here.
 


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            print('posting')
            username = request.POST.get('username')
            pass5 = request.POST.get('password')
            if not (len(username) > 0 or len(pass5)>0):
                print('hello')
                messages.error(request,'please fill')
                return redirect(signin)
            user = authenticate(username=username, password=pass5)
            
                
            
            if user is not None:
                if not user.is_superadmin:
                    messages.error(request,'you are not super admin')
                    return redirect(signin)
                login(request, user)
                print('signin redirect page')
                return redirect(main)
        
            else:
                print('signin render')
                messages.error(request,'enter valid username and password')
                return redirect(signin)
        else:
            print('signin page')
            return render(request,'admin_T/login.html')
    else:
        # products = product.objects.all()
        print('signin redirect page2')  
        return redirect(main)

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def main(request):
    orders = Order.objects.all().order_by('id')
    return render(request, 'admin_T/first.html',{'orders':orders} )   


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def account(request):
    print('hello')
    if request.method == 'POST':
        search = request.POST.get('search')
        context = Accounts.objects.filter(username__icontains=search, is_admin=False)
        request.session['name'] = search
        return redirect(account)
    

    search = request.session.get('name', False)
    context = Accounts.objects.filter(username__icontains=search, is_admin=False)
    if search :
        request.session['name'] = False
        return render(request,'admin_T/accounts.html', {'full_user':context})
        
    else:
        full_users = Accounts.objects.filter(is_admin=False).order_by('id')
        
        
        return render(request,'admin_T/accounts.html', {'full_user':full_users})
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        details = request.POST.get('details')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        categ = request.POST.get('categ')
        if len(request.FILES)!=0:
            try:
                product = Products.objects.create(name = name, details = details, price = price, stock = stock, category_id_id = categ, offer = 0)
            except ValueError:
                    messages.error(request,'please check the values u inserted')
                    return redirect(add_product)
            
            product.image_product = request.FILES['image']
            product.save()
        else:
            messages.error(request,'please input the photo')
            return redirect(add_product)
            
    cate =Category.objects.all()
    return render(request, 'admin_T/add-product.html',{'cate':cate})

@login_required(login_url=signin)
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def edit_product(request,id):
    if request.method == 'POST':
        pro = Products.objects.get(id=id)
        name = request.POST.get('name')
        details = request.POST.get('details')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        categ = request.POST.get('cate')
        print(categ)
        
        
        if name:
            pro.name=name
        if name:
            pro.details=details
        if price:
            pro.price=price
        if stock:
            pro.stock=stock
        if categ:
            print('here')
            pro.category_id_id=categ
        pro.save()
           
        if len(request.FILES)!=0:
            print('entered1')
            if len(pro.image_product)>0:
                print('entered2')
                os.remove(pro.image_product.path)
                print('removed')
            pro.image_product = request.FILES['image']
            pro.save()
            print('saved')
            return redirect(edit_product)
            


        

    product = Products.objects.get(id=id)
    cate =Category.objects.all()

    return render(request, 'admin_T/edit-product.html', {'product': product, 'cate':cate})

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def product(request):
    pro = Products.objects.all()
    cats = Category.objects.all()
    

    return render(request, 'admin_T/products.html',{'pro':pro, 'cats':cats})

# @login_required(login_url=signin)
# def add_users(request):
#     return render(request, 'admin_T/add_users.html')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def block(request,id):
    user_d = Accounts.objects.get(id=id)
    if user_d.is_active:
        user_d.is_active=False
    else:
        user_d.is_active=True
    print(user_d)
    print(user_d.is_active)
    user_d.save()
    return redirect(account)
    
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def signout(request):
    logout(request)
    return redirect(signin)

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def delete_product(request,id):
    Products.objects.get(id=id).delete()
    return redirect(product)

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        details = request.POST.get('details')
        if category_name and details:
            Category.objects.create(namer=category_name, description = details)
        else:
            messages.error('please fill the form')
        return redirect(add_category)

    return render(request, 'admin_T/add_category.html')


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@login_required(login_url=signin)
def delete_category(request, id):
    try:
        Category.objects.get(id=id).delete()
    except:
        messages.error( request, "can't delete the category")
    return redirect(product)


def change(request,id,status = None):
    order = Order.objects.get(id=id)


    if status == "cancel":
        order.status = "CANCEL"
    elif order.status == "PENDING":
        order.status = "DELIVERED"
    else:
        order.status = "PENDING"
    order.save()
    return redirect(main)
    