from itertools import product
from tkinter.constants import CASCADE

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ForeignKey, CharField, PositiveIntegerField
from django.utils.translation import gettext_lazy as _

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен'),
)

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
    shops = models.ManyToManyField (Shop, verbose_name='Название', blank=True)
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

class Parameter(models.Model):
    name = models.CharField(max_length=80, verbose_name='Название параметра')

    class Meta:
        verbose_name = 'Параметр'
        verbose_name_plural = 'Список параметров'

    def __str__(self):
        return self.name

class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name='Информация о продукте',
        on_delete=models.CASCADE,
        related_name='product_parameters'
    )
    parameter = models.ForeignKey(
        Parameter,
        verbose_name='Параметр',
        on_delete=models.CASCADE,
        related_name = 'product_parameters'
    )
    value = models.CharField(max_length=80, verbose_name='Значение')

    class Meta:
        verbose_name = 'Параметр продукта'
        verbose_name_plural = 'Параметры продуктов'

    def __str__(self):
        return f"{self.parameter.name} - {self.value}"

class Contact(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакты пользователя'
        verbose_name_plural = "Список контактов пользователя"

    def __str__(self):
        return f'{self.city} {self.street} {self.house}'

class Order(models.Model):
    user = models.ForeignKey (
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    dt = models.DateTimeField (auto_now_add=True)
    state = models.CharField (max_length=15, choices=STATE_CHOICES, default='basket')
    contact = models.ForeignKey (Contact,
                                 blank=True,
                                 null=True,
                                 on_delete=models.SET_NULL
    )
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'

class OrderItem (models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    product_info = models.ForeignKey(
        ProductInfo,
        on_delete=models.CASCADE,
        related_name='order_item_info'
    )
    quantity = models.PositiveIntegerField()
