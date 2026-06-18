"""
URL configuration for abc_project project.
"""

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Global monkeypatch to handle dynamic pagination (list_per_page) without FieldError
original_get_changelist = ModelAdmin.get_changelist

def custom_get_changelist(self, request, **kwargs):
    cls = original_get_changelist(self, request, **kwargs)
    class DynPaginationChangeList(cls):
        def __init__(self, req, *args, **kws):
            page_param = req.GET.get('list_per_page')
            if page_param and page_param.isdigit():
                val = int(page_param)
                if 'list_per_page' in kws:
                    kws['list_per_page'] = val
                elif len(args) > 7:
                    args_list = list(args)
                    args_list[7] = val
                    args = tuple(args_list)
                else:
                    kws['list_per_page'] = val
            super().__init__(req, *args, **kws)
            
        def get_filters_params(self, params=None):
            lookup_params = super().get_filters_params(params)
            if lookup_params and 'list_per_page' in lookup_params:
                lookup_params.pop('list_per_page', None)
            return lookup_params
            
    return DynPaginationChangeList

ModelAdmin.get_changelist = custom_get_changelist

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('products/', include('products.urls')),
    path('contact/', include('contact.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Admin site customization
admin.site.site_header = 'ABC - Atal Bharat Creation'
admin.site.site_title = 'ABC Admin Portal'
admin.site.index_title = 'Welcome to ABC Admin Portal'
