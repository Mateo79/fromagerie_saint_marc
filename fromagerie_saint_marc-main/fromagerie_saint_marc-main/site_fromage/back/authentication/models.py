from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	language = models.CharField(default='eng')

class Item(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	images = models.ImageField(upload_to='items/', blank=True, null=True)
	quantity = models.IntegerField(default=1)
	available = models.BooleanField(default=True)
	category = models.CharField(max_length=100)
