from django.db import models


class Inquiry(models.Model):
    """Model for bulk inquiry submissions"""
    
    PRODUCT_INTEREST_CHOICES = [
        ('kurtis', 'Kurtis'),
        ('short_kurtis', 'Short Kurtis'),
        ('tops', 'Tops'),
        ('jeans', 'Jeans'),
        ('multiple', 'Multiple Categories'),
        ('all', 'All Products'),
    ]
    
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, blank=True)
    product_interest = models.CharField(max_length=50, choices=PRODUCT_INTEREST_CHOICES)
    estimated_quantity = models.CharField(max_length=100, blank=True, help_text="e.g., 500-1000 pieces")
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    is_responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
    
    def __str__(self):
        return f"{self.company_name} - {self.contact_person}"
