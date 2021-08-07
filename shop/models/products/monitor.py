from django.db import models
from shop.models.products.product import Product


class Monitor(Product):
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'

    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    frequency = models.PositiveSmallIntegerField(verbose_name='Частота обновления')
    resolution = models.CharField(max_length=50, verbose_name='Разрешение дисплея')
    matrix_type = models.CharField(max_length=50, verbose_name='Тип матрицы')