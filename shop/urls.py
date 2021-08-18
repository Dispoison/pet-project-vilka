from django.urls import path

from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='home'),
    path('category/<slug:slug>/', CategoryView.as_view(), name='category'),
    path('subcategory/<slug:slug>/', SubcategoryView.as_view(), name='subcategory'),
    path('product/<slug:slug>/', ProductView.as_view(), name='product'),
    path('help', HelpView.as_view(), name='help'),
    path('about-us', AboutUsView.as_view(), name='about_us'),
    path('cart-product/delete/', DeleteCartProductView.as_view(), name='cart_product_delete'),
    path('cart-product/create/', CreateCartProductView.as_view(), name='cart_product_create'),
    path('wishlist-product/delete/', DeleteWishlistProductView.as_view(), name='wishlist_product_delete'),
    path('wishlist-product/create/', CreateWishlistProductView.as_view(), name='wishlist_product_create'),
    path('review/create/', CreateReviewView.as_view(), name='review_create'),
]
