from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app.models import *
from django.contrib.auth.models import User,auth
from app.emailhandle import EmailHandle
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
# Create your views here.

def index(request):
    Product =  products.objects.all()
    context = {
        'Product':Product,
    }
    return render(request,'product.html',context)



def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        
        
        if User.objects.filter(email = email).exists():
            return redirect('login')
        else:
            user  = User(
                username = username,
                email = email,
            )
            user.set_password(password)
            user.save()

            if user is not None:
                auth_login(request, user)
                return redirect('/')

    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        user = EmailHandle.authenticate(request,username = request.POST.get('email'),password = request.POST.get('password'))
        if user is not None:
            auth_login(request, user)
            return redirect('/')
    
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='/login')
def cart(request,product_id):
    product = products.objects.get(id=product_id)
    user = request.user  


    if request.method=='POST':
        quantity=request.POST.get('quantity')
        
    cart_item, created = addcart.objects.get_or_create(user=user, product=product)

    
    return redirect("/")

@login_required(login_url='/login')
def viewcart(request):
    cartitems = addcart.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cartitems)
    context={
        'cartitems':cartitems,
        'total_amount': total_amount,
    }
    return render(request,'cart.html',context)

@login_required(login_url='/login')
def order(request):
    if request.method == 'POST':
        cartitems = addcart.objects.filter(user=request.user)

        
        if not cartitems.exists():
            messages.error(request, "Your cart is empty.")
            return redirect('order')
        
        # Update quantities based on submitted form data
        for item in cartitems:
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity and quantity.isdigit() and int(quantity) > 0:
                item.quantity = int(quantity)
                item.save()

        total_amount = sum(item.total_price() for item in cartitems)
        
        # Create an order
        order = Order.objects.create(user=request.user, total_amount=total_amount)
        
        # Add all cart items to this order
        for cart_item in cartitems:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )

        order.save()
        
        # Clear the cart after ordering
        cartitems.delete()
        
        return redirect('myorder')
    
    return render(request,'order.html')

@login_required(login_url='/login')
def myorder(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('order_products__product')
    context = {
        'orders': user_orders,
    }
    return render(request,'order.html',context)



@login_required
def delete_cart_item(request, item_id):
    cart_item = addcart.objects.get(id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')  # Adjust 'cart' to your cart page URL name

@login_required
def empty_cart(request):
    addcart.objects.filter(user=request.user).delete()
    return redirect('cart')  # Adjust 'cart' to your cart page URL na
