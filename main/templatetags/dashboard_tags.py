from django import template
from django.contrib.auth.models import User
from products.models import Product, Category

register = template.Library()

@register.simple_tag
def get_total_products():
    return Product.objects.count()

@register.simple_tag
def get_total_users():
    return User.objects.count()

@register.simple_tag
def get_total_categories():
    return Category.objects.count()

@register.simple_tag
def get_categories_list():
    names = list(Category.objects.values_list('name', flat=True))
    if len(names) > 4:
        return ", ".join(names[:4]) + "..."
    return ", ".join(names)
