from django.db import models
from shop.models.products.product import Product


class Smartphone(Product):
    class Meta:
        verbose_name = 'Смартфон'
        verbose_name_plural = 'Смартфоны'

    internet = models.CharField(max_length=100, verbose_name='Стандарт связи')
    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    display = models.CharField(max_length=100, verbose_name='Дисплей')
    processor = models.CharField(max_length=100, verbose_name='Процессор')
    sim_number = models.PositiveSmallIntegerField(verbose_name='Количество СИМ-карт')
    sim_size = models.CharField(max_length=50, verbose_name='Размер СИМ-карт')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    memory = models.CharField(max_length=50, verbose_name='Встроенная память')
    accum_volume = models.CharField(max_length=50, verbose_name='Объем аккумулятора')