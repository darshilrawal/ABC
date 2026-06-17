from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def cart_add(request, product_id):
    # Require login before adding to cart
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to add products to your inquiry basket.')
        login_url = reverse('accounts:login')
        return redirect(f"{login_url}?next={request.path}")

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override_quantity=cd['override'])
    else:
        # Simple GET request adds 1 item
        cart.add(product=product, quantity=1)
        messages.success(request, f'"{product.name}" added to your inquiry basket.')

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    # Require login before removing from cart
    if not request.user.is_authenticated:
        messages.warning(request, 'Please log in to manage your inquiry basket.')
        login_url = reverse('accounts:login')
        return redirect(f"{login_url}?next=/cart/")

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
                            'quantity': item['quantity'],
                            'override': True})
    return render(request, 'cart/detail.html', {'cart': cart})
