from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inquiry


def contact(request):
    """Contact page view"""
    context = {
        'address': '1050–1051, Under Ground, Tirupati Market, Moti Begumwadi, Ring Road, Surat – 395002, Gujarat, India',
        'phone': '+91 88661 56157 (Kantilal D. Rawal) | +91 70698 26157 (Ratanlal D. Rawal)',
        'email': 'atalbharatcreation@gmail.com',
        'business_hours': 'Mon - Sat: 9:00 AM - 7:00 PM',
        'gst_number': 'GSTIN: 24AASPR5788C1Z5',
        'owners': [
            {'name': 'Kantilal D. Rawal', 'phone': '+91 88661 56157'},
            {'name': 'Ratanlal D. Rawal', 'phone': '+91 70698 26157'},
        ],
    }
    return render(request, 'contact/contact.html', context)


def inquiry(request):
    """Bulk inquiry form view"""
    if request.method == 'POST':
        try:
            inquiry = Inquiry(
                company_name=request.POST.get('company_name', ''),
                contact_person=request.POST.get('contact_person', ''),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone', ''),
                city=request.POST.get('city', ''),
                product_interest=request.POST.get('product_interest', ''),
                estimated_quantity=request.POST.get('estimated_quantity', ''),
                message=request.POST.get('message', ''),
            )
            inquiry.save()
            messages.success(request, 'Your inquiry has been submitted successfully! Our team will contact you soon.')
            return redirect('contact:inquiry_success')
        except Exception as e:
            messages.error(request, 'There was an error submitting your inquiry. Please try again.')
    
    product_choices = Inquiry.PRODUCT_INTEREST_CHOICES
    
    # Pre-fill message with cart items if coming from cart
    default_message = ""
    from cart.cart import Cart
    cart = Cart(request)
    if cart:
        default_message = "I am interested in the following products:\n\n"
        for item in cart:
            product = item['product']
            default_message += f"- {product.name} (Qty: {item['quantity']})\n"
        default_message += "\nPlease provide a quote for these items."

    context = {
        'product_choices': product_choices,
        'default_message': default_message,
    }
    return render(request, 'contact/inquiry.html', context)


def inquiry_success(request):
    """Inquiry success page"""
    return render(request, 'contact/inquiry_success.html')
