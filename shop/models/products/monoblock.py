from django.db import models
from shop.models.products.product import Product


class Monoblock(Product):
    class Meta:
        verbose_name = 'Моноблок'
        verbose_name_plural = 'Моноблоки'

    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    display = models.CharField(max_length=100, verbose_name='Дисплей')
    processor = models.CharField(max_length=100, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    disk = models.CharField(max_length=50, verbose_name='Накопитель данных')
    videocard = models.CharField(max_length=100, verbose_name='Видеокарта')
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Вес')
