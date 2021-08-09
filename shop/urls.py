from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('subcategory/<slug:slug>/', SubcategoryView.as_view(), name='subcategory'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
    path('help', HelpView.as_view(), name='help'),
    path('about-us', AboutUsView.as_view(), name='about_us'),
]
