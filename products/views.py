from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Unit, Cart, CartItem


def product_list(request):
    """Product listing page with category filtering"""
    category = request.GET.get('category', None)
    
    products = Product.objects.filter(is_active=True)
    
    current_category_name = 'All Products'
    if category and category != 'all':
        try:
            curr_cat = Category.objects.get(slug=category)
            products = products.filter(category=curr_cat)
            current_category_name = curr_cat.name
        except Category.DoesNotExist:
            category = 'all'
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Load all categories dynamically from database
    categories = [{'slug': 'all', 'name': 'All Products'}] + [
        {'slug': cat.slug, 'name': cat.name} for cat in Category.objects.all()
    ]
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'current_category': category or 'all',
        'current_category_name': current_category_name,
        'total_products': products.count(),
    }
    return render(request, 'products/product_list.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add a product to the user's cart (login required)"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Get or create cart for user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create cart item
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated quantity for "{product.name}" in your cart!')
    else:
        messages.success(request, f'Added "{product.name}" to your cart!')
    
    # Check if AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'Added "{product.name}" to cart!',
            'cart_count': cart.get_total_items()
        })
    
    return redirect('products:list')


@login_required
def view_cart(request):
    """View the user's shopping cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    context = {
        'cart': cart,
        'items': cart.get_items(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'products/cart.html', context)


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed "{product_name}" from your cart.')
    return redirect('products:cart')


@login_required
def update_cart_quantity(request, item_id):
    """Update quantity of a cart item"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully!')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
    
    return redirect('products:cart')
