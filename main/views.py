from django.shortcuts import render
from products.models import Product

def home(request):
    recent_products = Product.objects.order_by('-id')[:8]
    # swiper_products = Product.objects.filter(is_sale=True)

    context = {
        'recent_products': recent_products,
        # 'swiper_products': swiper_products,
    }
    return render(request, 'main/home.html', context)
def about(request):
    return render(request, 'main/about.html')



from django.http import JsonResponse
from products.models import Product

def search_product_api(request):
    query = request.GET.get('q', '').strip().lower()
    # Use icontains to find products that contain the query
    products = Product.objects.filter(name__icontains=query).order_by('name')[:1]  # Get the top match
    if products.exists():
        product = products.first()
        return JsonResponse({'id': product.id, 'name': product.name})
    return JsonResponse({'error': 'No products found'}, status=404)
