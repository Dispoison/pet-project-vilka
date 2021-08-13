from django.db import models
from django.db.models.signals import post_delete, m2m_changed, post_save
from django.dispatch import receiver

from customer.models.customer import Customer
from customer.models.wishlist_product import WishlistProduct


class Wishlist(models.Model):
    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'

    owner = models.OneToOneField(Customer, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(WishlistProduct, blank=True, related_name='related_wishlist')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def __str__(self):
        return f'Список желаний: {self.owner}'


@receiver(post_save, sender=Customer)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(owner=instance)


@receiver(post_delete, sender=WishlistProduct)
def update_wishlist_on_delete_wishlist_product(sender, instance, **kwargs):
    instance.wishlist.total_products -= instance.quantity
    instance.wishlist.total_price -= instance.total_price
    instance.wishlist.save()


@receiver(m2m_changed, sender=Wishlist.products.through)
def update_wishlist_on_m2m_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        wishlist_products = WishlistProduct.objects.filter(pk__in=kwargs.get('pk_set'))
        for wishlist_product in wishlist_products:
            instance.total_products += wishlist_product.quantity
            instance.total_price += wishlist_product.total_price
        instance.save()
    elif action == 'custom_update':
        instance.total_products += kwargs.get('quantity')
        instance.total_price += kwargs.get('total_price')
        instance.save()
