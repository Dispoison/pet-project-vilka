from operator import attrgetter
from shop.utils.functions import set_discount
from shop.models.products.product import Product


class TopDiscountedProductsManager:
    @staticmethod
    def get_products():
        products = Product.objects.filter(discounted_price__isnull=False).select_related('subcategory')
        set_discount(products)
        return sorted(products, key=attrgetter('discount'), reverse=True)


class TopDiscountedProducts:
    objects = TopDiscountedProductsManager()