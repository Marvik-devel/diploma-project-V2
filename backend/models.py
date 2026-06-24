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

    # 3. Переключаем авторизацию на email вместо логина
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.get_type_display()})"