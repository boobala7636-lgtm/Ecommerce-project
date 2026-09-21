from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse


# Create your views here.

def home(request):
    trending_products = Product.objects.filter(trending=1)
    return render(request,"shop/index.html", {'trending_products':trending_products})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)

            if user is not None:
                login(request,user)
                messages.success(request,'Logged In Successful!')
                return redirect('/')
            else:
                messages.error(request,'Invalid User and Password')
                return redirect('login')
        return render(request, 'shop/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged Out Successfully.')
    return redirect('/')


def  register(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            form=CustomUserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Register Successful!')
                return redirect('login')
            else:
                messages.warning(request,'Re-Enter the details.')
                
        else:
            form = CustomUserForm()
        return render(request, 'shop/register.html',{'form':form})



    

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



def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                product_qty = int(data['product_qty']) # Ensure it is handled as an integer
                product_id = data['pid']

                # 1. Fetch the full Product object instance from the database
                product_status = Product.objects.get(id=product_id)
                
                
                # 2. Check if the product is already in the user's cart
                if Cart.objects.filter(user=request.user, product=product_status).exists():
                    return JsonResponse({
                        'status' : 'alert',
                        'message' : 'Product Already in Cart'
                    }, status=200)
                else:
                    # 3. Verify stock availability before adding
                    if product_status.quantity >= product_qty:
                        
                        Cart.objects.create(
                            user=request.user, 
                            product=product_status, 
                            product_qty=product_qty
                        )
                        return JsonResponse({
                            'status':'success',
                            'message' : 'Product successfully added to cart.'
                        }, status=200)
                    else:
                        return JsonResponse({
                                'status':'alert',
                                'message' : 'Product stock Not Available '
                            }, status=200)

            except Product.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Product does not exist.'
                }, status=404)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid data received.'
                }, status=400)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=400)


def cart_display(request):
    if request.user.is_authenticated:
        cart_data = Cart.objects.filter(user=request.user)
        return render(request, 'shop/cart_details.html',{'cart_data':cart_data})
    else:
        messages.warning(request,'You Should login first')
        return redirect('/')

def remove_cart(request, id):
    cartitem = Cart.objects.get(id=id)
    cartitem.delete()
    return redirect('cart_details')

