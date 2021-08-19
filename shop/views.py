from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.signals import m2m_changed
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Case, When

from shop.models.products.product import Product
from shop.models.categories.category import Category
from shop.models.categories.subcategory import Subcategory
from shop.models.products.product_rating import ProductRating
from shop.forms import DisplayOptionsForm
from shop.utils.mixins.view_data_mixin import ViewDataMixin
from shop.utils.functions import set_discount
from shop.utils.index_page_data import *

from customer.models.cart import Cart
from customer.models.cart_product import CartProduct
from customer.models.wishlist_product import WishlistProduct
from customer.models.review import Review

from datetime import datetime
from babel.dates import format_datetime


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

    def get_context_data(self, *, object_list=None, **kwargs):
        base_context = super().get_context_data(**kwargs)

        from collections import namedtuple
        shown_size = 3
        other_product_shown_count = 4
        Field = namedtuple('Field', 'name verbose_name')
        product_parent_fields_number = len(Product._meta.concrete_fields)
        product = self.get_object()
        details = [Field(field.name, field.verbose_name)
                   for field in product._meta.fields][product_parent_fields_number + 1:]
        short_description = product.description.split('.')[0]
        other_products = product.__class__.objects.exclude(pk=product.pk). \
                             select_related('subcategory')[:other_product_shown_count]
        set_discount(other_products)
        reviews = Review.objects.filter(object_id=product.pk)[:shown_size + 1]

        is_more_reviews = True
        if len(reviews) < shown_size + 1:
            is_more_reviews = False

        reviews = reviews[:shown_size]

        mixin_context = self.get_mixin_context(details=details,
                                               short_description=short_description,
                                               other_products=other_products,
                                               reviews=reviews,
                                               is_more_reviews=is_more_reviews)
        return base_context | mixin_context

    def get_object(self, queryset=None):
        return Product.objects.get_queryset().prefetch_related('photos').select_related('rating').get(
            slug=self.kwargs[self.slug_url_kwarg])


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


class CreateCartProductView(View):
    @staticmethod
    def post(request):
        product_id = request.POST.get('id')
        quantity = request.POST.get('quantity')

        quantity = 1 if quantity is None else int(quantity)

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
                'message': 'Продукт успешно добавлен в корзину',
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
                'message': 'Продукт в корзине успешно обновлен',
            }

        cart_product_total_price = cart_product.total_price
        total_quantity = cart_product.quantity
        total_products = cart.total_products
        total_price = cart.total_price

        data.update({
            'cart_product_total_price': cart_product_total_price,
            'total_quantity': total_quantity,
            'total_products': total_products,
            'total_price': total_price,
        })
        return JsonResponse(data=data)


class DeleteWishlistProductView(View):
    @staticmethod
    def post(request):
        id = request.POST.get('id')
        try:
            wishlist_product = WishlistProduct.objects.get(pk=id)
            if wishlist_product.customer.user == request.user:
                wishlist = wishlist_product.wishlist
                wishlist_product.delete()

                total_products = wishlist.total_products

                data = {
                    'total_products': total_products,
                    'message': 'Продукт успешно удален из желаемого',
                }

                return JsonResponse(data=data)
            else:
                raise PermissionDenied
        except ObjectDoesNotExist:
            return JsonResponse(data={'message': 'Продукт с заданным id не существует'}, status=400)
        except PermissionDenied:
            return JsonResponse(data={'message': 'Продукт не принадлежит вам'}, status=403)


class CreateWishlistProductView(View):
    @staticmethod
    def post(request):
        product_id = request.POST.get('id')

        customer = request.user.customer
        wishlist = customer.wishlist
        product = Product.objects.get(pk=product_id)

        same_product = wishlist.products.filter(object_id=product_id)

        if not same_product.exists():

            wishlist_product = WishlistProduct.objects.create(content_object=product,
                                                              customer=customer,
                                                              wishlist=wishlist)
            wishlist.products.add(wishlist_product)
            total_products = wishlist.total_products

            data = {
                'wishlist_product_id': wishlist_product.pk,
                'total_products': total_products,
                'message': 'Продукт успешно добавлен в корзину',
            }
            return JsonResponse(data=data)
        else:
            return JsonResponse(data={'message': 'Продукт уже находится в желаемом'}, status=400)


class CreateReviewView(View):
    @staticmethod
    def post(request):
        product_id = request.POST.get('product-id')
        rating = request.POST.get('rating')
        text = request.POST.get('text')

        product = Product.objects.get(pk=product_id)
        customer = request.user.customer

        review = Review.objects.create(author=customer,
                                       content_object=product,
                                       text=text,
                                       rating=rating)

        product_rating = ProductRating.objects.get(product_id=review.object_id)

        data = {'username': customer.user.username,
                'created_at': format_datetime(review.created_at, 'dd MMMM yyyy г. HH:mm', locale='ru'),
                'rating': review.rating,
                'text': text,
                'product_rating': product.rating.rating,
                'five_star_count': product_rating.five_star_count,
                'four_star_count': product_rating.four_star_count,
                'three_star_count': product_rating.three_star_count,
                'two_star_count': product_rating.two_star_count,
                'one_star_count': product_rating.one_star_count,
                'total_stars_count': product_rating.total_stars_count,
                'message': 'Отзыв успешно создан'}

        return JsonResponse(data=data)


class MoreReviewsView(View):
    @staticmethod
    def get(request):
        shown_size = 3
        product_id = int(request.GET.get('product_id'))
        earliest_review_id = int(request.GET.get('earliest_review_id'))
        data = dict()

        review_objects = Review.objects.filter(object_id=product_id, pk__lt=earliest_review_id)[:shown_size + 1]

        if not review_objects:
            data.update({'message': 'Больше нет отзывов'})
            return JsonResponse(data=data, status=400)

        if len(review_objects) < shown_size + 1:
            data.update({'is_more_reviews': False})
        else:
            data.update({'is_more_reviews': True})

        reviews = []

        for i, review in enumerate(review_objects[:shown_size]):
            review_data = {'username': review.author.user.username,
                           'created_at': format_datetime(review.created_at, 'dd MMMM yyyy г. HH:mm', locale='ru'),
                           'rating': review.rating,
                           'text': review.text}

            if i + 1 == shown_size:
                review_data['earliest-review'] = True
                review_data['review_id'] = review.pk

            reviews.append(review_data)

        data.update({'reviews': reviews, 'message': 'Успешно доставлены дополнительные отзывы'})

        return JsonResponse(data=data)


def handler404(request, exception):
    return render(request, 'shop/handlers/handler404.html')
