from django.db import models
from shop.models.products.product import Product


class ProductPhoto(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.product.name
