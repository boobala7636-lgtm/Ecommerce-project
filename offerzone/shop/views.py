from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request,"shop/index.html")

def  register(request):
    return render(request,"shop/register.html")

def collections(request):
    category = Catagory.objects.filter(status=0)
    return render(request,'shop/collections.html',{'category':category})

def productview(request,name):
    if(Catagory.objects.filter(name=name,status=0)):
        products =Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/products.html',{'products':products, 'product_name':name})
    else:
        messages.warning(request, "No Such Category Found")
        return redirect('collections')

def product_details(request,cname,pname):
    if(Catagory.objects.filter(name=cname, status=0)):
        if(Product.objects.filter(name=pname, status=0)):
            product_details=Product.objects.filter(name=pname,status=0).first()
            return render(request, 'shop/products/product_details.html',{'product_details':product_details})
        else:
            messages.warning(request,'No Such Product Found')
            return redirect('collections')
    else:
        messages.warning(request, 'No Such Product Found')
        return redirect('collections')