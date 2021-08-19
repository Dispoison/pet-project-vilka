from django.db import models


class ProductRating(models.Model):
    class Meta:
        verbose_name = 'Рейтинг продукта'
        verbose_name_plural = 'Рейтинги продуктов'

    product = models.OneToOneField('Product', on_delete=models.CASCADE, related_name='rating')
    rating = models.DecimalField(max_digits=2, decimal_places=1, verbose_name='Рейтинг', default=0)
    one_star_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов с одной звездой', default=0)
    two_star_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов с двумя звездами', default=0)
    three_star_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов с тремя звездами', default=0)
    four_star_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов с четырьмя звездами', default=0)
    five_star_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов с пятью звездами', default=0)
    total_stars_count = models.PositiveSmallIntegerField(verbose_name='Количество отзывов', default=0)

    def __str__(self):
        return self.product.name

    def update_star_count(self, rating, value):
        if rating == '1':
            self.one_star_count += value
        elif rating == '2':
            self.two_star_count += value
        elif rating == '3':
            self.three_star_count += value
        elif rating == '4':
            self.four_star_count += value
        elif rating == '5':
            self.five_star_count += value

        self.total_stars_count += value
        self._update_rating()
        self.save()

    def _update_rating(self):
        if self.total_stars_count:
            self.rating = (self.one_star_count + self.two_star_count * 2 + self.three_star_count * 3 +
                           self.four_star_count * 4 + self.five_star_count * 5) / self.total_stars_count
        else:
            self.rating = 0
