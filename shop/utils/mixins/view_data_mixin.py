from shop.models.categories.category import Category
from customer.models.customer import Customer
from customer.models.cart import Cart


class ViewDataMixin:

    def get_mixin_context(self, **kwargs):
        context = kwargs

        context.update({
            'title': 'Интернет-магазин Vilka',
            'categories': Category.objects.prefetch_related('subcategory_set'),
        })

        user = self.request.user
        if user.is_authenticated:
            cart = Cart.objects.get(owner=Customer.objects.get(user=user))
            cart_products = cart.products.all()
            context.update({
                'cart': cart,
                'cart_products': cart_products,
            })

        return context
