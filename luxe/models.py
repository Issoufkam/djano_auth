from itertools import product
from pyexpat import model
from tkinter import CASCADE
from django.db import models
# from django.contrib.auth.models import AbstractUser
# from phone_field import PhoneField
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']
    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    category = models.ForeignKey(Category, related_name='categorie', on_delete=models.CASCADE)
    image1 = models.CharField(max_length=5000)
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="imgs")
    
    def __str__(self):
        return self.product.title
    