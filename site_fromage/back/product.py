from django.db import models

class Product(models.Model):
    # Nom du produit (fromage, yaourt, etc.)
    name = models.CharField(max_length=100)
    
    # Description du produit
    description = models.TextField()
    
    # Type de produit (par exemple : fromage, beurre, etc.)
    CATEGORY_CHOICES = [
        ('fromage', 'Fromage'),
        ('beurre', 'Beurre'),
        ('lait', 'Lait'),
        ('yaourt', 'Yaourt'),
        ('autre', 'Autre'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    # Prix du produit
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Date de production
    production_date = models.DateField()
    
    # Date limite de consommation (facultatif)
    expiration_date = models.DateField(blank=True, null=True)
    
    # Stock disponible (en unités)
    stock_quantity = models.PositiveIntegerField()
    
    # Image du produit (stockée dans un dossier 'products/')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # Produit mis en avant (produit du mois, promotions, etc.)
    featured = models.BooleanField(default=False)
    
    # Date de création et de mise à jour pour gérer les modifications
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
