import django.contrib.admin
from django.http import HttpResponse
from django.shortcuts import render

from .models import *


def index(request):
    three_main_subcategories = ThreeMainSubcategory.objects.get_three_main_subcategories()
    top_discounted_products = TopDiscountedProducts.objects.get_discounted_products_from_subclasses()
    three_random_subcategory_products = ThreeRandomSubcategoryProductSet.objects \
        .get_three_random_subcategory_products()
    context = {
        'title': 'Интернет-магазин Vilka',
        'three_main_subcategories': three_main_subcategories,
        'top_discounted_products': top_discounted_products,
        'three_random_subcategory_products': three_random_subcategory_products,
    }
    return render(request, 'shop/index/index.html', context=context)


def show_category(request, slug):
    return HttpResponse(slug)


def show_subcategory(request, slug):
    return HttpResponse(slug)


def show_product(request, slug):
    from collections import namedtuple
    product = Product.objects.get_queryset().prefetch_related('photos').get(slug=slug)
    categories = Category.objects.prefetch_related('subcategory_set')
    Field = namedtuple('Field', 'name verbose_name')
    details = [Field(field.name, field.verbose_name) for field in product._meta.fields][10:]
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'product': product,
        'details': details
    }
    return render(request, 'shop/product.html', context=context)
