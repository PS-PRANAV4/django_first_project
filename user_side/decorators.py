from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages





def guest_user(url):
    def decorator(fun):
        def wrap(request,*args,**kwargs):
            user = request.user
            if user.is_authenticated:
                return fun(request,*args,**kwargs)
            else:
                return redirect(url,*args, **kwargs)
            
        return wrap
    return decorator