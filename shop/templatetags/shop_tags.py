from django import template
from math import ceil

register = template.Library()


@register.filter
def division_by_3_ceil_range(num):
    return range(ceil(num / 3))


@register.filter
def products_slice(subcategory, i):
    return subcategory[i*3:i*3+3]
