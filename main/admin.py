from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.utils.html import format_html
from django.urls import reverse

# Unregister the default GroupAdmin
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Define Custom GroupAdmin with merged Actions column
@admin.register(Group)
class CustomGroupAdmin(BaseGroupAdmin):
    show_facets = admin.ShowFacets.ALWAYS
    list_display = ('name', 'group_actions')
    search_fields = ('name',)

    def group_actions(self, obj):
        edit_url = reverse('admin:auth_group_change', args=[obj.pk])
        delete_url = reverse('admin:auth_group_delete', args=[obj.pk])
        return format_html(
            '<div style="display: flex; gap: 8px; align-items: center;">'
            '  <a class="btn-action btn-action-edit" href="{}" title="Edit"><i class="fas fa-edit"></i></a>'
            '  <a class="btn-action btn-action-delete" href="{}" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    group_actions.short_description = 'Actions'
    group_actions.allow_tags = True

# Define Custom UserAdmin with Action Buttons
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Unregister the default User admin
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    show_facets = admin.ShowFacets.ALWAYS
    # Add 'user_actions' to list_display
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_actions')
    
    # Enable editing 'is_staff' directly from the list
    list_editable = ('is_staff',)

    def user_actions(self, obj):
        edit_url = reverse('admin:auth_user_change', args=[obj.pk])
        delete_url = reverse('admin:auth_user_delete', args=[obj.pk])
        return format_html(
            '<div style="display: flex; gap: 8px; align-items: center;">'
            '  <a class="btn-action btn-action-edit" href="{}" title="Edit"><i class="fas fa-edit"></i></a>'
            '  <a class="btn-action btn-action-delete" href="{}" title="Delete"><i class="fas fa-trash-alt"></i></a>'
            '</div>',
            edit_url, delete_url
        )
    user_actions.short_description = 'Actions'
    user_actions.allow_tags = True
