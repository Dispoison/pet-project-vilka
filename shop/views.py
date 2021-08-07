from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from shop.models.products.product import Product
from shop.models.categories.category import Category
from shop.models.categories.subcategory import Subcategory
from shop.forms import AddProductToCartForm, DisplayOptionsForm
from shop.utils.mixins.view_data_mixin import ViewDataMixin
from shop.utils.functions import set_discount
from shop.utils.index_page_data import *
from django.db.models import Case, When


class MainPageView(ViewDataMixin, ListView):
    model = Subcategory
    template_name = 'shop/index/index.html'
    context_object_name = 'three_main_subcategories'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(top_discounted_products=TopDiscountedProducts.objects.get_products(),
                                               three_random_subcategory_products=ThreeRandomSubcategoryProductSet
                                               .objects.get_products())
        return base_context | mixin_context

    def get_queryset(self):
        return Subcategory.objects.filter(name__in=['Смартфоны', 'Планшеты', 'Ноутбуки']).order_by('id')


class CategoryView(ViewDataMixin, ListView):
    model = Category
    template_name = 'shop/category/category.html'
    context_object_name = 'subcategories'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context

    def get_queryset(self):
        return Category.objects.prefetch_related('subcategory_set').get(slug=self.kwargs['slug']).subcategory_set.all()


class SubcategoryView(ViewDataMixin, ListView):
    model = Product
    template_name = 'shop/subcategory/subcategory.html'
    context_object_name = 'products'
    allow_empty = False

    sort_dict = {'0': '-lowest_price', '1': 'lowest_price'}
    display_num_dict = {'0': 3, '1': 6, '2': 9}

    sort = sort_dict['0']
    display_num = display_num_dict['0']
    form = DisplayOptionsForm

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context(form=self.form,
                                               sort=self.sort,
                                               display_num=self.display_num)
        return base_context | mixin_context

    def get_queryset(self):
        products = Product.objects.select_related('subcategory').filter(subcategory__slug=self.kwargs['slug']) \
            .annotate(lowest_price=Case(When(discounted_price__isnull=True, then='price'),
                                        When(discounted_price__isnull=False, then='discounted_price')))\
            .order_by(self.sort)
        set_discount(products)
        return products

    def post(self, request, *args, **kwargs):
        self.form = DisplayOptionsForm(request.POST)
        if self.form.is_valid():
            print(self.form.cleaned_data)
            self.sort = self.sort_dict[self.form.cleaned_data['sort']]
            self.display_num = self.display_num_dict[self.form.cleaned_data['display_num']]
        return self.get(request, *args, **kwargs)

    def get_paginate_by(self, queryset):
        return self.display_num


class ProductView(ViewDataMixin, DetailView):
    model = Product
    template_name = 'shop/product/product.html'
    context_object_name = 'product'

    form = AddProductToCartForm

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)

        from collections import namedtuple
        Field = namedtuple('Field', 'name verbose_name')
        ProductParentFieldsNumber = len(Product._meta.concrete_fields)
        product = self.get_object()
        details = [Field(field.name, field.verbose_name)
                   for field in product._meta.fields][ProductParentFieldsNumber + 1:]
        short_description = product.description.split('.')[0]
        other_products = product.__class__.objects.exclude(pk=product.pk).select_related('subcategory')[:4]
        set_discount(other_products)

        mixin_context = self.get_mixin_context(details=details,
                                               short_description=short_description,
                                               other_products=other_products,
                                               form=self.form)
        return base_context | mixin_context

    def get_object(self, queryset=None):
        return Product.objects.get_queryset().prefetch_related('photos').get(slug=self.kwargs[self.slug_url_kwarg])

    def post(self, request, *args, **kwargs):
        self.form = AddProductToCartForm(request.POST)
        if self.form.is_valid():
            print(self.form.cleaned_data)
        return self.get(request, *args, **kwargs)


class HelpView(ViewDataMixin, TemplateView):
    template_name = 'shop/other/help.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context


class AboutUsView(ViewDataMixin, TemplateView):
    template_name = 'shop/other/about_us.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)
        mixin_context = self.get_mixin_context()
        return base_context | mixin_context


def show_sign_in(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
    }
    return render(request, 'shop/account/sign_in.html', context=context)


def show_sign_up(request):
    categories = Category.objects.prefetch_related('subcategory_set')
    context = {
        'title': 'Интернет-магазин Vilka',
        'categories': categories,
    }
    return render(request, 'shop/account/sign_up.html', context=context)


class RegisterCustomer(CreateView):
    pass


def handler404(request, exception):
    return render(request, 'shop/handlers/handler404.html')
