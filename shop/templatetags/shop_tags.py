from django import template
from math import ceil

register = template.Library()


@register.filter
def division_by_3_ceil_range(num):
    return range(ceil(num / 3))


@register.filter
def products_slice(subcategory, i):
    return subcategory[i * 3:i * 3 + 3]


@register.filter
def times(count):
    return range(1, int(count)+1)


@register.simple_tag(name='getattr')
def get_attribute(obj, field):
    from collections import namedtuple
    Field = namedtuple('Field', 'verbose_name value')
    value = getattr(obj, field.name)
    return Field(field.verbose_name, value)


@register.simple_tag()
def get_bound_field(form, field):
    return form.fields[field].get_bound_field(form, field).data


@register.simple_tag()
def rating_progress_width(count, total_count):
    return count / total_count * 100 if total_count else 0


@register.inclusion_tag('shop/subcategory/display_options.html')
def display_options(form):
    return {'form': form}


@register.inclusion_tag('shop/base/cart.html')
def show_cart(cart, cart_products, request):
    return {'cart': cart, 'cart_products': cart_products, 'request': request}


@register.inclusion_tag('shop/base/wishlist.html')
def show_wishlist(wishlist, wishlist_products, request):
    return {'wishlist': wishlist, 'wishlist_products': wishlist_products, 'request': request}


@register.inclusion_tag('shop/base/product_block.html')
def show_product_block(product):
    return {'product': product}


@register.inclusion_tag('shop/product/stars.html')
def show_stars(rating):
    full_stars = int(rating)
    remainder = rating - full_stars
    half_star = 0
    if 0.5 <= remainder:
        half_star = 1
    empty_stars = 5 - (full_stars + half_star)
    return {'full_stars': full_stars, 'half_star': half_star, 'empty_stars': empty_stars}
