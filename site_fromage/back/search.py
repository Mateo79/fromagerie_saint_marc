from django.db import models
from django.urls import path
from . import views

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)


urlpatterns = [
    path('search/', views.search, name='search'),
]