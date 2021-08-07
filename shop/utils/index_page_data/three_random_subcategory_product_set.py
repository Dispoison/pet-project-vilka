from shop.utils.functions import get_random_int_numbers, poly_set_to_counted_products_list
from shop.models.products.product import Product
from shop.utils.functions import set_discount


class ThreeRandomSubcategoryProductSetManager:
    @staticmethod
    def get_products():
        subcategories_length = len(Product.objects.values('subcategory_id').distinct())
        three_random_subcategory_products = Product.objects\
            .filter(subcategory_id__in=get_random_int_numbers(3, 1, subcategories_length)).select_related('subcategory')
        product_list = poly_set_to_counted_products_list(three_random_subcategory_products)
        for list_prod_model in product_list:
            set_discount(list(list_prod_model.values())[0])
            return product_list


class ThreeRandomSubcategoryProductSet:
    objects = ThreeRandomSubcategoryProductSetManager()