from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from customer.models.customer import Customer


class Cart(models.Model):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    owner = models.OneToOneField(Customer, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=Customer)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)


@receiver(post_save, sender=Customer)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()

