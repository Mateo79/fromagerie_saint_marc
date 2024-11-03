from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'featured', 'created_at')
    list_filter = ('category', 'featured', 'created_at')
    search_fields = ('name', 'description')
