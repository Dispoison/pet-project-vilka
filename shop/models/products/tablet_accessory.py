from django.db import models
from shop.models.products.product import Product


class TabletAccessory(Product):
    class Meta:
        verbose_name = 'Аксессуар для планшета'
        verbose_name_plural = 'Аксессуары для планшета'

    form_factor = models.CharField(max_length=50, verbose_name='Форм фактор')
    material = models.CharField(max_length=50, verbose_name='Материал')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    tablet_diagonal = models.CharField(max_length=100, verbose_name='Диагональ планшета')
