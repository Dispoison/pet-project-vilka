from django.db import models
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from customer.models.customer import Customer
from customer.models.cart_product import CartProduct


class Cart(models.Model):
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    owner = models.OneToOneField(Customer, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена', default=0)

    def __str__(self):
        return f'Корзина: {self.owner}'


@receiver(post_save, sender=Customer)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(owner=instance)


@receiver(post_save, sender=Customer)
def save_cart(sender, instance, **kwargs):
    instance.cart.save()


@receiver(post_delete, sender=CartProduct)
def update_cart_on_delete_cart_product(sender, instance, **kwargs):
    instance.cart.total_products -= instance.quantity
    instance.cart.total_price -= instance.total_price
    instance.cart.save()


@receiver(m2m_changed, sender=Cart.products.through)
def update_cart_on_m2m_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        cart_products = CartProduct.objects.filter(pk__in=kwargs.get('pk_set'))
        for cart_product in cart_products:
            instance.total_products += cart_product.quantity
            instance.total_price += cart_product.total_price
        instance.save()
    elif action == 'custom_update':
        instance.total_products += kwargs.get('quantity')
        instance.total_price += kwargs.get('total_price')
        instance.save()


