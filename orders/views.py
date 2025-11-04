# orders/views.py

from django.shortcuts import get_object_or_404, redirect,render
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Order
from .forms import CartItemForm  # Ensure you have a form class for this

# @login_required
# def place_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     quantity = request.POST.get('quantity', 1)  

#     
#     Order.objects.create(
#         user=request.user,
#         product=product,
#         quantity=quantity
#     )
    
#     
#     return redirect('product_list')  

# @login_required
# def order_list(request):
#     orders = Order.objects.filter(user=request.user)
#     return render(request, 'orders/order_list.html',{'orders':orders})

# orders/views.py
# orders/views.py

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order
from .forms import OrderForm

@login_required
def submit_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            address = form.cleaned_data['address']

            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

         
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                status='received'
            )

            return redirect('orders:order_confirmation')

    return redirect('orders:order_form')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def order_confirmation(request):
    return render(request, 'orders/order_confirmation.html')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('orders:empty_cart')

    total_price = sum(item.product.price * item.quantity for item in cart.items.all())

    if request.method == 'POST':
      
        cart.items.all().delete()
        
        # cart.delete()

    
        return redirect('orders:order_success')

    return render(request, 'orders/checkout.html', {'cart': cart, 'total_price': total_price})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import OrderForm



@login_required
def order_form(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    form = OrderForm(initial={
        'product': product,
        'name': user.get_full_name(),
        'email': user.email,
        'address': user.profile.address if hasattr(user, 'profile') else '',
    })

    return render(request, 'orders/order_form.html', {'form': form, 'product': product})

def order_success(request):
    return render(request, 'orders/order_success.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from orders.models import Cart, CartItem
from products.models import Product
from .forms import AddToCartForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return redirect('orders:empty_cart')
    
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'orders/view_cart.html', {'cart': cart, 'cart_items': cart_items})
def empty_cart(request): 
    return render(request, 'orders/empty_cart.html')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from products.models import Product
from .models import Cart, CartItem
@csrf_exempt 
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                return JsonResponse({'error': 'Invalid quantity'}, status=400)

            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            cart_quantity = CartItem.objects.filter(cart=cart).count()

            return JsonResponse({'cart_quantity': cart_quantity, 'message': 'Item added successfully!'})
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity <= 0:
                return render(request, 'orders/update_cart.html', {'cart_item': cart_item, 'error': 'Invalid quantity'})

            cart_item.quantity = quantity
            cart_item.save()
            return redirect('orders:view_cart')  # Redirect to the cart view after updating

        except ValueError:
            return render(request, 'orders/update_cart.html', {'cart_item': cart_item, 'error': 'Invalid quantity'})

    return render(request, 'orders/update_cart.html', {'cart_item': cart_item, 'error': 'Invalid request method'})





from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CartItem
@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, cart__user=request.user)
      
        Order.objects.filter(product=cart_item.product, user=request.user).delete()
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass 
    return redirect('orders:view_cart')




