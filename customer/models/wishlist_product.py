from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class WishlistProduct(models.Model):
    class Meta:
        verbose_name = 'Продукт списка желаний'
        verbose_name_plural = 'Продукты списков желаний'

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    wishlist = models.ForeignKey('Wishlist', verbose_name='Список желаний', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукт: {self.content_object.name}'
