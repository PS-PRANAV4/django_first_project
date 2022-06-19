
import email
import json
from turtle import home
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from requests import request
from admins.models import Accounts
from admins.views import product
from product.models import MainCategory, Products,Category
from .utils import send_sms
from codes.forms import CodeForm
from django.contrib.auth.forms import AuthenticationForm
from cart_orders.models import Cart,CartProduct, Order, ProductOrders
from profiles.models import Profile
from django.http import JsonResponse
import datetime
from django.template.loader import render_to_string
import os

GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
from weasyprint import HTML

import tempfile
from django.db.models import Sum
from wallet.models import Wallet

# Create your views here.
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def first(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    return render(request,'land.html', {'products': products,'categories':categories})

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def signin(request):
    form = AuthenticationForm()
    if not request.user.is_authenticated:
        if request.method == 'POST':
            print('posting')
            username = request.POST.get('username')
            pass5 = request.POST.get('pass')
            user = authenticate(username=username, password=pass5)
            print('authenticated')
            if user is not None:
                login(request,user)
                return redirect(first)
                # request.session['pk'] = user.pk
                # return redirect(verify_view)
            else:
                print('signin render')
                messages.error(request,'enter valid username and password')
                return render(request,'log.html')
        else:
            print('signin page')
            return render(request,'log.html')
    else:
        # products = product.objects.all()
        print('signin redirect page2')  
        return redirect(first)   

def signup(request):
    context = {}
    def a(context):
        return render(request,'signup.html',context)

    if request.method == "POST" :
        username = request.POST.get("username")
        number = request.POST.get('number')
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2  = request.POST.get("pass2")
        referal = request.POST.get("referal")
        print(len(username))
        if pass1 != pass2:
            messages.error(request,"password didn't match" )
            n = { 'login':'SIGNUp',
                'value':4
            }
            c=a(n)
            print('pass error')
            return c
            
        elif len(first_name) == 0:
            messages.error(request,'enter valid first name')
            n = { 'login':'SIGNUp',
                'value':1
            }
            c=a(n)
            print("name can't be blank")
            return c

        elif len(last_name) == 0:
            messages.error(request,'please input last_name')
            n = { 'login':'SIGNUp',
                'value':6
            }
            c=a(n)
            print('mail error')
            return c


        elif len(username) == 0:
            print('user error')
            messages.error(request,'enter valid username ')
            n = { 'login':'SIGNUp',
                'value':2
            }
            c=a(n)
            return c
    	    

        
        elif len(email) == 0:
            messages.error(request,'enter valid  email')
            n = { 'login':'SIGNUp',
                'value':3
            }
            c=a(n)
            print('mail error')
            return c

        elif len(number) == 0:
            messages.error(request,'please input phone number')
            n = { 'login':'SIGNUp',
                'value':5
            }
            c=a(n)
            print('mail error')
            return c
        
            

        elif len(pass1) == 0:
            messages.error(request,'please input password')
            n = { 'login':'SIGNUp',
                'value':4
            }
            c=a(n)
            print('mail error')
            return c
           
        

        

        my_user =Accounts.objects.create_user(first_name,last_name,username,email,pass1)
        wallet = Wallet.objects.create(user = my_user)
        if len(referal)>0:
            user = Accounts.objects.get(referal_code = referal)
            wallet = Wallet.objects.get(user=user)
            wallet.amount = wallet.amount+50
            wallet.save()
        if number:
            my_user.phone_number = number
            request.session['pk'] = my_user.pk
            
        print('user created')
        my_user.is_active = False
        my_user.save()
        print(my_user.id)
        cart = Cart.objects.create(user = my_user)
        print('user created')
        messages.success(request, "u succesfully created a user now verify the number")
        
        return redirect(verify_view)
    else:
        n = { 'login':'SIGNUp',
                'value':0
            }
        c=a(n)
        return c
    

    
@login_required(login_url=first)    
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def signout(request):
    logout(request)
    return redirect(first)

def profile(request):
    if request.user.is_authenticated:
        
        return render(request,'profile.html')
        
    else:
        messages.error(request,'please login first ')
        return redirect(signin)


# def cart(request):
#     if request.user.is_authenticated:
        
#         return render(request,'cart.html')
        
#     else:
#         messages.error(request,'please login first ')
#         return redirect(signin)
    


def product_details(request,id):

    pro = Products.objects.get(id=id)
    return render(request,'product_person.html',{'pro': pro})


def verify_view(request):
    form = CodeForm(request.POST or None)
    pk = request.session.get('pk')
    if pk:
        user = Accounts.objects.get(pk=pk)
        code = user.code
        code_user = f"{user.username}: {user.code}"
        if not request.POST:
            print(code_user)
            send_sms(code_user, user.phone_number)
        if form.is_valid():
            num = form.cleaned_data.get('number')

            if str(code) == num:
                code.save()
                messages.success(request,'phone no verified')
                user.is_active = True
                user.save()
                return redirect(signin)
            else:
                messages.error(request, 'wrong otp account not created')
                user.delete()
                return redirect(signin)
    return render(request, 'verify.html', {'form':form})



def check_out(request,id = 0):
    
    try:
        cart_product = request.session.get('cart_product')
        print(cart_product)
        print('here')
        
        
        try:
            profile = Profile.objects.filter(accounts = request.user.id)
            cart = Cart.objects.get(user = id)
            cartproducts = CartProduct.objects.filter(cart = cart)
            
        except:
            pass
    except:
        print('no-way')
        profile = Profile.objects.filter(accounts = id)
        cart = Cart.objects.get(user = id)
        cartproducts = CartProduct.objects.filter(cart = cart)
    if cart_product == None:
        print('no-way')
        profile = Profile.objects.filter(accounts = id)
        cart = Cart.objects.get(user = id)
        cartproducts = CartProduct.objects.filter(cart = cart)
    if request.method == "POST":
        check  = request.POST.get('check')
        print(check)
        
        if check == '0' :
            first_name  = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            town = request.POST.get('town')
            state = request.POST.get('state')
            phone = request.POST.get('phone')
            pin = request.POST.get('pin')
            email = request.POST.get('email')
            notes = request.POST.get('note')
            address = address1+' ' +address2
            user = Accounts.objects.get(id=id)
            new_profile = Profile.objects.create(first_name = first_name, last_name = last_name, country_name = country, address = address, town_city = town, state = state , phone_number = phone, post_code = pin, email = email, notes = notes,accounts = user)
            check1 = new_profile.id
        else:
            check2 = Profile.objects.get(id = check)
            check1 = check2.id
        
        if check1 != None:
            return redirect(purchase,check1,id)


    if id > 0:
       
        try:
            print('hereeeeeee')    
            del request.session['cart_product']
        except:
            print('hesssssss')
            pass


    try:
        cart_product = request.session.get('cart_product')
        product = CartProduct.objects.get(id=cart_product)
        print('hereornot')
        return render(request,'checkout.html',{'profile': profile, 'cartproduct': product, 'offer':product.total_amount })
    except:
        total_offer = 0
        for pros in cartproducts:
            total_offer = total_offer + pros.product.offer*pros.quantity
        print('her')
        return render(request,'checkout.html',{'profile': profile,"cart": cart, "cartproduc": cartproducts, 'offer':total_offer })

def cart(request, us):
    myuser = Accounts.objects.get(id=us)
    single_cart = Cart.objects.get(user=myuser)
    full_cart = CartProduct.objects.filter(cart = single_cart)
    total_offer = 0
    for product in full_cart:
        total_offer = total_offer+product.product.offer*product.quantity
    
    return render(request,'shopping-cart.html',{'products':full_cart,'single':single_cart,'offer':total_offer})

def addcart(request, id, us):
    product = Products.objects.get(id=id)
    myuser = Accounts.objects.get(id=us)
    print(myuser)
    single_cart = Cart.objects.get(user=myuser)
    addcart = CartProduct.objects.create(product = product, cart = single_cart, quantity=1, total_amount= product.price )
    full_cart_product = CartProduct.objects.filter(cart = single_cart)
    total = 0
    total = int(total)
    for products in full_cart_product:
        total = total+products.total_amount
    single_cart.grand_total = total
    single_cart.save()
    return redirect(cart,us)

def delete_cart(request,id, us):
    single_cart = Cart.objects.get(user = us)
    product = CartProduct.objects.get(id=id)
    single_cart.grand_total = single_cart.grand_total - product.product.price
    single_cart.save()
    CartProduct.objects.get(id=id).delete()
    full_cart_product = CartProduct.objects.filter(cart = single_cart)
    total = 0
    total = int(total)
    for products in full_cart_product:
        total = total+products.total_amount
    single_cart.grand_total = total
    single_cart.save()
    print()
    return redirect(cart,us)

def checkout(request,check, id):
    profile = Profile.objects.get(id=check)
    user_email = profile.accounts
    user_details = Accounts.objects.get(email=user_email)
    
    user_cart = Cart.objects.get(user = user_details)
    cart_product = CartProduct.objects.filter(cart = user_cart)
    
    cart_id = request.session.get('cart_product')
    if cart_id:
        cart_products = CartProduct.objects.get(id = cart_id)
        order = Order.objects.create(user = user_details, delivery_address = profile, status = 'PENDING', grand_total = cart_products.total_amount )
        cart_products.delete()
        id= order.id
        return redirect(invoice,id)
    if user_cart.grand_total > 0:
        total_offer = 0
        order = Order.objects.create(user = user_details, delivery_address = profile, status = 'PENDING', grand_total = user_cart.grand_total )
        for cart in cart_product:
            total_offer = total_offer + cart.product.offer*cart.quantity
            ProductOrders.objects.create(product = cart.product, quantity = cart.quantity, total_amount = cart.total_amount, main_order = order)
        order.grand_total = order.grand_total - total_offer
        order.save()
        cart_product.delete()
        user_cart.grand_total = 0
        user_cart.save()
        id = order.id
        return redirect(invoice,id)
    else:
        return redirect(first)


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def purchase(request,check,id):
    try:
            print('now')
            cart_product = request.session.get('cart_product')
            print(cart_product)
            
            cart = CartProduct.objects.get(id=cart_product)
            if request.method == "POST":
                return redirect(checkout,check,id)
            return render(request,'purchase.html',{'check':check, 'id':id,'carts': cart, 'offer':cart.product.offer} )
    except:
        cart = Cart.objects.get(user = id)
        if cart.grand_total>0:
        
            if request.method == "POST":
                return redirect(checkout,check,id)
            cartproduct = CartProduct.objects.filter(cart=cart)
            total_offer = 0
            for pros in cartproduct:
                total_offer = pros.product.offer*pros.quantity+total_offer
            
            
                print('nowss')
                return render(request,'purchase.html',{'check':check, 'id':id,'cart': cart, 'offer':total_offer} )
        else:
            return redirect(first)

 
def add_quantity(request, us, op, pro):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' :
        pass    
    if op == 'plus':
        carts = Cart.objects.get(user=us)
        cartproduct = CartProduct.objects.get(product=pro, cart = carts)
        product = Products.objects.get(id = pro)
        cartproduct.quantity = cartproduct.quantity+1
        cartproduct.total_amount = product.price*cartproduct.quantity
        cartproduct.save()
        full_cart_product = CartProduct.objects.filter(cart = carts)
        total = 0
        total = int(total)
        for products in full_cart_product:
            total = total+products.total_amount
        carts.grand_total = total
        carts.save()
        
    else:
        carts = Cart.objects.get(user=us)
        cartproduct = CartProduct.objects.get(product=pro, cart = carts)
        product = Products.objects.get(id = pro)
        cartproduct.quantity = cartproduct.quantity-1
        cartproduct.total_amount = product.price*cartproduct.quantity
        cartproduct.save()
        full_cart_product = CartProduct.objects.filter(cart = carts)
        total = 0
        total = int(total)
        for products in full_cart_product:
            total = total+products.total_amount
        carts.grand_total = total
        carts.save()

    return redirect(cart, us)



# def hello(request):
#     if request.method == "POST":
#         number = json.loads(request.body)['number']
#         return JsonResponse({'data': f"4"})
#     number = 5
#     return JsonResponse({'number':number})
#     # return redirect(first)

def hello(request):
    if request.method == "POST":
        us = request.user
        print(us)
        pro = json.loads(request.body)['number']
        carts = Cart.objects.get(user=us)
        cartproduct = CartProduct.objects.get(product=pro, cart = carts)
        product = Products.objects.get(id = pro)
        cartproduct.quantity = cartproduct.quantity+1
        cartproduct.total_amount = product.price*cartproduct.quantity
        cartproduct.save()
        full_cart_product = CartProduct.objects.filter(cart = carts)
        total = 0
        total = int(total)
        for products in full_cart_product:
            total = total+products.total_amount
        carts.grand_total = total
        carts.save()
        cars = cartproduct.quantity
        return JsonResponse({'data': f"{cars}", 'yes': carts.grand_total})

def hel(request):
    if request.method == "POST":
        us = request.user
        pro = json.loads(request.body)['number']
        carts = Cart.objects.get(user=us)
        cartproduct = CartProduct.objects.get(product=pro, cart = carts)
        product = Products.objects.get(id = pro)
        cartproduct.quantity = cartproduct.quantity-1
        cartproduct.total_amount = product.price*cartproduct.quantity
        cartproduct.save()
        full_cart_product = CartProduct.objects.filter(cart = carts)
        total = 0
        total = int(total)
        for products in full_cart_product:
            total = total+products.total_amount
        carts.grand_total = total
        carts.save()
        cars = cartproduct.quantity
        return JsonResponse({'data': f"{cars}"})



def invoice(request,id):
    
    order = Order.objects.get(id=id)
    productorder = ProductOrders.objects.filter(main_order = order)
    total = 0
    offer = 0
    for product in productorder:
        total = total + product.total_amount
        offer = offer + product.product.offer 
    print('jjjjjjjjjjjjjjjjjjjjjjj')
    return render(request,'invoice.html',{'order':order, 'products': productorder,'total':total,'offer':offer})


def paypal(request):
    body = json.loads(request.body)
    check = body['ad']
    id = body['id']
    status = body['status']
    data = {'check': check, 'id': id}
    if status == 'COMPLETED':
        return JsonResponse(data)
    
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def filter(request):
    main = request.GET.get('main')
    product = Products.objects.none()
    if main:
        main =Category.objects.filter(main_cate__id = main)
        for category in main:
            cate = category.category.all()
            product |= cate
            print(cate)
            print(product)
            
                
                
                
        
    return render(request, 'filter.html',{'products':product})


def invoice_pdf(request,id):
    order = Order.objects.get(id=id)
    productorder = ProductOrders.objects.filter(main_order = order)
    total = 0
    offer = 0
    for product in productorder:
        total = total + product.total_amount
        offer = offer + product.product.offer
    
    response = HttpResponse(content_type = 'application/pdf')
    
    
    response['Content-Disposition'] = 'inline; attachment; filename = daily report'+ \
        str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = 'binary'
    html_string = render_to_string('invoice.html',{'order':order, 'products': productorder,'total':total,'offer':offer})
    html = HTML(string= html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0) 
        response.write(output.read())
    
    return response


def buy_now(request,id):
    product = Products.objects.get(id=id)
    cart_product = CartProduct.objects.create(product=product,quantity = 1,total_amount = product.price - product.offer)
    request.session['cart_product'] = cart_product.id
    return redirect(check_out)