from shop.models.categories.category import Category


class ViewDataMixin:

    def get_mixin_context(self, **kwargs):
        context = kwargs

        context.update({
            'title': 'Интернет-магазин Vilka',
            'categories': Category.objects.prefetch_related('subcategory_set'),
        })
        return context
