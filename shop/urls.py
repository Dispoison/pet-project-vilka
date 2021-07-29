from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<slug:slug>/', show_category, name='category'),
    path('subcategory/<slug:slug>/', show_subcategory, name='subcategory'),
    path('product/<slug:slug>/', show_product, name='product'),
]
