from django import forms
from shop.models.categories.subcategory import Subcategory


class ProductMixin:
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    base_fieldsets = (
        (None, {
            'fields': (
            'name', 'slug', 'price', 'discounted_price', 'photo', 'more_photos', 'description', 'subcategory')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'subcategory':
            return forms.ModelChoiceField(Subcategory.objects.filter(slug=self.subcategory_slug), empty_label=None,
                                          label='Подкатегория')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            super().save_model(request, obj, form, change)
            photos = request.FILES.getlist('more_photos')
            for photo in photos:
                from shop.models.products.product_photo import ProductPhoto
                ProductPhoto.objects.create(product=obj, photo=photo)
