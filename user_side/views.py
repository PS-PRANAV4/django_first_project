
from distutils.log import error

import json



from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .decorators import guest_user
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
from coupon.models import Coupon

GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
from weasyprint import HTML

import tempfile
from django.db.models import Sum
from wallet.models import Wallet
import os
from twilio.rest import Client
from fashion_now.settings import TWILLIO_SERVICE_ID,TWILLIO_ACCOUNT_SID,TWILLIO_AUTH_TOKEN

# Create your views here.
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def first(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    return render(request,'land.html', {'products': products,'categories':categories})

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def signin(request):
    
    if not request.user.is_authenticated:
        if request.method == 'POST':
            print('posting')
            username = request.POST.get('username')
            pass5 = request.POST.get('pass')
            print(pass5) 
            user = authenticate(username=username, password=pass5)
            print(user)

            print('authenticated')
            if user is not None:
                cart_id = request.session.get('cart_id')
                try:
                    single_cart = Cart.objects.get(id=cart_id)
                    cart = Cart.objects.get(user=user)
                    pro = CartProduct.objects.filter(cart=cart)
                    carts = CartProduct.objects.filter(cart=single_cart)
                    grand_total = 0
                    print("nice")
                    prod = [x.product.id for x in carts]
                    pros = [x.product.id for x in pro]
                    setprod = set(prod)
                    setpros = set(pros)
                    inter  = list(setprod.intersection(setpros))
                    print(inter)
                    
                    print(prod,pros)
                    for ca in carts:
                        id = int(ca.product.id) 
                        print(id)
                        t = (id in inter) 
                        print(t)
                        print('welcome')
                        if t :
                            print('first')
                            item = CartProduct.objects.get(product = ca.product, cart = cart)
                            print('second')  
                            item.quantity = item.quantity + 1
                            print('third')
                            print(item.quantity)
                            print('final') 
                            item.save()
                        else:      
                            print("nice")
                            CartProduct.objects.create(cart=cart,product = ca.product,quantity = ca.quantity, total_amount = ca.total_amount)
                            grand_total = grand_total+ca.total_amount
                    cart.grand_total = cart.grand_total + grand_total
                    cart.save()
                    single_cart.delete() 
                except Exception as e:
                    print(e)

                    print('wel')
                    pass
                

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
           
        

        
        
        
        if number:
            try:
                my_user =Accounts.objects.create_user(first_name,last_name,username,email, number, pass1)
                wallet = Wallet.objects.create(user = my_user)
            
            except Exception as e:
                print(e)

                messages.error(request,"number already exist")
                n = { 'login':'SIGNUp',
                'value':3
                }
                c=a(n)
                print('mail error')
                return c
            my_user.phone_number = number
            request.session['pk'] = my_user.pk
            account_sid = TWILLIO_ACCOUNT_SID 
            auth_token = TWILLIO_AUTH_TOKEN 
            client = Client(account_sid, auth_token)

            verification = client.verify \
                     .services(TWILLIO_SERVICE_ID) \
                     .verifications \
                     .create(to= f"+91{number}", channel='sms')

            print(verification.status)
 
            if len(referal)>0:
                try:
                    user = Accounts.objects.get(referal_code = referal)
                    wallet = Wallet.objects.get(user=user)
                    wallet.amount = wallet.amount+50
                    wallet.save()
                except : 
                    messages.error(request,"user referal code doesn't exist")
                    n = { 'login':'SIGNUp',
                    'value':7
                        }
                    c=a(n)
                    print('mail error')
                    return c
            
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
    
     
    if request.method == 'POST':
        id = request.session.get('pk')
        print(id)
    
    
        user = Accounts.objects.get(id = id)
        number = user.phone_number
        codes = request.POST.get('username')
        account_sid = TWILLIO_ACCOUNT_SID
        auth_token = TWILLIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                            .services(TWILLIO_SERVICE_ID) \
                            .verification_checks \
                            .create(to=f"+91{number}", code=codes) 

        print('login')
        if verification_check.status == 'approved':
            user.is_active = True
            user.save()
            login(request,user)
            return redirect(first)
        else:
            messages.error(request,'wrong code')
            return redirect(verify_view)
    return render(request,'otp_signup.html')



def buy_now_redirect(request):
    messages.error(request,'login first to buy products')
    return redirect(signin)
     

@login_required(login_url=buy_now_redirect)
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
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
        return render(request,'checkout.html',{'profile': profile, 'cartproduct': product, 'offer':product.product.offer })  
    except Exception as e:
        print(e)
        total_offer = 0
        for pros in cartproducts:
            total_offer = total_offer + pros.product.offer*pros.quantity
            if pros.product.stock <=  0:
                messages.error(request,'please remove out of stock prouct')
                pre = pros.product.id
                return redirect(product_details,pre)
        print('her')
        return render(request,'checkout.html',{'profile': profile,"cart": cart, "cartproduc": cartproducts, 'offer':total_offer })
def guest_show(request,cart_id,total_offer):
    single_cart = Cart.objects.get(id=cart_id)
    full_cart = CartProduct.objects.filter(cart = single_cart)
    return render(request,'shop-cart.html',{'products':full_cart,'single':single_cart,'offer':total_offer})
    pass

def cart(request, us):
    print( 'hello')
    if us == 0:
        pro = request.session.get('pro')
        pros = Products.objects.get(id=pro)
        if pros.stock <=  0:
            messages.error(request,'no stock product')
            return redirect(product_details,pro)

        cart_id = request.session.get('cart_id')
        if cart_id == None:
            carts = Cart.objects.create(grand_total = pros.price,coupon_offer = 0)
            cart_id = carts.id
            request.session['cart_id'] = cart_id
        single_cart = Cart.objects.get(id=cart_id)
        print(pros.price)
        pro = CartProduct.objects.create(product=pros,quantity=1, total_amount = pros.price,cart = single_cart)
        
        full_cart = CartProduct.objects.filter(cart = single_cart)
        
        total_offer = 0
        total_amount = 0
        for product in full_cart:
            total_amount = total_amount+product.total_amount
            total_offer = total_offer+product.product.offer*product.quantity
        single_cart.grand_total = total_amount
        single_cart.save()
        return redirect(guest_show,cart_id,total_offer)
       
        
       
    myuser = Accounts.objects.get(id=us)
    single_cart = Cart.objects.get(user=myuser)
    full_cart = CartProduct.objects.filter(cart = single_cart).order_by('-id')
    total_offer = 0
    for product in full_cart:
        total_offer = total_offer+product.product.offer*product.quantity
    
    return render(request,'shop-cart.html',{'products':full_cart,'single':single_cart,'offer':total_offer})

def guest(request,id):
    
    request.session['pro'] = id
    
    
    us= 0
    
    return redirect(cart,us)


@guest_user(guest)
def addcart(request, id, us):
    product = Products.objects.get(id=id)
    if product.stock <=  0:
            messages.error(request,"product doesn't have any stock")
            return redirect(product_details,id)
    
    myuser = Accounts.objects.get(id=us)
    print(myuser)
    single_cart = Cart.objects.get(user=myuser)
    print('here')
    try:
        alcart = CartProduct.objects.get(product=product,cart=single_cart)
        alcart.quantity = alcart.quantity+1
        alcart.total_amount = alcart.quantity * alcart.product.price 
        alcart.save()
        
        print('nice')  
    except Exception as e:
        print(e)
        addcart = CartProduct.objects.create(product = product, cart = single_cart, quantity=1, total_amount= product.price )
        
    full_cart_product = CartProduct.objects.filter(cart = single_cart)
    total = 0
    total = int(total)
    for products in full_cart_product:
        total = total+(products.total_amount*products.quantity)
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
        
        order = Order.objects.create(user = user_details, delivery_address = profile, status = 'ACCEPTED', grand_total = cart_products.total_amount )
        orderprodcts = ProductOrders.objects.create(product = cart_products.product, quantity = cart_products.quantity, total_amount = cart_products.total_amount, main_order = order) 
        myproduct = Products.objects.get(id = orderprodcts.product.id)
        myproduct.stock = myproduct.stock - 1
        myproduct.save()
        cart_products.delete()
        id= order.id
        cash = request.session.get('cash')
        if cash:
            order.transaction_type = "CASH ON DELIVERY"
            request.session['cash'] = False
            order.save()
        return redirect(invoice,id)
    if user_cart.grand_total > 0:
        total_offer = 0
        order = Order.objects.create(user = user_details, delivery_address = profile, status = 'ACCEPTED', grand_total = user_cart.grand_total )
        for cart in cart_product:
            total_offer = total_offer + cart.product.offer*cart.quantity
            ProductOrders.objects.create(product = cart.product, quantity = cart.quantity, total_amount = cart.total_amount, main_order = order)
            
        if user_cart.coupon_offer > 0:
            total_offer = total_offer+user_cart.coupon_offer
            user_cart.coupon_offer = 0
            user_cart.save()            
                
        order.grand_total = order.grand_total - total_offer
        order.save()
        
        cart_product.delete()
        cash = request.session.get('cash')
        if cash:
            order.transaction_type = "CASH ON DELIVERY"
            request.session['cash'] = False
            order.save()
        user_cart.grand_total = 0
        user_cart.save()
        id = order.id
        return redirect(invoice,id)
    else:
        return redirect(first)



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
                request.session['cash'] = True
                return redirect(checkout,check,id)
            cartproduct = CartProduct.objects.filter(cart=cart)
            total_offer = 0
            for pros in cartproduct:
                total_offer = pros.product.offer*pros.quantity+total_offer
            if cart.coupon_offer > 0:
                total_offer = total_offer+cart.coupon_offer
            
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
        return JsonResponse({'data': f"{cars}", 'yes': carts.grand_total,'cartproduct':cartproduct.total_amount})

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
        return JsonResponse({'data': f"{cars}",'yes': carts.grand_total,'cartproduct':cartproduct.total_amount})



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
    html_string = render_to_string('invoice_pdf.html',{'order':order, 'products': productorder,'total':total,'offer':offer}) 
    html = HTML(string= html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0) 
        response.write(output.read())
    
    return response




@login_required(login_url=buy_now_redirect) 
def buy_now(request,id):
    product = Products.objects.get(id=id)
    if product.stock <= 0:
        messages.error(request, 'no stock')
        return redirect(product_details, id)
    cart_product = CartProduct.objects.create(product=product,quantity = 1,total_amount = product.price - product.offer)
    request.session['cart_product'] = cart_product.id
    return redirect(check_out)


def add_coupon(request):
    body = json.loads(request.body)
    check = body['coupon']
    print(check)
    try:
        print('here')
        coupon = Coupon.objects.get(number = check)
        print('here')
        val = "PASS"
        print('here')
    except:
        val = "FAILED"
    

    if val == "PASS":
        amount = coupon.coupon_amount
        user = request.user
        cart = Cart.objects.get(user=user)
        cartproduct = CartProduct.objects.filter(cart=cart)
        total_offer = 0
        for pros in cartproduct:
            total_offer = pros.product.offer*pros.quantity+total_offer
        cart.coupon_offer = amount
        cart.save()
        data = {'check': cart.coupon_offer}
        return JsonResponse(data)
    else:
        print('gone wrong')


def minus(request):
    if request.method == "POST":
        body = json.loads(request.body)
        cart_id = body['cart']
        id = body['id']
        cart = Cart.objects.get(id= cart_id)
        cartproducts = CartProduct.objects.get(cart= cart, id=id)
        if cartproducts.quantity == 1:
            messages.error(request, 'product need quantity or remove')
            data = {'quantity': cartproducts.quantity}
            return JsonResponse(data)
        cartproducts.quantity =  cartproducts.quantity - 1
        cartproducts.save()
        cartproducts.total_amount = cartproducts.quantity * cartproducts.product.price
        cartproducts.save()
        name = cartproducts.product.name
        cartproduct = CartProduct.objects.filter(cart=cart)
        total = 0
        offer = 0
        for pro in cartproduct:
            total = total + pro.quantity * pro.product.price
            offer = offer + (pro.product.offer * pro.quantity) 
        cart.grand_total = total
        cart.save()
        data = {'quantity': cartproducts.quantity,  'total': cartproducts.total_amount, 'grand_total':total, 'offer':offer } 
        
        return JsonResponse(data)

def add(request):
    if request.method == "POST":
        body = json.loads(request.body)
        cart_id = body['cart']
        id = body['id']
        cart = Cart.objects.get(id= cart_id)
        cartproducts = CartProduct.objects.get(cart= cart, id=id)
        
        cartproducts.quantity =  cartproducts.quantity + 1
        cartproducts.save()
        cartproducts.total_amount = cartproducts.quantity * cartproducts.product.price
        cartproducts.save()
        name = cartproducts.product.name
        cartproduct = CartProduct.objects.filter(cart=cart)
        total = 0
        offer = 0
        for pro in cartproduct:
            total = total + pro.quantity * pro.product.price
            offer = offer + (pro.product.offer * pro.quantity) 
        cart.grand_total = total
        cart.save() 
        data = {'quantity': cartproducts.quantity, 'total': cartproducts.total_amount , 'grand_total':total, 'offer':offer }   
        
        return JsonResponse(data)



def delet(request):
    if request.method == "POST":
        body = json.loads(request.body)
        cart_id = body['cart']
        id = body['id']
        cart = Cart.objects.get(id= cart_id)
        cartproducts = CartProduct.objects.get(cart= cart, id=id)
        cartproducts.delete()
        cartproduct = CartProduct.objects.filter(cart=cart)
        total = 0
        offer = 0
        for pro in cartproduct:
            total = total + pro.quantity * pro.product.price
            offer = offer + (pro.product.offer * pro.quantity) 
        cart.grand_total = total
        cart.save() 
        data = {'quantity': cartproducts.quantity, 'total': cartproducts.total_amount , 'grand_total':total, 'offer':offer }   
        
        return JsonResponse(data)


def cart_product_add(request):
    if request.method == "POST":
        body = json.loads(request.body)
        id = body['id']
        product = Products.objects.get(id= id)
        user = request.user
        cart = Cart.objects.get(user = user)
        try:
            cartproduct = CartProduct.objects.get(product=product, cart=cart)
            cartproduct.quantity = cartproduct.quantity + 1
            cartproduct.total_amount = cartproduct.quantity * cartproduct.product.price
            cartproduct.save()
        except Exception as e:
            print(e)
            CartProduct.objects.create(product = product, quantity = 1, total_amount = product.price, cart = cart )


        full_cart = CartProduct.objects.filter(cart = cart).aggregate(sum = Sum('total_amount'))
        print(full_cart) 
        cart.grand_total = full_cart['sum'] 
        cart.save()
        data = {'quantity': True}   
        
        return JsonResponse(data)


def shop(request):
    products = Products.objects.all()
    main_category = MainCategory.objects.all()
    category = Category.objects.all()
    return render(request,'shop_filter.html',{'products':products,'main_category':main_category, 'category':category}) 


def shop_filter(request,id):
    product = Products.objects.none()
    if id:
        main =Category.objects.filter(main_cate__id = id)
        for category in main:
            cate = category.category.all()
            product |= cate
            print(cate)
            print(product)
    main_category = MainCategory.objects.all()

    category = Category.objects.all()
    return render(request,'shop_filter.html', {'products':product,'main_category':main_category, 'category':category})

def shop_filter_cate(request,id):
    main_category = MainCategory.objects.all()
    product = Products.objects.filter(category_id = id)
    category = Category.objects.all()
    return render(request,'shop_filter.html', {'products':product,'main_category':main_category, 'category':category})

def shop_search(request):
    if request.method == 'POST':
        name = request.POST.get('content')
        request.session['name'] = name
        return redirect(shop_search)
    name = request.session.get('name')
    print(name)
    product = Products.objects.filter(name__icontains = name)
    print(product) 
    if not product:
        print('hello')
        product = Products.objects.filter(category_id__namer__icontains = name) 
    main_category = MainCategory.objects.all()
    
    category = Category.objects.all()
    return render(request,'shop_filter.html', {'products':product,'main_category':main_category, 'category':category})
    
 

 
def login_otp(request):
    if request.method == "POST":
        number = request.POST.get('username')
        try :
            user = Accounts.objects.get(phone_number = number)
        except: 
            messages.error(request, "phone number doesn't exist")
            return redirect(login_otp)
        request.session['id'] = user.id
        print(number) 
        account_sid = TWILLIO_ACCOUNT_SID
        auth_token = TWILLIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        verification = client.verify \
                     .services(TWILLIO_SERVICE_ID) \
                     .verifications \
                     .create(to= f"+91{number}", channel='sms')

        print(verification.status)
        return redirect(otp_veify)
    return render(request, 'otp_login.html')    
 

def otp_veify(request):
    id = request.session.get('id')
    print(id)
    
    
    user = Accounts.objects.get(id = id)
    number = user.phone_number
    print(number)  
    if request.method == 'POST':
        codes = request.POST.get('username')
        account_sid = TWILLIO_ACCOUNT_SID
        auth_token = TWILLIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        verification_check = client.verify \
                            .services(TWILLIO_SERVICE_ID) \
                            .verification_checks \
                            .create(to=f"+91{number}", code=codes)

        print('login')
        if verification_check.status == 'approved':
            login(request,user)
            return redirect(first)
    return render(request, 'verifi.html') 




def guest_check(request):
    messages.error(request,'login first to buy products')
    return redirect(signin)
 

def best_deals(request):
    product = Products.objects.exclude(offer = 0)
    main_category = MainCategory.objects.all()
    category = Category.objects.all()
    return render(request,'shop_filter.html', {'products':product,'main_category':main_category, 'category':category})

def pay_wallet(request,check):
    user  = request.user
    cart = Cart.objects.get(user = user)
    wallet = Wallet.objects.get(user = user)
    if wallet.amount >= cart.grand_total:
        wallet.amount = wallet.amount - cart.grand_total
        wallet.save()
        return redirect(checkout,check,user.id)

    else:
        messages.error(request,'not enough amount in wallet')
        return redirect(purchase,check,user.id)

