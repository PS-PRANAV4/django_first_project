from django.contrib import admin
from profiles.models import Profile
from .models import Cart,CartProduct,Order,ProductOrders
# Register your models here.


admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(ProductOrders)
admin.site.register(Profile)