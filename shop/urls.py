from django.urls import path, re_path
from django.views.generic import RedirectView

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<slug:slug>/', show_category, name='category'),
    path('subcategory/<slug:slug>/', show_subcategory, name='subcategory'),
    path('product/<slug:slug>/', show_product, name='product'),
    path('help', show_help, name='help'),
    path('about-us', show_about_us, name='about_us'),
    path('404', handler404, name='404'),
]
