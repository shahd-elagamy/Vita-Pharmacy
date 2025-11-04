from django.urls import path
from . import views


app_name = 'orders'

urlpatterns = [
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:cart_item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('', views.view_cart, name='view_cart'),
    path('order/<int:product_id>/', views.order_form, name='order_form'),
    path('submit_order/', views.submit_order, name='submit_order'),
    path('checkout/', views.checkout, name='checkout'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('order_success/', views.order_success, name='order_success'), 
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),  
    
]
