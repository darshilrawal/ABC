from django import template
from django.contrib.auth.models import User
from products.models import Product

register = template.Library()

@register.simple_tag
def get_total_products():
    return Product.objects.count()

@register.simple_tag
def get_total_users():
    return User.objects.count()
