from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def admin_Login(url):
    def decorator(fun):
        def wrap(request,*args,**kwargs):
            user = request.user
            if user.is_authenticated:
                if user.is_admin:
                    return fun(request,*args,**kwargs)
                else:
                    logout(request)
                    messages.error(request,'FORBIDDEN TO ENTER HERE')
                    return redirect(url)
            else:
                return redirect(url)
        return wrap
    return decorator