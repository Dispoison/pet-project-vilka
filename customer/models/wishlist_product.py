from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class WishlistProduct(models.Model):
    class Meta:
        verbose_name = 'Продукт списка желаний'
        verbose_name_plural = 'Продукты списков желаний'

    customer = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    wishlist = models.ForeignKey('Wishlist', verbose_name='Список желаний', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип продукта')
    object_id = models.PositiveIntegerField(verbose_name='ID продукта')
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Продукт: {self.content_object.name}'
