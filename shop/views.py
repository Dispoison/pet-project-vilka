from django.core.paginator import Paginator
from django.shortcuts import render

from shop.models import *
from shop.forms import AddProductToCartForm


def index(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    three_main_subcategories = ThreeMainSubcategory.objects.get_three_main_subcategories()
    top_discounted_products = TopDiscountedProducts.objects.get_discounted_products_from_subclasses()
    three_random_subcategory_products = ThreeRandomSubcategoryProductSet.objects \
        .get_three_random_subcategory_products()
    for list_prod_model in three_random_subcategory_products:
        set_discount(list(list_prod_model.values())[0])

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'three_main_subcategories': three_main_subcategories,
        'top_discounted_products': top_discounted_products,
        'three_random_subcategory_products': three_random_subcategory_products,
    }
    return render(request, 'shop/index/index.html', context=context)


def show_category(request, slug):
    categories = Category.objects.prefetch_related('subcategory_set')
    subcategories = categories.get(slug=slug).subcategory_set.all()
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'subcategories': subcategories,
    }
    return render(request, 'shop/category/category.html', context=context)


def show_subcategory(request, slug):
    categories = Category.objects.prefetch_related('subcategory_set')
    products = Product.objects.filter(subcategory__slug=slug)
    set_discount(products)
    paginator = Paginator(products, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'paginator': paginator,
        'page_obj': page_obj,
    }
    return render(request, 'shop/subcategory/subcategory.html', context=context)


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
    other_products = product.__class__.objects.exclude(pk=product.pk).select_related('subcategory')[:4]
    set_discount(other_products)

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'product': product,
        'details': details,
        'short_description': short_description,
        'other_products': other_products,
        'form': form,
    }
    return render(request, 'shop/product/product.html', context=context)


def show_help(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
    }
    return render(request, 'shop/other/help.html', context=context)


def show_about_us(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
    }
    return render(request, 'shop/other/about_us.html', context=context)
