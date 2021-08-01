import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models
from operator import attrgetter
from shop.utils import get_random_int_numbers, poly_set_to_counted_products_list
from vilka import settings

from polymorphic.models import PolymorphicModel

User = get_user_model()


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


class Subcategory(models.Model):
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

    name = models.CharField(max_length=100, unique=True, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True, verbose_name='Изображение')
    parent = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Подкатегория')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'slug': self.slug})


class TopDiscountedProductsManager:
    @staticmethod
    def get_discounted_products_from_subclasses():
        products = Product.objects.filter(discounted_price__isnull=False).select_related('subcategory')
        [setattr(prod, 'discount', int(100 - 100 * (prod.discounted_price / prod.price))) for prod in products]
        products = sorted(products, key=attrgetter('discount'), reverse=True)
        return products


class TopDiscountedProducts:
    objects = TopDiscountedProductsManager()


class ThreeMainSubcategoriesManager:
    @staticmethod
    def get_three_main_subcategories():
        return Subcategory.objects.filter(name__in=['Смартфоны', 'Планшеты', 'Ноутбуки']).order_by('id')


class ThreeMainSubcategory:
    objects = ThreeMainSubcategoriesManager()


class ThreeRandomSubcategoryProductSetManager:
    @staticmethod
    def get_three_random_subcategory_products():
        subcategories_length = len(Product.objects.values('subcategory_id').distinct())
        three_random_subcategory_products = Product.objects\
            .filter(subcategory_id__in=get_random_int_numbers(3, 1, subcategories_length)).select_related('subcategory')
        return poly_set_to_counted_products_list(three_random_subcategory_products)


class ThreeRandomSubcategoryProductSet:
    objects = ThreeRandomSubcategoryProductSetManager()


class Product(PolymorphicModel):
    name = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discounted_price = models.DecimalField(max_digits=9, decimal_places=2,
                                           null=True, blank=True, verbose_name='Цена со скидкой')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.PROTECT, verbose_name='Подкатегория')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def clean(self):
        if self.discounted_price and self.discounted_price >= self.price:
            raise ValidationError("Цена со скидкой не может превышать или быть равной обычной цене")


class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return os.path.join(settings.MEDIA_URL, self.photo.url)


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


class SmartphoneAccessory(Product):
    class Meta:
        verbose_name = 'Аксессуар для смартфона'
        verbose_name_plural = 'Аксессуары для смартфона'

    form_factor = models.CharField(max_length=50, verbose_name='Форм фактор')
    material = models.CharField(max_length=50, verbose_name='Материал')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    compatible_model = models.CharField(max_length=100, verbose_name='Совместимая модель')


class TabletAccessory(Product):
    class Meta:
        verbose_name = 'Аксессуар для планшета'
        verbose_name_plural = 'Аксессуары для планшета'

    form_factor = models.CharField(max_length=50, verbose_name='Форм фактор')
    material = models.CharField(max_length=50, verbose_name='Материал')
    color = models.CharField(max_length=50, verbose_name='Цвет')
    tablet_diagonal = models.CharField(max_length=100, verbose_name='Диагональ планшета')


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


class Monitor(Product):
    class Meta:
        verbose_name = 'Монитор'
        verbose_name_plural = 'Мониторы'

    diagonal = models.CharField(max_length=100, verbose_name='Диагональ')
    frequency = models.PositiveSmallIntegerField(verbose_name='Частота обновления')
    resolution = models.CharField(max_length=50, verbose_name='Разрешение дисплея')
    matrix_type = models.CharField(max_length=50, verbose_name='Тип матрицы')


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


class SystemUnit(Product):
    class Meta:
        verbose_name = 'Системный блок'
        verbose_name_plural = 'Системные блоки'

    processor = models.CharField(max_length=100, verbose_name='Процессор')
    ram = models.CharField(max_length=50, verbose_name='Оперативная память')
    disk = models.CharField(max_length=50, verbose_name='Накопитель данных')
    videocard = models.CharField(max_length=100, verbose_name='Видеокарта')
    weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Вес')
    power = models.PositiveSmallIntegerField(verbose_name='Мощность БП')
    dimensions = models.CharField(max_length=100, verbose_name='Габаритные размеры')


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f'Продукт: {self.product.name}'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField('CartProduct', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return f'Покупатель: {self.user.first_name} {self.user.last_name}'
