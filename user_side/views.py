
from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from admins.models import Accounts
from product.models import Products,Category
from .utils import send_sms
from codes.forms import CodeForm
from django.contrib.auth.forms import AuthenticationForm


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
        if number:
            my_user.phone_number = number
        print('user created')
        my_user.save()
        print('user created')
        messages.success(request, "u succesfully created a user  you can login now")
         
        return redirect(first)
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


# def verify_view(request):
#     form = CodeForm(request.POST or None)
#     pk = request.session.get('pk')
#     if pk:
#         user = Accounts.objects.get(pk=pk)
#         code = user.code
#         code_user = f"{user.username}: {user.code}"
#         if not request.POST:
#             print(code_user)
#             send_sms(code_user, user.phone_number)
#         if form.is_valid():
#             num = form.cleaned_data.get('number')

#             if str(code) == num:
#                 code.save()
#                 login(request,user)
#                 return redirect(first)
#             else:
#                 return redirect(signin)
#     return render(request, 'verify.html', {'form':form})



def check_out(request):
    return render(request,'checkout.html')

def cart(request):
    return render(request,'shopping-cart.html')
