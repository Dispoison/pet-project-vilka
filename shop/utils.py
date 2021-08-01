from django import forms


class ProductMixin:
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    base_fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'price', 'discounted_price', 'photo', 'more_photos', 'description', 'subcategory')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subcategory':
            from shop.models import Subcategory
            return forms.ModelChoiceField(Subcategory.objects.filter(slug=self.subcategory_slug), empty_label=None,
                                          label='Подкатегория')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            super().save_model(request, obj, form, change)
            photos = request.FILES.getlist('more_photos')
            for photo in photos:
                from shop.models import ProductPhoto
                ProductPhoto.objects.create(product=obj, photo=photo)



def get_random_int_numbers(count, start, stop):
    from random import randint
    random_list = set()
    while len(random_list) < count:
        random_list.add(randint(start, stop))
    return list(random_list)


def poly_set_to_counted_products_list(poly_set):
    counted_products_list = []
    current_prods_cls = None
    for product in poly_set:
        if product.__class__ == current_prods_cls:
            counted_products_list[-1]['products'].append(product)
            counted_products_list[-1]['count'] += 1
        else:
            counted_products_list.append({'products': [product],
                                          'subcategory_name': product.subcategory.name,
                                          'count': 1})
            current_prods_cls = product.__class__
    return counted_products_list
