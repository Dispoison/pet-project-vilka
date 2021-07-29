from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def index(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    top_discounted_products = TopDiscountedProducts.objects.get_discounted_products_from_subclasses()
    print(top_discounted_products, '!!!')
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'top_discounted_products': top_discounted_products,
    }
    return render(request, 'shop/index/index.html', context=context)


def show_category(request, slug):
    return HttpResponse(slug)


def show_subcategory(request, slug):
    return HttpResponse(slug)


def show_product(request, slug):
    return HttpResponse(f'Продукт: {slug}')
