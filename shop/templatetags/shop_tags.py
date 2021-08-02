from django import template
from math import ceil

register = template.Library()


@register.filter
def division_by_3_ceil_range(num):
    return range(ceil(num / 3))


@register.filter
def products_slice(subcategory, i):
    return subcategory[i*3:i*3+3]

@register.simple_tag(name='getattr')
def get_attribute(obj, field):
    from collections import namedtuple
    Field = namedtuple('Field', 'verbose_name value')
    value = getattr(obj, field.name)
    return Field(field.verbose_name, value)
