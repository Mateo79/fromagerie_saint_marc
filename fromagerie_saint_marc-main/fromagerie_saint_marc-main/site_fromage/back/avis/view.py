from .models import Review
from .forms import ReviewForm
from django.views.decorators.cache import cache_page

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = product.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
    else:
        form = ReviewForm()

    return render(request, 'products/product_detail.html', {'product': product, 'reviews': reviews, 'form': form})


@cache_page(60 * 15)  # Mise en cache pendant 15 minutes
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})
