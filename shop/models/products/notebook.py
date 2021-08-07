from django.db import models
from shop.models.products.product import Product


class Notebook(Product):
    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'

    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    display = models.CharField(max_length=100, verbose_name='Дисплей')
    processor = models.CharField(max_length=100, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    disk = models.CharField(max_length=50, verbose_name='Накопитель данных')
    videocard = models.CharField(max_length=100, verbose_name='Видеокарта')