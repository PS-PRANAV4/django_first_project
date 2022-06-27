from django.shortcuts import render

# Create your views here.

def todoo(request):
    return render(request,'admin_T/todo.html')