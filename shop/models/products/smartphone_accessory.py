from django.db import models
from shop.models.products.product import Product


class SmartphoneAccessory(Product):
    class Meta:
        verbose_name = 'Аксессуар для смартфона'
        verbose_name_plural = 'Аксессуары для смартфона'

    form_factor = models.CharField(max_length=50, verbose_name='Форм фактор')
    material = models.CharField(max_length=50, verbose_name='Материал')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    compatible_model = models.CharField(max_length=100, verbose_name='Совместимая модель')