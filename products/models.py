from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Model for product categories"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Unit(models.Model):
    """Model for units of measurement"""
    name = models.CharField(max_length=50, help_text="e.g., Piece, Box, Meter")
    short_name = models.CharField(max_length=10, help_text="e.g., pcs, box, m")
    
    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.short_name})"


class Product(models.Model):
    """Model for clothing products"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='products', null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    min_order_quantity = models.PositiveIntegerField(default=50)
    price_range = models.CharField(max_length=100, blank=True, verbose_name="Price", help_text="e.g., ₹250")
    fabric = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    def get_category_display(self):
        return self.category.name if self.category else ""

    def get_category_display_name(self):
        return self.category.name if self.category else ""


class Cart(models.Model):
    """Shopping cart for B2B buyers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def get_items(self):
        return self.items.all()


class CartItem(models.Model):
    """Individual items in a cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
