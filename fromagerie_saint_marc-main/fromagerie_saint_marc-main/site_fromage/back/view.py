from django.shortcuts import render
from .models import Product

def search(request):
    query = request.GET.get('q')  # Récupère le terme de recherche
    products = Product.objects.filter(name__icontains=query)  # Recherche dans le nom
    return render(request, 'products/search_results.html', {'products': products, 'query': query})

def product_list(request):
    category = request.GET.get('category')
    sort_by = request.GET.get('sort_by', 'name')  # Tri par défaut : nom

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    products = products.order_by(sort_by)

    return render(request, 'products/product_list.html', {'products': products})
