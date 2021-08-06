from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from shop.models import *
from shop.forms import AddProductToCartForm, DisplayOptionsForm
from collections import namedtuple

Breadcrumb = namedtuple('Breadcrumb', 'name url is_active')


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

    if not subcategories:
        raise Http404

    breadcrumb = [Breadcrumb(subcategories[0].parent.name, None, True)]

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'subcategories': subcategories,
        'breadcrumb': breadcrumb,
    }
    return render(request, 'shop/category/category.html', context=context)


def show_subcategory(request, slug):
    sort_dict = {'0': '-price', '1': 'price'}
    sort = sort_dict['0']
    display_num = 2
    if request.method == 'POST':
        form = DisplayOptionsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            sort = sort_dict[form.cleaned_data['sort']]
            display_num = form.cleaned_data['display_num']
    else:
        form = DisplayOptionsForm
    categories = Category.objects.prefetch_related('subcategory_set')
    products = Product.objects.select_related('subcategory').filter(subcategory__slug=slug).order_by(sort)
    set_discount(products)

    paginator = Paginator(products, display_num)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if not products:
        raise Http404

    prod = products[0]

    breadcrumb = [Breadcrumb(prod.subcategory.parent.name, prod.subcategory.parent.get_absolute_url(), False),
                  Breadcrumb(prod.subcategory.name, None, True)]

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'paginator': paginator,
        'page_obj': page_obj,
        'breadcrumb': breadcrumb,
        'form': form,
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

    breadcrumb = [Breadcrumb(product.subcategory.parent.name, product.subcategory.parent.get_absolute_url(), False),
                  Breadcrumb(product.subcategory.name, product.subcategory.get_absolute_url(), False),
                  Breadcrumb(product.name, None, True)]

    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'product': product,
        'details': details,
        'short_description': short_description,
        'other_products': other_products,
        'breadcrumb': breadcrumb,
        'form': form,
    }
    return render(request, 'shop/product/product.html', context=context)


def show_help(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    breadcrumb = [Breadcrumb('Помощь', None, True)]
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'breadcrumb': breadcrumb,
    }
    return render(request, 'shop/other/help.html', context=context)


def show_about_us(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    breadcrumb = [Breadcrumb('О нас', None, True)]
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
        'breadcrumb': breadcrumb,
    }
    return render(request, 'shop/other/about_us.html', context=context)


def handler404(request, exception):
    return render(request, 'shop/handlers/handler404.html')
