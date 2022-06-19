from django.shortcuts import redirect, render
import random
from .models import Coupon
# Create your views here.

def coupon(request):
    coupons = Coupon.objects.all()

    return render(request,'admin_T/coupon.html',{'coupons': coupons})

def generate(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        number_list = [x for x in range(10)]
        alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        list = number_list+alphabets
        code_items = []

        for i in range(10):
            num = random.choice(list)
            code_items.append(num)

        code_string = "".join(str(item) for item in code_items)
        
        coupons = Coupon.objects.create(number=code_string,coupon_amount=amount)
       
        
    return redirect(coupon)