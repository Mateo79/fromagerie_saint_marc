class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Note de 1 à 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product.name} ({self.rating}/5)'
