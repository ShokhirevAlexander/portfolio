from django.db import models
from django.urls import reverse

from users.models import User


class CategoryModel(models.Model):
    category = models.CharField(max_length=100, unique=True, verbose_name='категория')
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='описание')

    class Meta:
        verbose_name_plural = 'категории'
        verbose_name = 'категория'

    def __str__(self):
        return self.category


class ProductsModel(models.Model):
    products = models.CharField(max_length=150, unique=True, verbose_name='продукт')
    slug = models.SlugField(verbose_name='URL', unique=False)
    description = models.CharField(max_length=250, null=True, blank=True, verbose_name='описание')
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    image = models.ImageField(upload_to='products_image')
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='productsmodel')

    class Meta:
        verbose_name_plural = 'продукты'
        verbose_name = 'продукт'

    def __str__(self):
        return self.products

    def get_absolute_url(self):
        return reverse('olga:single', kwargs={'products_slug': self.slug})


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, verbose_name='продукт')
    quantity = models.PositiveIntegerField(default=0, verbose_name='количество')
    created_timestamp = models.DateTimeField(auto_now_add=True)
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return self.user.username

    def sum(self):
        return self.quantity*self.product.price
