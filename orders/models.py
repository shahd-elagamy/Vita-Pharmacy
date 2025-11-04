from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.conf import settings

class UserProfile(models.Model):
   user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
   phone = models.CharField(max_length=20)
   photo = models.ImageField(upload_to='profile_pics/',blank=True)

   def __str__(self):
      return self.user.username
   
from django.db import models
from django.conf import settings
from products.models import Product
from users.models import CustomUser

from django.db import models
from django.conf import settings
from products.models import Product 

class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('in_delivery', 'In-delivery'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')

    def __str__(self):
        return f"{self.user.username} ordered {self.product.name}"

    class Meta:
        db_table = 'orders_order'

from django.db import models
from django.conf import settings
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('in_delivery', 'In-delivery'),
        ('delivered', 'Delivered'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from products.models import Product
from .forms import OrderForm

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  
            order.user = request.user
            order.product = product
            order.save()  
            return redirect('orders:order_success')  
        form = OrderForm()

    return render(request, 'orders/create_order.html', {'form': form, 'product': product})
def order_success(request):
    return render(request, 'orders/order_success.html')



# class Favorite(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ('user', 'product')  # Prevent duplicates

#     def __str__(self):
#         return f"{self.user.username} favorited {self.product.name}"

