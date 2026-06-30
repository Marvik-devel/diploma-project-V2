from itertools import product

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # Спискок ролей
    USER_TYPE_CHOICES = (
        ('shop', 'Магазин'),
        ('customer', 'Покупатель')
    )

    # Добовляем поля
    email = models.EmailField(_('email address'), unique=True)
    company = models.CharField(_('company'), max_length=100, blank=True)
    position = models.CharField(_('position'),max_length=40, blank=True)
    type = models.CharField(_('user type'),
                            max_length=10,
                            choices = USER_TYPE_CHOICES,
                            default='customer'
    )

    # Переключаем авторизацию на email вместо логина
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return f"{self.email} ({self.get_type_display()})"
 # Класс для магазина
class Shop(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', null=True, blank=True)
    user = models.OneToOneField (
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    state = models.BooleanField(default=True, verbose_name='Статус работы')

class Category(models.Model):
    shops = models.ManyToManyField (max_length=50, verbose_name='Название', blank=True)
    name = models.CharField (max_length=40, verbose_name='Магазины')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список категорий'

    def __str__(self):
        return self.name

class Product (models.Model):
    name = models.CharField(max_length=80, verbose_name='Название')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
        related_name='product'
    )
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Списко продуктов'

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        on_delete=models.CASCADE,
        related_name='product_infos'
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name='Магазин',
        on_delete=models.CASCADE,
        related_name='product_infos'
    )

    name = models.CharField(max_length=80, verbose_name='Характеристика/Модель', blank=True)

    external_id = models.PositiveIntegerField(verbose_name='Внешний ID')

    quantity = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    price_rrc = models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информационные блоки о продуктах'

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"