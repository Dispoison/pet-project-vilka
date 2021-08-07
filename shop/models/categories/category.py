from django.db import models
from django.urls import reverse


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Изображение')
    image_large = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, verbose_name='Большое изображение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})
