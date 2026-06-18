from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render
from django.http import Http404
from django import forms
from django.utils.safestring import mark_safe
from .models import Product, Category, Unit


class AdminImageWidget(forms.ClearableFileInput):
    """Custom ClearableFileInput to render a thumbnail image preview and remove/change buttons in a dashed frame"""
    def render(self, name, value, attrs=None, renderer=None):
        input_id = attrs.get('id', f'id_{name}') if attrs else f'id_{name}'
        html = []
        
        # Unique IDs for elements
        preview_container_id = f"preview_container_{name}"
        img_id = f"preview_img_{name}"
        placeholder_id = f"preview_placeholder_{name}"
        clear_checkbox_id = f"{name}_clear_id"
        
        # Dashed container start
        html.append(
            format_html(
                '<div id="{}" class="view-image-card" style="border: 2px dashed var(--admin-border-color); border-radius: var(--admin-radius-md); padding: 24px; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 280px; background: rgba(255,255,255,0.01); text-align: center; max-width: 400px; margin-bottom: 12px; font-family: var(--admin-font-family); box-sizing: border-box; position: relative;">',
                preview_container_id
            )
        )
        
        if value and hasattr(value, "url"):
            # Image is present
            html.append(
                format_html(
                    '  <img id="{}" src="{}" alt="Preview" style="max-width: 100%; max-height: 140px; border-radius: 8px; object-fit: contain; margin-bottom: 12px; box-shadow: var(--admin-shadow-sm); border: 1px solid var(--admin-border-light);">'
                    '  <div id="{}" style="display: none;"><i class="fas fa-image" style="font-size: 3rem; color: var(--admin-text-muted); margin-bottom: 16px;"></i></div>'
                    '  <label class="image-remove-btn" style="color: #dc3545; font-size: 0.9rem; font-weight: 600; cursor: pointer; display: inline-flex; align-items: center; margin-bottom: 12px; user-select: none;">'
                    '    <input type="checkbox" name="{}-clear" id="{}" class="image-clear-checkbox" style="display: none;" onchange="toggleImageRemoval(this, \'{}\')">'
                    '    <span class="remove-text" style="transition: all 0.2s ease;">&#x274C; Remove</span>'
                    '  </label>'
                    '  <label for="{}" class="btn-change-image" style="background: var(--admin-gradient-primary); color: #ffffff; padding: 10px 20px; border-radius: var(--admin-radius-sm); font-weight: 600; font-size: 0.85rem; cursor: pointer; display: inline-block; transition: all 0.2s ease; box-shadow: 0 4px 12px var(--admin-accent-glow); text-transform: uppercase; margin-bottom: 8px;">'
                    '    Change Image'
                    '  </label>',
                    img_id, value.url, placeholder_id, name, clear_checkbox_id, img_id, input_id
                )
            )
        else:
            # Image is NOT present
            html.append(
                format_html(
                    '  <img id="{}" src="" alt="Preview" style="max-width: 100%; max-height: 140px; border-radius: 8px; object-fit: contain; margin-bottom: 12px; box-shadow: var(--admin-shadow-sm); border: 1px solid var(--admin-border-light); display: none;">'
                    '  <div id="{}"><i class="fas fa-image" style="font-size: 3rem; color: var(--admin-text-muted); margin-bottom: 16px;"></i></div>'
                    '  <label class="image-remove-btn" style="color: #dc3545; font-size: 0.9rem; font-weight: 600; cursor: pointer; display: none; align-items: center; margin-bottom: 12px; user-select: none;">'
                    '    <input type="checkbox" name="{}-clear" id="{}" class="image-clear-checkbox" style="display: none;" onchange="toggleImageRemoval(this, \'{}\')">'
                    '    <span class="remove-text" style="transition: all 0.2s ease;">&#x274C; Remove</span>'
                    '  </label>'
                    '  <label for="{}" class="btn-change-image" style="background: var(--admin-gradient-primary); color: #ffffff; padding: 10px 20px; border-radius: var(--admin-radius-sm); font-weight: 600; font-size: 0.85rem; cursor: pointer; display: inline-block; transition: all 0.2s ease; box-shadow: 0 4px 12px var(--admin-accent-glow); text-transform: uppercase; margin-bottom: 8px;">'
                    '    Upload Image'
                    '  </label>',
                    img_id, placeholder_id, name, clear_checkbox_id, img_id, input_id
                )
            )
            
        # File info, hidden file input, and JavaScript
        html.append(
            format_html(
                '  <span style="color: var(--admin-text-muted); font-size: 0.75rem; font-weight: 500;">PNG, JPG, GIF up to 2MB</span>'
                '  <input type="file" name="{}" id="{}" style="display: none;" class="image-file-input-hidden" onchange="previewSelectedImage(this, \'{}\', \'{}\', \'{}\')">'
                '</div>'
                '<script>'
                'function toggleImageRemoval(checkbox, imgId) {{'
                '    const img = document.getElementById(imgId);'
                '    const text = checkbox.nextElementSibling;'
                '    if (checkbox.checked) {{'
                '        if (img) img.style.opacity = "0.3";'
                '        text.textContent = "\\u267B\\uFE0F Keep Image";'
                '        text.style.color = "var(--admin-accent-primary)";'
                '    }} else {{'
                '        if (img) img.style.opacity = "1";'
                '        text.textContent = "\\u274C Remove";'
                '        text.style.color = "#dc3545";'
                '    }}'
                '}}'
                'function previewSelectedImage(input, imgId, placeholderId, checkboxId) {{'
                '    const img = document.getElementById(imgId);'
                '    const placeholder = document.getElementById(placeholderId);'
                '    const checkbox = document.getElementById(checkboxId);'
                '    if (input.files && input.files[0]) {{'
                '        const reader = new FileReader();'
                '        reader.onload = function(e) {{'
                '            if (img) {{'
                '                img.src = e.target.result;'
                '                img.style.display = "block";'
                '                img.style.opacity = "1";'
                '            }}'
                '            if (placeholder) placeholder.style.display = "none";'
                '            // Uncheck remove checkbox if user uploads new file'
                '            if (checkbox) {{'
                '                checkbox.checked = false;'
                '                toggleImageRemoval(checkbox, imgId);'
                '            }}'
                '            // Find the upload button text and change to "Change Image"'
                '            const label = input.closest(".view-image-card").querySelector(".btn-change-image");'
                '            if (label) label.textContent = "Change Image";'
                '        }};'
                '        reader.readAsDataURL(input.files[0]);'
                '    }}'
                '}}'
                '</script>',
                name, input_id, img_id, placeholder_id, clear_checkbox_id
            )
        )
        
        return mark_safe(''.join(html))


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
                'placeholder': '₹250',
                'style': 'width: 200px;'
            }),
            'fabric': forms.TextInput(attrs={
                'placeholder': 'e.g., Cotton Blend, Silk, Rayon',
                'style': 'width: 100%; max-width: 600px;'
            }),
            'image': AdminImageWidget(),
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
    list_display = ['name', 'category', 'unit', 'price_range', 'is_featured', 'is_active', 'created_at', 'edit_button']
    list_display_links = ['name']  # Make name clickable to edit
    list_filter = ['category', 'unit', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'fabric']
    list_editable = ['is_featured', 'is_active']
    ordering = ['-created_at']
    list_per_page = 10
    show_facets = admin.ShowFacets.ALWAYS  # Always show filter counts
    
    # Allow all fields to be edited
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'unit', 'image'),
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
    
    # Register custom view detail URL pattern
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/view/', self.admin_site.admin_view(self.view_product_detail), name='products_product_view'),
        ]
        return custom_urls + urls


    # Controller for custom read-only product detail page
    def view_product_detail(self, request, object_id):
        obj = self.get_object(request, object_id)
        if not obj:
            raise Http404("Product not found")
        
        context = self.admin_site.each_context(request)
        context.update({
            'title': f'View Product: {obj.name}',
            'opts': self.model._meta,
            'original': obj,
            'object_id': object_id,
            'is_popup': False,
            'media': self.media,
            'app_label': self.model._meta.app_label,
        })
        
        return render(request, 'admin/products/product/view_detail.html', context)

    # Add view, edit, delete icons to Action column
    def edit_button(self, obj):
        view_url = reverse('admin:products_product_view', args=[obj.pk])
        edit_url = reverse('admin:products_product_change', args=[obj.pk])
        delete_url = reverse('admin:products_product_delete', args=[obj.pk])
        
        return format_html(
            '<div style="display: flex; gap: 8px; align-items: center;">'
            '  <a class="btn-action btn-action-view" href="{}" title="View"><i class="fas fa-eye"></i></a>'
            '  <a class="btn-action btn-action-edit" href="{}" title="Edit"><i class="fas fa-edit"></i></a>'
            '  <a class="btn-action btn-action-delete" href="{}" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            view_url, edit_url, delete_url
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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description', 'edit_button']
    list_display_links = ['name']
    search_fields = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    show_facets = admin.ShowFacets.ALWAYS
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/view/', self.admin_site.admin_view(self.view_category_detail), name='products_category_view'),
        ]
        return custom_urls + urls

    def view_category_detail(self, request, object_id):
        obj = self.get_object(request, object_id)
        if not obj:
            raise Http404("Category not found")
        
        context = self.admin_site.each_context(request)
        context.update({
            'title': f'View Category: {obj.name}',
            'opts': self.model._meta,
            'original': obj,
            'object_id': object_id,
            'is_popup': False,
            'media': self.media,
            'app_label': self.model._meta.app_label,
            'products': obj.products.all(),
        })
        
        return render(request, 'admin/products/category/view_detail.html', context)

    def edit_button(self, obj):
        view_url = reverse('admin:products_category_view', args=[obj.pk])
        edit_url = reverse('admin:products_category_change', args=[obj.pk])
        delete_url = reverse('admin:products_category_delete', args=[obj.pk])
        
        return format_html(
            '<div style="display: flex; gap: 8px; align-items: center;">'
            '  <a class="btn-action btn-action-view" href="{}" title="View"><i class="fas fa-eye"></i></a>'
            '  <a class="btn-action btn-action-edit" href="{}" title="Edit"><i class="fas fa-edit"></i></a>'
            '  <a class="btn-action btn-action-delete" href="{}" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            view_url, edit_url, delete_url
        )
    edit_button.short_description = 'Action'
    edit_button.allow_tags = True


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'edit_button']
    list_display_links = ['name']
    search_fields = ['name', 'short_name']
    list_per_page = 10
    show_facets = admin.ShowFacets.ALWAYS
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/view/', self.admin_site.admin_view(self.view_unit_detail), name='products_unit_view'),
        ]
        return custom_urls + urls

    def view_unit_detail(self, request, object_id):
        obj = self.get_object(request, object_id)
        if not obj:
            raise Http404("Unit not found")
        
        context = self.admin_site.each_context(request)
        context.update({
            'title': f'View Unit: {obj.name}',
            'opts': self.model._meta,
            'original': obj,
            'object_id': object_id,
            'is_popup': False,
            'media': self.media,
            'app_label': self.model._meta.app_label,
            'products': obj.products.all(),
        })
        
        return render(request, 'admin/products/unit/view_detail.html', context)

    def edit_button(self, obj):
        view_url = reverse('admin:products_unit_view', args=[obj.pk])
        edit_url = reverse('admin:products_unit_change', args=[obj.pk])
        delete_url = reverse('admin:products_unit_delete', args=[obj.pk])
        
        return format_html(
            '<div style="display: flex; gap: 8px; align-items: center;">'
            '  <a class="btn-action btn-action-view" href="{}" title="View"><i class="fas fa-eye"></i></a>'
            '  <a class="btn-action btn-action-edit" href="{}" title="Edit"><i class="fas fa-edit"></i></a>'
            '  <a class="btn-action btn-action-delete" href="{}" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            view_url, edit_url, delete_url
        )
    edit_button.short_description = 'Action'
    edit_button.allow_tags = True
