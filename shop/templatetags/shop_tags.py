from django import template
from math import ceil

register = template.Library()


@register.filter
def division_by_3_ceil_range(num):
    return range(ceil(num / 3))


@register.filter
def products_slice(subcategory, i):
    return subcategory[i * 3:i * 3 + 3]


@register.simple_tag(name='getattr')
def get_attribute(obj, field):
    from collections import namedtuple
    Field = namedtuple('Field', 'verbose_name value')
    value = getattr(obj, field.name)
    return Field(field.verbose_name, value)


@register.inclusion_tag('shop/product/add_to_cart.html')
def show_add_to_cart(form):
    return {'form': form}


@register.inclusion_tag('shop/subcategory/display_options.html')
def display_options(form):
    return {'form': form}


@register.inclusion_tag('shop/base/breadcrumb.html')
def show_breadcrumb(breadcrumb):
    return {'breadcrumb': breadcrumb}


@register.simple_tag()
def get_bound_field(form, field):
    return form.fields[field].get_bound_field(form, field).data
