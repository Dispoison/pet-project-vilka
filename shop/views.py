from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db.models.signals import m2m_changed
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from django.db.models import Case, When

from shop.models.products.product import Product
from shop.models.categories.category import Category
from shop.models.categories.subcategory import Subcategory
from shop.forms import AddProductToCartForm, DisplayOptionsForm
from shop.utils.mixins.view_data_mixin import ViewDataMixin
from shop.utils.functions import set_discount
from shop.utils.index_page_data import *

from customer.models.customer import Customer
from customer.models.cart import Cart
from customer.models.cart_product import CartProduct


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
                                        When(discounted_price__isnull=False, then='discounted_price'))) \
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
        product_parent_fields_number = len(Product._meta.concrete_fields)
        product = self.get_object()
        details = [Field(field.name, field.verbose_name)
                   for field in product._meta.fields][product_parent_fields_number + 1:]
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
            form_data = {
                'user': request.user.username,
                'quantity': self.form.cleaned_data.get('quantity'),
                'slug': kwargs.get('slug')
            }
            User = get_user_model()
            customer = Customer.objects.get(user=User.objects.get(username=form_data.get('user')))
            cart = Cart.objects.get(owner=customer)
            product = Product.objects.get(slug=form_data.get('slug'))
            total_price = product.get_price() * form_data.get('quantity')

            same_product = cart.products.filter(object_id=product.pk)

            if not same_product.exists():

                cart_product = CartProduct.objects.create(content_object=product,
                                                          customer=customer,
                                                          cart=cart,
                                                          quantity=form_data.get('quantity'),
                                                          total_price=total_price)
                cart.products.add(cart_product)
            else:
                cart_product = same_product.first()
                cart_product.quantity += form_data.get('quantity')
                cart_product.total_price += total_price
                cart_product.save()
                m2m_changed.send(sender=Cart.products.through, instance=cart, action='custom_update',
                                 quantity=form_data.get('quantity'), total_price=total_price)
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


class DeleteCartProductView(View):
    @staticmethod
    def post(request):
        id = request.POST.get('id')
        try:
            cart_product = CartProduct.objects.get(pk=id)
            if cart_product.customer.user == request.user:
                cart = cart_product.cart
                cart_product.delete()

                total_products = cart.total_products
                total_price = cart.total_price

                data = {
                    'message': 'Продукт успешно удален из корзины',
                    'total_products': total_products,
                    'total_price': total_price,
                }

                return JsonResponse(data=data)
            else:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return JsonResponse(data={'message': 'Продукт с заданным id не существует'}, status=400)
        except PermissionDenied:
            return JsonResponse(data={'message': 'Продукт не принадлежит вам'}, status=403)


class CreateCartProduct(View):
    @staticmethod
    def post(request):
        product_id = request.POST.get('id')
        quantity = int(request.POST.get('quantity'))

        customer = request.user.customer
        cart = customer.cart
        product = Product.objects.get(pk=product_id)
        cart_product_total_price = product.get_price() * quantity

        same_product = cart.products.filter(object_id=product_id)

        if not same_product.exists():

            cart_product = CartProduct.objects.create(content_object=product,
                                                      customer=customer,
                                                      cart=cart,
                                                      quantity=quantity,
                                                      total_price=cart_product_total_price)
            cart.products.add(cart_product)

            data = {
                'result': 'created',
                'cart_product_id': cart_product.pk,
            }
        else:
            cart_product = same_product.first()
            cart_product.quantity += quantity
            cart_product.total_price += cart_product_total_price
            cart_product.save()
            m2m_changed.send(sender=Cart.products.through, instance=cart, action='custom_update',
                             quantity=quantity, total_price=cart_product_total_price)

            data = {
                'result': 'updated',
                'cart_product_id': cart_product.pk,
            }

        cart_product_total_price = cart_product.total_price
        total_quantity = cart_product.quantity
        total_products = cart.total_products
        total_price = cart.total_price

        data.update({
            'cart_product_total_price': cart_product_total_price,
            'quantity': total_quantity,
            'total_products': total_products,
            'total_price': total_price,
        })
        return JsonResponse(data=data)


def handler404(request, exception):
    return render(request, 'shop/handlers/handler404.html')
