from django import template
from collections import namedtuple

register = template.Library()

Breadcrumb = namedtuple('Breadcrumb', 'name url')


@register.inclusion_tag('shop/base/breadcrumb.html')
def show_breadcrumb_category(subcategories):
    breadcrumb = [Breadcrumb(subcategories.first().parent, None)]
    return {'breadcrumb': breadcrumb}


@register.inclusion_tag('shop/base/breadcrumb.html')
def show_breadcrumb_subcategory(product):
    breadcrumb = [Breadcrumb(product.subcategory.parent, product.subcategory.parent.get_absolute_url()),
                  Breadcrumb(product.subcategory, None)]
    return {'breadcrumb': breadcrumb}


@register.inclusion_tag('shop/base/breadcrumb.html')
def show_breadcrumb_product(product):
    breadcrumb = [Breadcrumb(product.subcategory.parent, product.subcategory.parent.get_absolute_url()),
                  Breadcrumb(product.subcategory, None)]
    return {'breadcrumb': breadcrumb}


@register.inclusion_tag('shop/base/breadcrumb.html')
def show_breadcrumb_single_title(text):
    breadcrumb = [Breadcrumb(text, None)]
    return {'breadcrumb': breadcrumb}
