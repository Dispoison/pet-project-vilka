from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from customer.models.customer import Customer


class Wishlist(models.Model):
    class Meta:
        verbose_name = 'Список желаний'
        verbose_name_plural = 'Списки желаний'

    owner = models.OneToOneField(Customer, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField('WishlistProduct', blank=True, related_name='related_wishlist')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def __str__(self):
        return f'Список желаний: {self.owner}'


@receiver(post_save, sender=Customer)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(owner=instance)


@receiver(post_save, sender=Customer)
def save_wishlist(sender, instance, **kwargs):
    instance.wishlist.save()

