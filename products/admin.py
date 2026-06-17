from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from .models import Product


class ProductAdminForm(forms.ModelForm):
    """Custom form for Product admin with improved price field"""
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={
                'placeholder': 'Product description (Optional)',
                'rows': 4,
                'style': 'width: 100%;'
            }),
            'price_range': forms.TextInput(attrs={
                'placeholder': '₹250 - ₹450',
                'style': 'width: 200px;'
            }),
            'fabric': forms.TextInput(attrs={
                'placeholder': 'e.g., Cotton Blend, Silk, Rayon',
                'style': 'width: 100%; max-width: 600px;'
            }),
        }
    
    def clean_price_range(self):
        """Ensure price has ₹ symbol"""
        price = self.cleaned_data.get('price_range', '')
        if price and not price.startswith('₹'):
            # Add ₹ symbol if not present
            price = '₹' + price
        return price


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm  # Use custom form with ₹ placeholder
    list_display = ['name', 'category', 'price_range', 'is_featured', 'is_active', 'created_at', 'edit_button']
    list_display_links = ['name']  # Make name clickable to edit
    list_filter = ['category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'fabric']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']
    list_per_page = 20
    show_facets = admin.ShowFacets.ALWAYS  # Always show filter counts
    
    # Allow all fields to be edited
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'image'),
            'classes': ('wide',),
        }),
        ('Pricing & Details', {
            'fields': ('price_range', 'fabric'),
            'classes': ('wide',),
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active'),
            'classes': ('wide',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Add an edit button column
    def edit_button(self, obj):
        url = reverse('admin:products_product_change', args=[obj.pk])
        return format_html(
            '<a class="btn btn-sm btn-warning" href="{}" style="color: #000; padding: 5px 15px; border-radius: 4px; text-decoration: none; font-weight: 600;">✏️ Edit</a>',
            url
        )
    edit_button.short_description = 'Action'
    edit_button.allow_tags = True
    
    # Admin actions for bulk operations
    actions = ['make_featured', 'remove_featured', 'activate_products', 'deactivate_products']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} products marked as featured.")
    make_featured.short_description = "⭐ Mark selected as Featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} products removed from featured.")
    remove_featured.short_description = "Remove Featured status"
    
    def activate_products(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} products activated.")
    activate_products.short_description = "✅ Activate selected products"
    
    def deactivate_products(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} products deactivated.")
    deactivate_products.short_description = "❌ Deactivate selected products"
