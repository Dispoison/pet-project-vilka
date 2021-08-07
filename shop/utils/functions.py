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


def set_discount(products):
    [setattr(prod, 'discount', int(100 - 100 * (prod.discounted_price / prod.price)))
     for prod in products if prod.discounted_price]
