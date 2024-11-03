from django.contrib.sitemaps.views import sitemap
from .sitemaps import ProductSitemap

sitemaps = {
    'products': ProductSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
