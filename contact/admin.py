from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_person', 'email', 'phone', 'product_interest', 'is_read', 'is_responded', 'created_at']
    list_filter = ['product_interest', 'is_read', 'is_responded', 'created_at']
    search_fields = ['company_name', 'contact_person', 'email', 'phone', 'city', 'message']
    list_editable = ['is_read', 'is_responded']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    show_facets = admin.ShowFacets.ALWAYS  # Always show filter counts
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('company_name', 'contact_person', 'email', 'phone', 'city')
        }),
        ('Inquiry Details', {
            'fields': ('product_interest', 'estimated_quantity', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_responded', 'created_at')
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_responded']
    
    @admin.action(description='Mark selected inquiries as read')
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    
    @admin.action(description='Mark selected inquiries as responded')
    def mark_as_responded(self, request, queryset):
        queryset.update(is_responded=True, is_read=True)
