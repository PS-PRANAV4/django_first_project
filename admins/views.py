from datetime import datetime

from itertools import count

from pickle import TRUE


from unicodedata import category, name
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from requests import delete
from .models import Accounts,Manager
from product.models import Category,Products,MainCategory
from cart_orders.models import Cart,CartProduct,Order,ProductOrders
import os
from django.core.paginator import Paginator
from django.db.models import Count,Avg,Sum
from django.db.models.functions import TruncMonth,TruncDate,TruncWeek,TruncDay, ExtractWeekDay , TruncYear
import datetime
from django.template.loader import render_to_string
import os

GTK_FOLDER = r'C:\Program Files\GTK3-Runtime Win64\bin'
os.environ['PATH'] = GTK_FOLDER + os.pathsep + os.environ.get('PATH', '')
from weasyprint import HTML

import tempfile
from django.db.models import Sum
from.decorators import admin_Login
from notification.models import Notification
import json
from django.http import JsonResponse
from .error import OfferAmountError

 


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
@admin_Login(signin)
def main(request):
    c= Order.objects.annotate(count=ExtractWeekDay('order_date')).values('count').annotate(number=Count('id')).values('count', 'number')
    wee = []
    z=0
    g = 0
    print("sssssssssssssss")
    print(c)
    for x in range(1,8):
        j = 0
        for week in c:
            # print(week)
            if week["count"] == x:
                wee.append(week['number'])
                # print(wee[z])
                z = z+1
                j=1
        if j == 0:
            wee.append(g)
    
                 
    noti = Notification.objects.all()
    now = datetime.datetime.now() 
    year = int(now.year) 
    month = int(now.month)
    date = int(now.day) 
    print('gggggggggggg')
    print(date)

    total_order = Order.objects.filter(order_date__year = year, order_date__month = month,order_date__day = date ).count()
    total_revenu = Order.objects.filter(order_date__year = year, order_date__month = month,order_date__day = date).aggregate(sum = Sum('grand_total'))
    
    print(datetime.date.today()) 
    print(total_order)
    print(wee)            
                
    return render(request, 'admin_T/first.html',{"week":wee, 'notification':noti, 'order_today': total_order, 'revenue_today':total_revenu})   


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
def account(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        context = Accounts.objects.filter(username__icontains=search, is_admin=False)
        request.session['name'] = search
        return redirect(account)
    

    search = request.session.get('name', False)
    context = Accounts.objects.filter(username__icontains=search, is_admin=False)
    if search :
        request.session['name'] = False
        look = 0
        return render(request,'admin_T/accounts.html', {'full_user':context,'search':look})
        
    else:

        full_users = Accounts.objects.filter(is_admin=False).order_by('id')
        page_number = request.GET.get('page')
        p = Paginator(full_users,2)
        
        try:
            users = p.page(page_number)
        except:
            users = p.page(1)
        look = 1
        return render(request,'admin_T/accounts.html', {'full_user':users,'search':look})
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
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
            except IntegrityError:
                    messages.error(request,"name is duplicate can't insert")
                    return redirect(add_product)
            
            product.image_product = request.FILES['image']
            product.image_product4 = request.FILES['image1']
            product.image_product5 = request.FILES['image2']
            product.save()
            messages.error(request,'PRODUCT SAVED')
        else:
            messages.error(request,'please input the photo')
            return redirect(add_product)
            
    cate =Category.objects.all()
    main = MainCategory.objects.all()
    return render(request, 'admin_T/add-product.html',{'cate':cate,'main':main})

@admin_Login(signin)
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
            try:
                image_product = request.FILES['image']
                if len(image_product) > 0:
                    if len(pro.image_product)>0:
                        print('entered2')
                        os.remove(pro.image_product.path)
                        print('removed')
                    pro.image_product = request.FILES['image']    
            except: 
                pass
                print('yes')
                
            print('entered1')
                
            
            try:
                image_product2 = request.FILES['image2']
                if len(pro.image_product4)>0:
                    print('entered2')
                    os.remove(pro.image_product4.path)
                    print('removed')
                pro.image_product4 = request.FILES['image2']
            except:
                pass
                

            try:    
                image_product3 = request.FILES['image3']
                if len(pro.image_product5)>0:
                    print('entered2')
                    os.remove(pro.image_product5.path)
                    print('removed')
                pro.image_product5 = request.FILES['image3']
            except:
                pass
            pro.save()
        messages.error(request,'PRODUCT EDITED SUCCESFULLY')
        return redirect(product)
            


        

    products = Products.objects.get(id=id)
    cate =Category.objects.all()
    main = MainCategory.objects.all()

    return render(request, 'admin_T/edit-product.html', {'product': products, 'cate':cate,'main':main})

@admin_Login(signin)
def product(request):
    pro = Products.objects.all().order_by('-id')
    cats = Category.objects.all()
    product = Paginator(pro,5) 
    product_number = request.GET.get('pages')
       
    try:
        pro = product.page(product_number)
           
    except:
        pro = product.page(1)
        
    com = 1
    return render(request, 'admin_T/products.html',{'pro':pro, 'cats':cats, "search":com})

# @login_required(login_url=signin)
# def add_users(request):
#     return render(request, 'admin_T/add_users.html')

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
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
@admin_Login(signin)
def signout(request):
    logout(request)
    return redirect(signin)

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
def delete_product(request,id):
    Products.objects.get(id=id).delete()
    return redirect(product)

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
def add_category(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        category_name = body['name']        
        main = body['main_ca']
        details = body['det']
        
        if category_name and details and main:
            mains = MainCategory.objects.get(id= main)
            print('hai')
            try:
                Category.objects.create(namer=category_name, description = details,main_cate = mains)
            except IntegrityError:
                
                data = {'message': 'NAME ALREADY EXIST'}
                return JsonResponse(data)
        else:
            data = {'message': "PLEASE FILL THE FORM"}
            return JsonResponse(data) 


        data = {'message': "CATEGORY ADDED"} 
        return JsonResponse(data)
    ma = MainCategory.objects.all()
    return render(request, 'admin_T/add_category.html',{'main':ma})


@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@admin_Login(signin)
def delete_category(request, id):
    try:
        Category.objects.get(id=id).delete()
    except:
        messages.error( request, "can't delete the category")
    return redirect(category_managment) 

@admin_Login(signin)
def change(request,id,status = None):
    order = Order.objects.get(id=id)


    if status == "cancel":
        order.status = "CANCEL"
    elif order.status == "PENDING":
        order.status = "DELIVERED"
    elif order.status == "ACCEPTED":
        order.status = "SHIPPED"
    elif order.status == "SHIPPED":
        order.status = "OUT FOR DELIVERY"
    elif order.status == "OUT FOR DELIVERY":
        order.status = "DELIVERED"

    else:
        order.status = "PENDING"
    order.save()
    return redirect(orders_list)

@admin_Login(signin)
def orders_list(request):
    orders = Order.objects.all().order_by('-id')
    order = Paginator(orders,7)
    product_number = request.GET.get('pages')
    try:
        order_page = order.page(product_number)
    except:
        order_page = order.page(1) 
    return render(request, 'admin_T/orders.html',{'orders':order_page} )

@admin_Login(signin)
def daily_report(request):
    if request.method == "POST":
        frm = request.POST.get('from')
        to = request.POST.get("to")
        print(frm,to)
        fro = frm.split('-')
        too = to.split('-')
        print(fro[0])
        
        try:
            res = [int(item) for item in fro]
            pos = [int(item) for item in too]
        except:
            pos = []
            res = []
        request.session['res'] = res
        request.session['pos'] = pos
        return redirect(daily_report) 
    
    pos = request.session.get('pos')
    res = request.session.get('res')
    try:
        del request.session['pos']
        del request.session['res']
    except:
        pass
    try:
        report = Order.objects.filter(status= "DELIVERED", order_date__gte=datetime.date(res[0],res[1],res[2]), order_date__lte=datetime.date(pos[0],pos[1],pos[2])).annotate(day=TruncDate('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total')).order_by('-day').distinct()
    except:
        report = Order.objects.filter(order_date__gte=datetime.date(2022, 6, 1), order_date__lte=datetime.date(2022, 6, 30)).annotate(day=TruncDate('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total')).order_by('-day').distinct()
    return render(request,'admin_T/daily_report.html',{'report': report})

@admin_Login(signin)
def monthly_report(request):
    if request.method == "POST":
        frm = request.POST.get('from')
        to = request.POST.get('to')

        print(frm)
        fro = frm.split('-')
        too = to.split('-')
        try:
            res = [int(item) for item in fro]
            pos = [int(item) for item in too]
        except:
            pos = []
            res = []
        request.session['from'] = res
        request.session['to'] = pos
        return redirect(monthly_report)

    
    pos = request.session.get('from')
    res = request.session.get('to')
    print(pos)
    try:
        del request.session['from']
        del request.session['to']
    except:
        pass
    try:
        report = Order.objects.filter(status= "DELIVERED", order_date__year__gte=pos[0], order_date__month__gte=pos[1], order_date__year__lte=res[0], order_date__month__lte=res[1]).annotate(day=TruncMonth('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))
        print(report)
    except Exception as e:
        print(e)
        
        report = Order.objects.filter(status='DELIVERED').annotate(day=TruncMonth('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))

    
    return render(request,'admin_T/monthly_report.html',{'report': report})
   

@admin_Login(signin)
def yearly_report(request):
    
    report = Order.objects.filter(status='DELIVERED').annotate(weekly=TruncYear('order_date')).values('weekly').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))
    
    return render(request,'admin_T/weekly_report.html',{'report': report})

@admin_Login(signin)
def daily_pdf(request):
    report = Order.objects.filter(status='DELIVERED').annotate(day=TruncDate('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))
    
    response = HttpResponse(content_type = 'application/pdf')
    
    
    response['Content-Disposition'] = 'inline; attachment; filename = daily report'+ \
        str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = 'binary'
    html_string = render_to_string('admin_T/pdf_output.html',{'order': report})
    html = HTML(string= html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=TRUE) as output:
        output.write(result)
        output.flush()
        output.seek(0) 
        response.write(output.read())
    
    return response

@admin_Login(signin)
def weekly_pdf(request):
    report = Order.objects.filter(status='DELIVERED').annotate(weekly=TruncYear('order_date')).values('weekly').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))
    response = HttpResponse(content_type = 'application/pdf')
    
    
    response['Content-Disposition'] = 'inline; attachment; filename = daily report'+ \
        str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = 'binary'
    html_string = render_to_string('admin_T/pdf_output.html',{'order': report})
    html = HTML(string= html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=TRUE) as output:
        output.write(result)
        output.flush()
        output.seek(0) 
        response.write(output.read())
    
    return response

@admin_Login(signin)
def monthly_pdf(request):
    report = Order.objects.filter(status='DELIVERED').annotate(day=TruncMonth('order_date')).values('day').annotate(count=Count('id')).annotate(sum=Sum('grand_total'))
    response = HttpResponse(content_type = 'application/pdf')
    
    
    response['Content-Disposition'] = 'inline; attachment; filename = daily report'+ \
        str(datetime.datetime.now()) + '.pdf'
    response["Content-Transfer-Encoding"] = 'binary'
    html_string = render_to_string('admin_T/pdf_output.html',{'order': report})
    html = HTML(string= html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=TRUE) as output:
        output.write(result)
        output.flush()
        output.seek(0) 
        response.write(output.read())
    
    return response


@admin_Login(signin)
def select(request):
    main = request.GET.get('main_categ')
    category = Category.objects.filter(main_cate=main)
    return render(request,'admin_T/select.html',{'mains':category})


@admin_Login(signin)
def category_managment(request):
    category = Category.objects.all().order_by('-id')
    main = MainCategory.objects.all().order_by('-id')
    return render(request,'admin_T/category_M.html',{'pro': category, 'cats':main}) 


@admin_Login(signin)
def edit_cate(request,id=0):
    if request.method == "POST":
        body = json.loads(request.body)
        category_name = body['name']        
        main = body['main_ca']
        details = body['det']
        id= request.session.get('cate')
        print(id)
        try:
            cate = Category.objects.filter(id=id).update(namer = category_name, description = details,main_cate = main) 
        except Exception as e:
            print(e)
            data = {'message': "NAME ALREADY EXIST "} 
            return JsonResponse(data)    
        data = {'message': "EDITED SUCCESFULLY"} 
        return JsonResponse(data)

    request.session['cate'] = id
    cate = Category.objects.get(id=id)
    mai  = MainCategory.objects.all()
    print(id)
    return render(request, 'admin_T/edit_cate.html',{'cate':cate, 'main':mai}) 


def offer_product(request):
    products = Products.objects.all().order_by('-id')  
    return render(request,'admin_T/product_offer.html',{'products': products})


def add_offer(request):
    body = json.loads(request.body)
    
    
    try:
        id = body['id']
        amount =int( body['amount'])
        if amount < 0:
            raise ValueError
        product = Products.objects.get(id=id)
        if amount > product.price:
            raise OfferAmountError(amount)
        product.offer = amount
        product.save()
        data = {'name':product.name,
                'message': 'offer added'
                }
        return JsonResponse(data)
    except OfferAmountError :
        data = {'message':"value can't be grater than product price",
                 'status': 'failed', 

        }
        return JsonResponse(data) 


    except Exception as e:
        print(e)
        
        data = {'message':'check the value u entered',
                'status': 'failed',
          }
        return JsonResponse(data)

    

