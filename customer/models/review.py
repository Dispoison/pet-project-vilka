from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from shop.models.products.product_rating import ProductRating
from customer.models.customer import Customer


class Review(models.Model):
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']

    author = models.ForeignKey(Customer, verbose_name='Автор', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='Тип продукта')
    object_id = models.PositiveIntegerField(verbose_name='ID продукта')
    content_object = GenericForeignKey('content_type', 'object_id')
    text = models.TextField(verbose_name='Текст отзыва')
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Отзыв: {self.author}'


@receiver(post_save, sender=Review)
def update_review_product(sender, instance, created, **kwargs):
    if created:
        product_rating = ProductRating.objects.get(product_id=instance.object_id)
        product_rating.update_star_count(instance.rating)
