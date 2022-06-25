from django.shortcuts import redirect, render
import razorpay
from admins.models import Accounts
from fashion_now import settings
from cart_orders.models import Cart, Order,CartProduct
from profiles.models import Profile
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Payment
from user_side.views import checkout,first
from django.views.decorators.cache import cache_control

# Create your views here.

def index(request):
    return render(request,'indexx.html')


def order_payment(request,id,check):
    cart_id = request.session.get('cart_product')
    if cart_id:
        cart_products = CartProduct.objects.get(id = cart_id)
        offer = cart_products.product.offer
        amount = cart_products.product.price - offer
    else:
        request.session['check']  = check
        user =request.user
        print(user,'jjjjjjjjjjjjjjjj')
        user_o = Accounts.objects.get(id=id)
        print(check)
        request.session['user']  = user_o.id
        cart = Cart.objects.get(user=user_o)
        if cart.grand_total > 0:
            
            cartproduct  = CartProduct.objects.filter(cart=cart)
            total_offer = 0
            for prod in cartproduct:
                total_offer = total_offer + prod.product.offer*prod.quantity
            if cart.coupon_offer > 0:
                    total_offer = total_offer+cart.coupon_offer
            amount = cart.grand_total-total_offer  
        else:
            return redirect(first)
        
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create(
        {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
    )
    print(razorpay_order['id'])
    if cart_id:
        payment = Payment.objects.create(
            user=request.user, total_amount=amount, order_id=razorpay_order['id']
        )
    else:
        payment = Payment.objects.create(
            user=user_o, total_amount=amount, order_id=razorpay_order['id']
        )
    payment.save()
    return render(
        request,
        "payment.html",
        {
            "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": payment,
        },
    )
        

@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@csrf_exempt
def callback(request):
    
    print("JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ")
    if  request.method == 'POST':
        print('*********************************')
        payment_id = request.POST.get("razorpay_payment_id", "")
        print('eeeeeeeeeeeeeeee',payment_id)
        provider_order_id = request.POST.get("razorpay_order_id", "")
        print(provider_order_id, 'gggggggggggg')
        signature_id = request.POST.get("razorpay_signature", "")
        try:
            order = Payment.objects.get(order_id=provider_order_id)
        except:
            
            # payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
            provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id")
            print(provider_order_id)
            order = Payment.objects.get(order_id=provider_order_id)

            print('going through here')
            return render(request, "callback.html", context={"status": "FAILED"})

        # order.transaction_id = payment_idclient = razorpay.Client(auth=("YOUR_ID", "YOUR_SECRET"))
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        result = client.utility.verify_payment_signature({
        'razorpay_order_id': provider_order_id,
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature_id
        })

        order.payment_id = payment_id
        order.signature_id = signature_id    
        order.save()
        if result:
            user =request.user
            print(user,'jjjjjjjjjjjjjjjj')
            check = request.session.get('check')
            id = request.session.get('user')
            print(check,id,'ffffffffffffffffffff')
            order.status = 'ACCEPTED'
            order.save()
            print('out complete')
            return redirect(course_changer)
        else:
            order.status = 'FAILED'
            order.save()
            print('going through here')
            return render(request, "callback.html", context={"status": order.status})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = 'FAILED'
        order.save()
        return render(request, "callback.html", context={"status": order.status})
    
def course_changer(request):
    check = request.session.get('check')
    id = request.session.get('user')
    print(check,id,'ffffffffffffffffffff')

    return redirect(checkout,check,id)