from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    ingredients = models.TextField(blank=True, help_text="List ingredients and allergens here.")
    size = models.CharField(max_length=255, help_text="e.g. '6 inch', '8-10 servings'")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/images/')
    stock = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    is_bestseller = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/')
    
    def __str__(self):
        return self.product.name

class AddOn(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.name} (+${self.price})"
