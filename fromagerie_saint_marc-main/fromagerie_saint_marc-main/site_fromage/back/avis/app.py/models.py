# produits/models.py

from django.db import models

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nom
