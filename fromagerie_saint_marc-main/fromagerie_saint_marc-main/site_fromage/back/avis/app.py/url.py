# produits/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProduitViewSet
from django.contrib import admin
from django.urls import path, include


router = DefaultRouter()
router.register(r'produits', ProduitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('produits.urls')),  # Inclure les routes de l'API
]
