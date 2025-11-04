# from django.contrib import admin
# from .models import Order, UserProfile

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user','product','status','order_date')
#     list_filter = ('status',)
#     search_fields = ('user__username','product__name')

# admin.site.register(Order, OrderAdmin)
# admin.site.register(UserProfile)

# from django.contrib import admin
# from .models import Order

# class OrderAdmin(admin.ModelAdmin):
#      list_display = ('user', 'product', 'quantity', 'order_date', 'status')  
#     # list_filter = ('status',)  
#     # list_editable = ('status',)  

# admin.site.register(Order, OrderAdmin)

# orders/admin.py

from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity','status')

