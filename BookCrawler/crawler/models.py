from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    route_name = models.CharField(max_length=100)
    extraction_date = models.DateTimeField()

class Book(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail_url = models.CharField(max_length=400)
    price = models.CharField(max_length=100)
    stock = models.BooleanField()
    product_description = models.CharField(max_length=500)
    upc = models.CharField(max_length=100)
