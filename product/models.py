from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings
from product.validators import validate_file
from cloudinary.models import CloudinaryField
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product=models.ForeignKey(
        Product,on_delete=models.CASCADE,related_name='images'
    )
    image=CloudinaryField("images")



class Review(models.Model):

    comment= models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)
    ratings=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    product= models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    )