from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel
from shop.models.categories.subcategory import Subcategory


class Product(PolymorphicModel):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discounted_price = models.DecimalField(max_digits=9, decimal_places=2,
                                           null=True, blank=True, verbose_name='Цена со скидкой')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, verbose_name='Подкатегория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def clean(self):
        if self.discounted_price and self.discounted_price >= self.price:
            raise ValidationError("Цена со скидкой не может превышать или быть равной обычной цене")

    def get_price(self):
        return self.discounted_price if self.discounted_price else self.price
