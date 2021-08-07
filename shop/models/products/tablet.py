from django.db import models
from shop.models.products.product import Product


class Tablet(Product):
    class Meta:
        verbose_name = 'Планшет'
        verbose_name_plural = 'Планшеты'

    internet = models.CharField(max_length=100, verbose_name='Стандарт связи')
    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    display = models.CharField(max_length=100, verbose_name='Дисплей')
    processor = models.CharField(max_length=100, verbose_name='Процессор')
    sim_number = models.PositiveSmallIntegerField(verbose_name='Количество СИМ-карт')
    sim_size = models.CharField(max_length=50, verbose_name='Размер СИМ-карт')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    memory = models.CharField(max_length=50, verbose_name='Встроенная память')
    accum_volume = models.CharField(max_length=50, verbose_name='Объем аккумулятора')
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Вес')