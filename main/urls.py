from django.urls import path
from . import views
from .views import search_product_api
app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),  
    path('about/', views.about, name='about'),
    path('api/search_product/', search_product_api, name='search_product_api'),
]
