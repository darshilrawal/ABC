from django.shortcuts import render
from products.models import Product


def home(request):
    """Home page view"""
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]
    categories = [
        {
            'name': 'Kurtis',
            'slug': 'kurtis',
            'description': 'Traditional & contemporary designs',
            'icon': 'fa-vest'
        },
        {
            'name': 'Short Kurtis',
            'slug': 'short_kurtis',
            'description': 'Trendy & versatile styles',
            'icon': 'fa-shirt'
        },
        {
            'name': 'Tops',
            'slug': 'tops',
            'description': 'Modern & fashionable collection',
            'icon': 'fa-tshirt'
        },
        {
            'name': 'Jeans',
            'slug': 'jeans',
            'description': 'Quality denim for all occasions',
            'icon': 'fa-person-dress'
        },
    ]
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


def about(request):
    """About page view"""
    capabilities = [
        {
            'title': 'Manufacturing Capacity',
            'value': '50,000+',
            'description': 'Pieces per month',
            'icon': 'fa-industry'
        },
        {
            'title': 'Quality Check',
            'value': '100%',
            'description': 'Inspection rate',
            'icon': 'fa-check-circle'
        },
        {
            'title': 'Delivery',
            'value': '15-20',
            'description': 'Days turnaround',
            'icon': 'fa-truck-fast'
        },
        {
            'title': 'Experience',
            'value': '10+',
            'description': 'Years in industry',
            'icon': 'fa-award'
        },
    ]
    
    values = [
        {
            'title': 'Quality First',
            'description': 'We never compromise on quality. Each piece undergoes rigorous quality checks before dispatch.',
            'icon': 'fa-gem'
        },
        {
            'title': 'Timely Delivery',
            'description': 'We understand the importance of timelines in business. Our logistics ensure on-time delivery.',
            'icon': 'fa-clock'
        },
        {
            'title': 'Competitive Pricing',
            'description': 'Direct manufacturing allows us to offer the best prices without compromising quality.',
            'icon': 'fa-tags'
        },
        {
            'title': 'Customer Support',
            'description': 'Our dedicated team is always ready to assist you with your queries and requirements.',
            'icon': 'fa-headset'
        },
    ]
    
    context = {
        'capabilities': capabilities,
        'values': values,
    }
    return render(request, 'main/about.html', context)
