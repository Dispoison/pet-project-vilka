from django import template

register = template.Library()


@register.inclusion_tag('shop/base/list_subcategories.html')
def show_subcaterogies(category):
    subs = category.subcategory_set.all()
    return {'subcategories': subs}


@register.inclusion_tag('shop/base/list_categories_header.html')
def show_categories_header(categories):
    return {'categories': categories}


@register.inclusion_tag('shop/index/top_discounted_products.html')
def show_top_discounted_products(top_discounted_products):
    return {'top_discounted_products': top_discounted_products}
