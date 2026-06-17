from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('success/', views.inquiry_success, name='inquiry_success'),
]
