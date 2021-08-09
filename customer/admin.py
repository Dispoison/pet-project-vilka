from django.contrib import admin

from customer.models import *

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Wishlist)
admin.site.register(WishlistProduct)
