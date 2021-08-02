import django.contrib.admin
from django.http import HttpResponse
from django.shortcuts import render

from shop.models import *
from shop.forms import AddProductToCartForm


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
    if request.method == 'POST':
        form = AddProductToCartForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
    else:
        form = AddProductToCartForm
    from collections import namedtuple
    product = Product.objects.get_queryset().prefetch_related('photos').get(slug=slug)
    categories = Category.objects.prefetch_related('subcategory_set')
    Field = namedtuple('Field', 'name verbose_name')
    details = [Field(field.name, field.verbose_name) for field in product._meta.fields][10:]
    short_description = product.description.split('.')[0]


    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'product': product,
        'details': details,
        'short_description': short_description,
        'form': form,
    }
    return render(request, 'shop/product/product.html', context=context)
